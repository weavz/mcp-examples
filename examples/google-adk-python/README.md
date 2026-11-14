# Google ADK + Weavz MCP

This starter uses ADK's native `McpToolset` with Streamable HTTP. Tool Mode and Code Mode are configured on the Weavz MCP server; `WEAVZ_MCP_MODE` checks the advertised tools and does not switch a remote server.

Requirements: Python 3.11 or 3.12, uv, a custom Weavz MCP endpoint and MCP access token. Do not use a Weavz REST API key. The personal `https://platform.weavz.io/mcp/weavz` endpoint uses OAuth.

## Local fixture

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The local fixture is an independent bearer-protected MCP SDK server with synthetic data. These checks call the ADK MCP transport and do not use a model or live Weavz.

## Weavz and optional model

Copy `.env.example` to `.env`, set the custom endpoint/token, then use `uv run --env-file .env python main.py --mode tools` or `--mode code` to discover actual tools. For an optional ADK agent run, connect an app with suitable records, set `WEAVZ_MODEL` to a model supported by your ADK configuration, provide its normal credentials, and pass `--prompt`.
