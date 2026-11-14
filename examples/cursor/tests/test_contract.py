import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CursorContract(unittest.TestCase):
 def test_project_remote_config_oauth_default(self):
  cfg=json.loads((ROOT/".cursor/mcp.json").read_text())
  server=cfg["mcpServers"]["weavz"]
  self.assertEqual(server["url"],"https://platform.weavz.io/mcp/weavz")
  self.assertNotIn("headers",server); self.assertNotIn("Authorization",str(server))
 def test_native_rule_and_agents_file(self):
  self.assertTrue((ROOT/".cursor/rules/weavz.mdc").exists())
  self.assertIn("wait for approval",(ROOT/"AGENTS.md").read_text())
if __name__=='__main__': unittest.main()
