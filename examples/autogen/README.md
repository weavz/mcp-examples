# AutoGen + Weavz MCP

Connects Microsoft's AutoGen AgentChat through the native `McpWorkbench` and Streamable HTTP adapter. Configure a custom Weavz MCP server in Tools Mode or Code Mode first; the `--mode` option verifies tools from the configured server. The personal `/mcp/weavz` connector uses OAuth and does not accept a copied MCP bearer token.

Requires Python 3.11 or 3.12 and uv. `WEAVZ_MCP_TOKEN` must be an MCP access token, not a Weavz REST API key.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The fixture checks run without a model against a separate local bearer-protected MCP SDK server and synthetic data. For live discovery, copy `.env.example` to `.env` and use `uv run --env-file .env python main.py --mode tools` or `--mode code`. To run the optional AutoGen agent, connect an app with task-relevant records, set `WEAVZ_MODEL` to a model supported by your provider and `OPENAI_API_KEY` (plus `OPENAI_BASE_URL` for compatible endpoints), then add `--prompt "Summarize the records relevant to my current task"`.
