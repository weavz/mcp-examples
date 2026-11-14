# LlamaIndex MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect LlamaIndex to Notion, Google Drive, Google Docs and Google Sheets through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Notion MCP with LlamaIndex Python](docs/app-recipes.md#notion-mcp-with-llamaindex-python)
- [Google Drive MCP with LlamaIndex Python](docs/app-recipes.md#google-drive-mcp-with-llamaindex-python)
- [Google Docs MCP with LlamaIndex Python](docs/app-recipes.md#google-docs-mcp-with-llamaindex-python)
- [Google Sheets MCP with LlamaIndex Python](docs/app-recipes.md#google-sheets-mcp-with-llamaindex-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Uses LlamaIndex's `BasicMCPClient` and MCP `FunctionTool` adapter. Configure the Weavz server in Tool Mode or Code Mode first; `--mode` checks advertised names and cannot switch a live server.

Requires Python 3.11 or 3.12, uv, a custom Streamable HTTP endpoint, and an MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The loopback fixture is a separate bearer-protected MCP SDK server with synthetic data; the checks need no model. Copy `.env.example` to `.env` for live discovery with `uv run --env-file .env python main.py --mode tools` or `--mode code`. For the optional FunctionAgent run, connect an app with the requested data, set `WEAVZ_MODEL` and `OPENAI_API_KEY`, then pass `--prompt`.
