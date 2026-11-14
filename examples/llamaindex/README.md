# LlamaIndex + Weavz MCP

Uses LlamaIndex's `BasicMCPClient` and MCP `FunctionTool` adapter. Configure the Weavz server in Tool Mode or Code Mode first; `--mode` checks advertised names and cannot switch a live server.

Requires Python 3.11 or 3.12, uv, a custom Streamable HTTP endpoint, and an MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The loopback fixture is a separate bearer-protected MCP SDK server with synthetic data; the checks need no model. Copy `.env.example` to `.env` for live discovery with `uv run --env-file .env python main.py --mode tools` or `--mode code`. For the optional FunctionAgent run, connect an app with the requested data, set `WEAVZ_MODEL` and `OPENAI_API_KEY`, then pass `--prompt`.
