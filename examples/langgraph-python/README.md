# LangGraph + Weavz MCP

Uses the LangChain MCP adapter to bind server-discovered tools into a LangGraph ReAct workflow. Configure Weavz in Tool Mode or Code Mode first; local `--mode` validates the expected names and cannot switch a live server.

Requires Python 3.11 or 3.12, uv, a custom MCP URL, and its MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The independent fixture is a real bearer-protected MCP SDK server with synthetic data. It requires no model. Copy `.env.example` to `.env`; use `uv run --env-file .env python main.py --mode tools` or `--mode code` to inspect live tools. For an optional model run, connect an app containing the data needed for your prompt, set `WEAVZ_MODEL` and `OPENAI_API_KEY`, and pass `--prompt`. LangGraph executes the MCP-backed graph while the tools remain attached.
