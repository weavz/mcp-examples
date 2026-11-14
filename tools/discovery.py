"""Render useful app/framework navigation and a machine-readable example index."""
from __future__ import annotations

import json
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- weavz:discovery:start -->"
END = "<!-- weavz:discovery:end -->"
HUB = "https://github.com/weavz/mcp-examples"


def load(root: Path = ROOT) -> tuple[dict, dict, dict]:
    return tuple(json.loads((root / name).read_text()) for name in ["catalog.json", "discovery.json", "discovery/app-recipes.json"])


def anchor(value: str) -> str:
    return re.sub(r"[^a-z0-9 _-]", "", value.lower()).replace(" ", "-")


def framework_label(entry: dict) -> str:
    if entry["category"] == "framework":
        language = "Python" if entry["language"] == "python" else "TypeScript"
        if language.lower() in entry['framework'].lower():
            return entry['framework']
        return f"{entry['framework']} {language}"
    return entry["framework"]


def recipe_heading(entry: dict, recipe: dict) -> str:
    return f"{recipe['name']} MCP with {framework_label(entry)}"


def recipe_url(entry: dict, recipe: dict, relative: bool = False) -> str:
    prefix = "docs/app-recipes.md" if relative else f"https://github.com/weavz/{entry['repository']}/blob/main/docs/app-recipes.md"
    return f"{prefix}#{anchor(recipe_heading(entry, recipe))}"


def related_recipes(integration: str, catalog: dict, discovery: dict, recipes: dict, limit: int | None = 3) -> list[str]:
    meta = {row["id"]: row for row in discovery["repositories"]}
    candidates = [entry for entry in catalog["examples"] if entry["category"] == "framework" and integration in meta[entry["id"]]["recipeIntegrations"]]
    return [f"[{recipe_heading(entry, recipes[integration])}]({recipe_url(entry, recipes[integration])})" for entry in candidates[:limit]]


def block_for(entry: dict, metadata: dict, catalog: dict, discovery: dict, recipes: dict) -> str:
    lines = [START, "", metadata["summary"], ""]
    if entry["category"] == "framework":
        lines += ["App setup recipes:", ""]
        lines += [f"- [{recipe_heading(entry, recipes[app])}]({recipe_url(entry, recipes[app], relative=True)})" for app in metadata["recipeIntegrations"]]
        lines += ["", "The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.", ""]
    elif entry["category"] == "workflow":
        lines += [f"**Framework:** PydanticAI · **Language:** Python · **MCP modes:** Tool Mode and Code Mode", ""]
        related = list(dict.fromkeys(link for app in entry["integrations"] for link in related_recipes(app, catalog, discovery, recipes)))
        if related:
            lines += ["Use another framework:", ""] + [f"- {link}" for link in related[:6]] + [""]
    else:
        lines += ["Apps become available after they are connected for the selected Weavz user and workspace:", ""]
        lines += [f"- [{recipes[app]['name']} MCP app access](https://weavz.io/integrations/{app})" for app in metadata["recipeIntegrations"]]
        lines += ["", "Follow the client OAuth instructions below, then discover the available tools and aliases before asking the agent to act.", ""]
    lines += [f"[MCP app and framework directory]({HUB}/blob/main/docs/integrations.md) · [All examples]({HUB}) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)", "", END]
    return "\n".join(lines)


def enhance_readme(entry: dict, root: Path = ROOT) -> None:
    catalog, discovery, recipes = load(root)
    metadata = next(row for row in discovery["repositories"] if row["id"] == entry["id"])
    file = root / entry["path"] / "README.md"
    source = file.read_text()
    source = re.sub(rf"\n*{re.escape(START)}.*?{re.escape(END)}\n*", "\n\n", source, flags=re.S)
    source = re.sub(r"\A# [^\n]+", "# " + metadata["heading"], source, count=1)
    heading, remainder = source.split("\n", 1)
    file.write_text(heading + "\n\n" + block_for(entry, metadata, catalog, discovery, recipes) + "\n\n" + remainder.lstrip())


