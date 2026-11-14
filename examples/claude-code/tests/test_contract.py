import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ClaudeCodeContract(unittest.TestCase):
 def test_http_oauth_config_has_no_inline_auth(self):
  cfg=json.loads((ROOT/".mcp.json").read_text())
  server=cfg["mcpServers"]["weavz"]
  self.assertEqual(server["type"],"http")
  self.assertEqual(server["url"],"https://platform.weavz.io/mcp/weavz")
  self.assertNotIn("headers",server); self.assertNotIn("Authorization",str(server))
 def test_claude_instructions(self):
  self.assertIn("wait for approval",(ROOT/"CLAUDE.md").read_text())
if __name__=='__main__': unittest.main()
