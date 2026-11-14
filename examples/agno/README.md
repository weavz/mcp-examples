# Agno MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect Agno to Slack, GitHub, Figma and HubSpot through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Slack MCP with Agno Python](docs/app-recipes.md#slack-mcp-with-agno-python)
- [GitHub MCP with Agno Python](docs/app-recipes.md#github-mcp-with-agno-python)
- [Figma MCP with Agno Python](docs/app-recipes.md#figma-mcp-with-agno-python)
- [HubSpot MCP with Agno Python](docs/app-recipes.md#hubspot-mcp-with-agno-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Connects Agno's native `MCPTools` over Streamable HTTP. Configure a custom Weavz MCP server in Tools Mode or Code Mode first; `--mode` checks the endpoint's actual tool names and does not switch its server configuration. The personal `/mcp/weavz` connector uses OAuth and does not accept a copied MCP bearer token.

Requires Python 3.11 or 3.12 and uv. Use an MCP access token in `WEAVZ_MCP_TOKEN`, not a Weavz REST API key.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

These fixture checks launch a local bearer-protected MCP SDK server with synthetic records. They exercise Agno's MCP client without a model or live Weavz account. For live discovery, copy `.env.example` to `.env` and run `uv run --env-file .env python main.py --mode tools` or `--mode code`. For an optional model run, configure an app with the task data, set `WEAVZ_MODEL` to a model identifier supported by your OpenAI-compatible provider and `OPENAI_API_KEY`, then add `--prompt "Summarize the records relevant to my current task"`.
