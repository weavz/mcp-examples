import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PiContract(unittest.TestCase):
 def test_project_mcp_and_oauth_discovery(self):
  cfg=json.loads((ROOT/".pi/mcp.json").read_text())
  server=cfg["mcpServers"]["weavz"]
  self.assertEqual(server["url"],"https://platform.weavz.io/mcp/weavz")
  self.assertNotIn("headers",server); self.assertNotIn("Authorization",str(server))
 def test_project_instructions_separate(self):
  self.assertIn("OAuth",(ROOT/".pi/APPEND_SYSTEM.md").read_text())
  self.assertIn("MCP setup is client configuration",(ROOT/"AGENTS.md").read_text())
if __name__=='__main__': unittest.main()