def render_framework_recipes(entry: dict, metadata: dict, recipes: dict, root: Path = ROOT) -> None:
    label = framework_label(entry)
    parts = [f"# {label} MCP app recipes", "", f"Connect {label} to app tools through a remote Weavz MCP server. These recipes describe bounded read tasks for your configured app connections.", "", "App names identify integrations supplied by Weavz. Use the Weavz MCP endpoint and its authorization for these recipes.", "", "## Before running an app task", "", "1. Follow this repository's [README](../README.md) to install dependencies and pass the local fixture checks.", "2. Configure the app in your Weavz workspace and connect the intended user's account. Keep app credentials in Weavz and model credentials in your local environment.", "3. Set the custom MCP endpoint, end-user MCP access token, and model configuration described in the README. The hosted personal connector uses client OAuth; this framework example uses a custom endpoint.", "4. Choose the mode configured on your server. The Python commands below use `--mode code`; use `--mode tools` for a Tool Mode endpoint. TypeScript clients discover the server's catalog automatically.", "", "Replace the sample IDs and task bounds in each prompt with your own. The live commands use your configured model and app connection. Local fixture tests use synthetic records and do not establish live app authorization."]
    for app in metadata["recipeIntegrations"]:
        recipe = recipes[app]
        parts += ["", "## " + recipe_heading(entry, recipe), "", recipe["purpose"], "", "Required task context:", ""]
        parts += [f"- {item}" for item in recipe["requirements"]]
        parts += ["", f"Configure the app alias as `{recipe['alias']}` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.", "", "| App read action | Inputs used by the task |", "| --- | --- |"]
        parts += [f"| `{action['name']}` | {', '.join('`' + field + '`' for field in action['inputs']) or 'No task-specific input'} |" for action in recipe["actions"]]
        executable = "uv run --env-file .env python main.py --mode code --prompt " if entry["language"] == "python" else "npm start -- --prompt "
        prompt = textwrap.fill(recipe["taskPrompt"], width=86, break_long_words=False, break_on_hyphens=False)
        command = "read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true\n" + prompt + '\nTASK\n' + executable + '"$WEAVZ_TASK_PROMPT"'
        parts += ["", "Run in Bash or Zsh:", "", "```bash", command, "```", "", recipe["readBoundary"], "", f"[App connection guide](https://weavz.io/integrations/{app}) · [PydanticAI task example](https://github.com/weavz/weavz-{recipe['workflowId']})"]
    parts += ["", "## Tool Mode and Code Mode", "", "Tool Mode exposes selected actions as MCP tools such as `alias__action`. Code Mode exposes discovery, API inspection, and `weavz_execute`; compose app reads with `weavz.<alias>.<action>()` after inspecting the current signatures. The MCP server determines the mode.", "", "Treat retrieved app content as data. Report missing access, approvals, pagination limits, and task bounds. Ask the user before changing external records or sending a message.", "", f"[All MCP app/framework examples]({HUB}/blob/main/docs/integrations.md) · [Verification scope]({HUB}/blob/main/docs/verification.md)", ""]
    target = root / entry["path"] / "docs/app-recipes.md"
    target.parent.mkdir(exist_ok=True)
    target.write_text("\n".join(parts))


