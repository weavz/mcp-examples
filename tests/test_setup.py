from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Thread
import unittest

from weavz_sdk import WeavzClient

from tools.setup_weavz import configure, validate_url


WORKSPACE = "00000000-0000-4000-8000-000000000001"
SERVER = "00000000-0000-4000-8000-000000000002"
END_USER = "customer-example"


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.duplicate = False
        self.fail_token = False
        self.server_data = {"id": SERVER, "workspaceId": WORKSPACE, "mode": "CODE", "authMode": "bearer", "endUserId": END_USER}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def respond(self, status, value):
                body = json.dumps(value).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                owner.requests.append(("GET", self.path, None))
                self.respond(200, {"server": owner.server_data})

            def do_POST(self):
                assert self.headers["Authorization"] == "Bearer wvz_example_fixture_only"
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.requests.append(("POST", self.path, body))
                if self.path == "/api/v1/end-users":
                    self.respond(409 if owner.duplicate else 201, {"code": "DUPLICATE", "error": "Already exists"} if owner.duplicate else {"endUser": {"id": "example"}})
                elif self.path == "/api/v1/mcp/servers":
                    self.respond(201, {"server": {"id": SERVER}, "bearerToken": "mcp_unused_static_fixture"})
                elif self.path == f"/api/v1/mcp/servers/{SERVER}/access-tokens":
                    if owner.fail_token:
                        self.respond(503, {"code": "TEMPORARY", "error": "Try later"})
                    else:
                        self.respond(201, {"accessToken": "mcp_scoped_fixture_only", "mcpEndpoint": f"https://platform.example.com/mcp/srv_{SERVER}"})
                else:
                    self.respond(404, {"error": "Unexpected route"})

        self.http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()
        self.client = WeavzClient(api_key="wvz_example_fixture_only", base_url=f"http://127.0.0.1:{self.http.server_port}", max_retries=0)

    def tearDown(self):
        self.client.close()
        self.http.shutdown()
        self.http.server_close()
        self.thread.join(timeout=3)
        self.assertFalse(self.thread.is_alive())

    def test_creates_end_user_bound_server_and_scoped_expiring_token(self):
        result = configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code")
        self.assertEqual(result["WEAVZ_MCP_TOKEN"], "mcp_scoped_fixture_only")
        self.assertNotEqual(result["WEAVZ_MCP_TOKEN"], "mcp_unused_static_fixture")
        creation = self.requests[1][2]
        self.assertEqual(creation["endUserId"], END_USER)
        self.assertEqual(creation["endUserAccess"], "restricted")
        token = self.requests[2][2]
        self.assertEqual(token, {"endUserId": END_USER, "scopes": ["mcp:tools", "mcp:code"], "expiresIn": 3600})

    def test_reuses_existing_user_and_matching_server_without_changing_it(self):
        self.duplicate = True
        configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code", server_id=SERVER)
        self.assertEqual([method for method, _, _ in self.requests], ["GET", "POST", "POST"])
        self.assertNotIn("/api/v1/mcp/servers", [path for _, path, _ in self.requests])

    def test_token_failure_preserves_created_server_id_for_recovery_without_deletion(self):
        self.fail_token = True
        created = []
        with self.assertRaises(Exception):
            configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code", on_server_created=created.append)
        self.assertEqual(created, [SERVER])
        self.assertEqual([method for method, _, _ in self.requests], ["POST", "POST", "POST"])

    def test_tools_mode_token_does_not_gain_code_scope(self):
        configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="tools")
        self.assertEqual(self.requests[-1][2]["scopes"], ["mcp:tools"])
        self.assertEqual(self.requests[1][2]["mode"], "TOOLS")

    def test_rejects_cross_workspace_server_before_writes(self):
        self.server_data["workspaceId"] = "00000000-0000-4000-8000-000000000099"
        with self.assertRaisesRegex(ValueError, "different workspace"):
            configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code", server_id=SERVER)
        self.assertEqual(len(self.requests), 1)

    def test_rejects_another_end_users_server_before_writes(self):
        self.server_data["endUserId"] = "another-customer"
        with self.assertRaisesRegex(ValueError, "another end user"):
            configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code", server_id=SERVER)
        self.assertEqual(len(self.requests), 1)

    def test_does_not_change_existing_mode_or_auth(self):
        for field, value, message in [("mode", "TOOLS", "server mode"), ("authMode", "oauth", "does not accept")]:
            with self.subTest(field=field):
                old = self.server_data[field]
                self.server_data[field] = value
                with self.assertRaisesRegex(ValueError, message):
                    configure(self.client, workspace_id=WORKSPACE, end_user_id=END_USER, mode="code", server_id=SERVER)
                self.server_data[field] = old
        self.assertTrue(all(method == "GET" for method, _, _ in self.requests))

    def test_rejects_bad_input_before_network(self):
        for workspace, mode, end_user in [("not-a-uuid", "code", END_USER), (WORKSPACE, "invalid", END_USER), (WORKSPACE, "tools", "")]:
            with self.subTest(workspace=workspace, mode=mode):
                with self.assertRaises(ValueError):
                    configure(self.client, workspace_id=workspace, end_user_id=end_user, mode=mode)
        self.assertEqual(self.requests, [])


class UrlTests(unittest.TestCase):
    def test_secure_and_loopback_urls(self):
        for url in ["https://platform.example.com", "http://127.0.0.1:8765/mcp", "http://[::1]:8765/mcp"]:
            self.assertEqual(validate_url(url), url)

    def test_credentials_and_unsafe_urls(self):
        for url in ["http://example.com/mcp", "https://user:secret@example.com/mcp", "https://example.com/mcp?token=secret", "https://example.com/mcp#fragment", "file:///etc/passwd"]:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_url(url)


if __name__ == "__main__":
    unittest.main()
