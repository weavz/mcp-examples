from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from tools.discovery import START, END, anchor, enhance_readme, load, recipe_heading, render_all

ROOT = Path(__file__).resolve().parents[1]


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.discovery, cls.recipes = load(ROOT)
        cls.entries = {entry["id"]: entry for entry in cls.catalog["examples"]}
        cls.metadata = {entry["id"]: entry for entry in cls.discovery["repositories"]}

    def test_every_published_example_has_valid_search_metadata(self):
        self.assertEqual(set(self.entries), set(self.metadata))
        self.assertEqual(len(self.entries), 50)
        for ident, row in self.metadata.items():
            with self.subTest(example=ident):
                self.assertGreater(len(row["description"]), 60)
                self.assertLessEqual(len(row["description"]), 350)
                self.assertLessEqual(len(row["topics"]), 20)
                self.assertEqual(len(row["topics"]), len(set(row["topics"])))
                self.assertTrue(all(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic) for topic in row["topics"]))
                self.assertIn("mcp", row["topics"])
                self.assertIn("MCP", row["heading"])
                self.assertIn(self.entries[ident]["framework"], row["heading"])
                self.assertTrue(set(row["recipeIntegrations"]) <= set(self.recipes))
                self.assertTrue(row["homepage"].startswith("https://weavz.io/"))

    def test_every_workflow_app_has_a_source_backed_recipe(self):
        apps = {app for entry in self.entries.values() for app in entry.get("integrations", [])}
        self.assertEqual(apps, set(self.recipes))
        for app, recipe in self.recipes.items():
            with self.subTest(app=app):
                self.assertEqual(recipe['name'], self.discovery['integrationNames'][app])
                workflow = self.entries[recipe["workflowId"]]
                self.assertIn(app, workflow["integrations"])
                scenario = json.loads((ROOT / "workflows" / f"{workflow['id']}.json").read_text())
                action_inputs = {step["action"]: set(step["arguments"]) for step in scenario["steps"] if step["integration"] == app}
                self.assertTrue(recipe["alias"].isidentifier())
                self.assertIn(recipe["alias"], recipe["taskPrompt"])
                self.assertTrue(recipe["requirements"])
                self.assertTrue(recipe["readBoundary"])
                for action in recipe["actions"]:
                    self.assertIn(action["name"], action_inputs)
                    self.assertTrue(set(action["inputs"]) <= action_inputs[action["name"]])

    def test_machine_directory_preserves_auth_and_verification_boundaries(self):
        index = json.loads((ROOT / "examples-index.json").read_text())
        self.assertEqual({row["id"] for row in index["examples"]}, set(self.entries))
        for row in index["examples"]:
            self.assertFalse(row["liveAccountVerified"])
            self.assertTrue(row["localChecks"])
            self.assertEqual(set(row["mcpModes"]), {"code"} if row['category'] == 'client' else {"tools", "code"})
            self.assertIn("OAuth" if row["category"] == "client" else "end-user MCP access token", row["authentication"])
            self.assertEqual({app["id"] for app in row["apps"]}, set(self.metadata[row["id"]]["recipeIntegrations"]))

    def test_generated_links_resolve_to_actual_recipe_headings(self):
        directory=(ROOT/'docs/integrations.md').read_text()
        for entry in self.entries.values():
            content = (ROOT / entry["path"] / "README.md").read_text()
            self.assertEqual(content.count(START), 1)
            self.assertEqual(content.count(END), 1)
            prose = re.sub(r"```.*?```", "", content, flags=re.S)
            self.assertEqual(len(re.findall(r"^# ", prose, flags=re.M)), 1)
            if entry["category"] != "framework": continue
            recipes_file = ROOT / entry["path"] / "docs/app-recipes.md"
            recipe_content = recipes_file.read_text()
            headings = {anchor(value) for value in re.findall(r"^## (.+)$", recipe_content, flags=re.M)}
            links = re.findall(r"\]\(docs/app-recipes\.md#([^\)]+)\)", content)
            self.assertEqual(len(links), len(self.metadata[entry["id"]]["recipeIntegrations"]))
            self.assertTrue(set(links) <= headings)
            for app in self.metadata[entry["id"]]["recipeIntegrations"]:
                self.assertIn(recipe_heading(entry, self.recipes[app]), recipe_content)
                self.assertIn(recipe_heading(entry, self.recipes[app]), directory)

    def test_recipe_commands_are_shell_valid_and_use_the_documented_cli(self):
        count = 0
        for entry in self.entries.values():
            if entry["category"] != "framework": continue
            content = (ROOT / entry["path"] / "docs/app-recipes.md").read_text()
            commands = re.findall(r"```bash\n(.*?)\n```", content, flags=re.S)
            for index, command in enumerate(commands):
                result = subprocess.run(["bash", "-n"], input=command, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, f"{entry['id']}: {result.stderr}")
                self.assertIn("--prompt", command)
                self.assertIn("<<'TASK'", command)
                self.assertIn("uv run --env-file .env python main.py" if entry["language"] == "python" else "npm start -- --prompt", command)
                # Stub the framework CLI and verify the prompt is passed as one
                # literal argument; no provider or account is contacted.
                stub = "uv() { printf '%s' \"${!#}\"; }; npm() { printf '%s' \"${!#}\"; };\n"
                executed = subprocess.run(["bash"], input=stub + command, text=True, capture_output=True)
                self.assertEqual(executed.returncode, 0, executed.stderr)
                recipe = self.recipes[self.metadata[entry['id']]['recipeIntegrations'][index]]
                self.assertEqual(executed.stdout.split(), recipe['taskPrompt'].split())
                if shutil.which('zsh'):
                    zsh_stub = "uv() { printf '%s' \"${argv[-1]}\"; }; npm() { printf '%s' \"${argv[-1]}\"; };\n"
                    zsh = subprocess.run(['zsh', '-f'], input=zsh_stub + command, text=True, capture_output=True)
                    self.assertEqual(zsh.returncode, 0, zsh.stderr)
                    self.assertEqual(zsh.stdout.split(), recipe['taskPrompt'].split())
                count += 1
        self.assertEqual(count, 72)

    def test_generators_are_idempotent_and_keep_existing_setup_text(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory)
            for name in ["catalog.json", "discovery.json", "verification.json", "discovery", "docs"]:
                source = ROOT / name
                if source.is_dir(): shutil.copytree(source, copy / name)
                else: shutil.copyfile(source, copy / name)
            for entry in self.entries.values():
                target = copy / entry["path"]
                target.mkdir(parents=True)
                shutil.copyfile(ROOT / entry["path"] / "README.md", target / "README.md")
            before = {entry["id"]: (copy / entry["path"] / "README.md").read_bytes() for entry in self.entries.values()}
            render_all(copy)
            render_all(copy)
            for entry in self.entries.values():
                self.assertEqual(before[entry["id"]], (copy / entry["path"] / "README.md").read_bytes(), entry["id"])
            self.assertEqual((ROOT / "examples-index.json").read_bytes(), (copy / "examples-index.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