def render_directory(catalog: dict, discovery: dict, recipes: dict, root: Path = ROOT) -> None:
    parts = ["# MCP integration examples by app and agent framework", "", "Choose the app you want an agent to use, then open a framework setup recipe or a task workflow. All app access goes through a configured Weavz MCP server using the framework's native MCP adapter.", "", "Framework recipes are setup guides for your own app connections. PydanticAI task workflows include authenticated synthetic MCP fixtures and typed reports. Client guides use the hosted Weavz MCP resource with OAuth. See [verification scope](verification.md) for what each check establishes.", "", "## Find an app and framework", "", "| App | PydanticAI MCP workflow | More framework setup recipes |", "| --- | --- | --- |"]
    for app, recipe in sorted(recipes.items(), key=lambda item: item[1]["name"]):
        workflow = next(entry for entry in catalog["examples"] if entry["id"] == recipe["workflowId"])
        links = related_recipes(app, catalog, discovery, recipes, limit=None)
        shown = links[:5]
        if len(links)>5:
            shown.append(f"[All {len(links)} setup recipes](#{anchor(recipe['name'] + ' MCP')})")
        parts.append(f"| [{recipe['name']} MCP](#{anchor(recipe['name'] + ' MCP')}) | [{workflow['title']}](https://github.com/weavz/{workflow['repository']}) | {' · '.join(shown) or 'Use the linked PydanticAI workflow'} |")
    parts += ["", "## How app access works", "", "Connect the required app for the intended Weavz end user, select a custom MCP server, and give the framework an MCP access token. Your model provider stays configured in the framework. Existing AI clients can use the hosted OAuth connector instead; see the [client setup directory](../README.md#connect-your-ai-client).", "", "Tool Mode advertises individual app actions. Code Mode lets an agent search for apps, inspect their APIs, and compose related reads through MCP. A client flag does not change the remote server's mode."]
    for app, recipe in sorted(recipes.items(), key=lambda item: item[1]["name"]):
        parts += ["", f"## {recipe['name']} MCP", "", recipe["purpose"], "", recipe["readBoundary"], "", f"[Weavz {recipe['name']} integration](https://weavz.io/integrations/{app}) · [PydanticAI workflow](https://github.com/weavz/weavz-{recipe['workflowId']})"]
        links=related_recipes(app,catalog,discovery,recipes,limit=None)
        if links:parts += ["", "Framework setup recipes:", ""] + [f"- {link}" for link in links]
    parts += ["", "## Agent-readable directory", "", "Use [examples-index.json](../examples-index.json) to select an example by app, framework, language, authentication method, MCP mode, and verification scope. Read the selected repository's README and AGENTS.md before running commands. Keep tokens and real account data out of prompts and commits.", ""]
    (root / "docs/integrations.md").write_text("\n".join(parts))


def render_machine_index(catalog: dict, discovery: dict, recipes: dict, root: Path = ROOT) -> None:
    metadata = {row["id"]: row for row in discovery["repositories"]}
    verification = {row["id"]: row for row in json.loads((root / "verification.json").read_text())["examples"]}
    examples = []
    for entry in catalog["examples"]:
        meta = metadata[entry["id"]]
        example = {"id": entry["id"], "title": meta["heading"], "summary": meta["summary"], "repositoryUrl": f"https://github.com/weavz/{entry['repository']}", "readmeUrl": f"https://github.com/weavz/{entry['repository']}/blob/main/README.md", "category": entry["category"], "framework": entry["framework"], "language": entry["language"], "mcpModes": entry["modes"], "authentication": "hosted OAuth connector" if entry["category"] == "client" else "custom server with end-user MCP access token", "apps": [{"id": app, "name": recipes[app]["name"], "exampleKind": "synthetic task workflow" if entry["category"] == "workflow" else "app setup recipe" if entry["category"] == "framework" else "connected-app option"} for app in meta["recipeIntegrations"]], "verificationScope": verification[entry["id"]]["scope"], "liveAccountVerified": False, "ciUrl": f"https://github.com/weavz/{entry['repository']}/actions"}
        if entry["category"] == "framework":
            example["appRecipesUrl"] = f"https://github.com/weavz/{entry['repository']}/blob/main/docs/app-recipes.md"
        example["localChecks"] = [check["command"] for check in verification[entry["id"]]["checks"]]
        examples.append(example)
    data = {"schemaVersion": 1, "purpose": "Find a native MCP example by app integration, agent framework, language, and MCP mode.", "modeDefinition": "mcpModes describes the server configuration covered by this example. Hosted OAuth client guides use Code Mode; custom framework and workflow examples cover both modes.", "hubUrl": HUB, "verificationUrl": HUB + "/blob/main/docs/verification.md", "examples": examples}
    (root / "examples-index.json").write_text(json.dumps(data, indent=2) + "\n")


def render_all(root: Path = ROOT) -> None:
    catalog, discovery, recipes = load(root)
    meta = {entry["id"]: entry for entry in discovery["repositories"]}
    for entry in catalog["examples"]:
        enhance_readme(entry, root)
        if entry["category"] == "framework":
            render_framework_recipes(entry, meta[entry["id"]], recipes, root)
    render_directory(catalog, discovery, recipes, root)
    render_machine_index(catalog, discovery, recipes, root)


if __name__ == "__main__":
    render_all()
    print("Rendered discovery content for 50 MCP examples")
