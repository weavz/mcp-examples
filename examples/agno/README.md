# Agno + Weavz MCP

Connects Agno's native `MCPTools` over Streamable HTTP. Configure a custom Weavz MCP server in Tools Mode or Code Mode first; `--mode` checks the endpoint's actual tool names and does not switch its server configuration. The personal `/mcp/weavz` connector uses OAuth and does not accept a copied MCP bearer token.

Requires Python 3.11 or 3.12 and uv. Use an MCP access token in `WEAVZ_MCP_TOKEN`, not a Weavz REST API key.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

These fixture checks launch a local bearer-protected MCP SDK server with synthetic records. They exercise Agno's MCP client without a model or live Weavz account. For live discovery, copy `.env.example` to `.env` and run `uv run --env-file .env python main.py --mode tools` or `--mode code`. For an optional model run, configure an app with the task data, set `WEAVZ_MODEL` to a model identifier supported by your OpenAI-compatible provider and `OPENAI_API_KEY`, then add `--prompt "Summarize the records relevant to my current task"`.
