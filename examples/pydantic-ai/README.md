# PydanticAI MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect PydanticAI to Gmail, Google Sheets, Notion and Figma through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Gmail MCP with PydanticAI Python](docs/app-recipes.md#gmail-mcp-with-pydanticai-python)
- [Google Sheets MCP with PydanticAI Python](docs/app-recipes.md#google-sheets-mcp-with-pydanticai-python)
- [Notion MCP with PydanticAI Python](docs/app-recipes.md#notion-mcp-with-pydanticai-python)
- [Figma MCP with PydanticAI Python](docs/app-recipes.md#figma-mcp-with-pydanticai-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

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
uv run --env-file .env python main.py --mode tools
uv run --env-file .env python main.py --mode code
```

These commands discover and display the server's actual tools. They do not call a demo alias on a live server. Keep the token in your local environment; do not commit it.

## Optional model run

Set `WEAVZ_MODEL` to a model string accepted by PydanticAI, configure that model provider's credentials, and connect an app containing records for your task. Then run:

```sh
uv run --env-file .env python main.py --mode tools --prompt "Find the latest record matching the task you connected"
```

The MCP connection remains open for the full agent run and closes afterward. This optional path calls your configured model provider; it is separate from fixture tests.
