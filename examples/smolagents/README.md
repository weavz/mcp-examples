# smolagents + Weavz MCP

Uses Hugging Face smolagents' native `MCPClient` for Streamable HTTP. Configure the Weavz MCP server in Tool Mode or Code Mode first; `--mode` checks the tools and does not switch a remote server.

Requires Python 3.11 or 3.12, uv, and a custom endpoint plus MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

Fixture checks use a separate bearer-protected MCP SDK server and synthetic data; no model or live Weavz call is made. For live discovery, copy `.env.example` to `.env` and use `uv run --env-file .env python main.py --mode tools` or `--mode code`. For an optional CodeAgent run, set `WEAVZ_MODEL`, configure `OPENAI_API_KEY` (and `OPENAI_BASE_URL` if needed), connect an app with relevant records, then add `--prompt`.
