# PydanticAI + Weavz MCP

This starter connects a PydanticAI agent to a remote Weavz MCP server using PydanticAI's native MCP toolset. Tool Mode and Code Mode are selected when you configure the MCP server in Weavz. `WEAVZ_MCP_MODE` is used to validate the tools advertised by that server; it does not change the remote server's mode.

## Requirements

- Python 3.11 or 3.12
- uv
- A custom Streamable HTTP MCP endpoint and MCP access token from your Weavz setup. Do not use a Weavz customer REST API key as the MCP token. The personal `https://platform.weavz.io/mcp/weavz` endpoint uses OAuth rather than this bearer-token setup.

## Run the local fixture

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The fixture starts a separate bearer-protected MCP SDK server on loopback and calls it through PydanticAI's actual `MCPToolset`. It only returns synthetic data. It does not call a model or a live Weavz server.

## Connect to your Weavz MCP server

Copy `.env.example` to `.env` and set `WEAVZ_MCP_URL`, `WEAVZ_MCP_TOKEN`, and `WEAVZ_MCP_MODE` to values from your custom Weavz MCP setup. The endpoint must already be configured for the selected mode.

```sh
uv run python main.py --mode tools
uv run python main.py --mode code
```

These commands discover the server's tools and execute one deterministic lookup. Keep the token in your local environment; do not commit it.

## Optional model run

Set `WEAVZ_MODEL` to a model string accepted by PydanticAI and configure that model provider's credentials in the environment. Then run:

```sh
uv run python main.py --mode tools --prompt "Look up record-1"
```

The MCP connection remains open for the full agent run and closes afterward. This optional path calls your configured model provider; it is separate from fixture tests.
