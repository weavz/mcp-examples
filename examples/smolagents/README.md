# smolagents MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect smolagents to GitHub, Figma, Google Sheets and Gmail through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [GitHub MCP with smolagents Python](docs/app-recipes.md#github-mcp-with-smolagents-python)
- [Figma MCP with smolagents Python](docs/app-recipes.md#figma-mcp-with-smolagents-python)
- [Google Sheets MCP with smolagents Python](docs/app-recipes.md#google-sheets-mcp-with-smolagents-python)
- [Gmail MCP with smolagents Python](docs/app-recipes.md#gmail-mcp-with-smolagents-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Uses Hugging Face smolagents' native `MCPClient` for Streamable HTTP. Configure the Weavz MCP server in Tool Mode or Code Mode first; `--mode` checks the tools and does not switch a remote server.

Requires Python 3.11 or 3.12, uv, and a custom endpoint plus MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

Fixture checks use a separate bearer-protected MCP SDK server and synthetic data; no model or live Weavz call is made. For live discovery, copy `.env.example` to `.env` and use `uv run --env-file .env python main.py --mode tools` or `--mode code`. For an optional CodeAgent run, set `WEAVZ_MODEL`, configure `OPENAI_API_KEY` (and `OPENAI_BASE_URL` if needed), connect an app with relevant records, then add `--prompt`.
