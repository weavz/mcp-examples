# Google ADK (Python) MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect Google ADK (Python) to Gmail, Google Calendar, Google Drive and Google Sheets through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Gmail MCP with Google ADK Python](docs/app-recipes.md#gmail-mcp-with-google-adk-python)
- [Google Calendar MCP with Google ADK Python](docs/app-recipes.md#google-calendar-mcp-with-google-adk-python)
- [Google Drive MCP with Google ADK Python](docs/app-recipes.md#google-drive-mcp-with-google-adk-python)
- [Google Sheets MCP with Google ADK Python](docs/app-recipes.md#google-sheets-mcp-with-google-adk-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

This starter uses ADK's native `McpToolset` with Streamable HTTP. Tool Mode and Code Mode are configured on the Weavz MCP server; `WEAVZ_MCP_MODE` checks the advertised tools and does not switch a remote server.

Requirements: Python 3.11 or 3.12, uv, a custom Weavz MCP endpoint and MCP access token. Do not use a Weavz REST API key. The personal `https://platform.weavz.io/mcp/weavz` endpoint uses OAuth.

## Local fixture

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The local fixture is an independent bearer-protected MCP SDK server with synthetic data. A deterministic in-process ADK model drives the normal `Runner` and `McpTool` path, without a model provider or live Weavz.

## Weavz and optional model

Copy `.env.example` to `.env`, set the custom endpoint/token, then use `uv run --env-file .env python main.py --mode tools` or `--mode code` to discover actual tools. For an optional ADK agent run, connect an app with suitable records, set `WEAVZ_MODEL` to a model supported by your ADK configuration, provide its normal credentials, and pass `--prompt`.
