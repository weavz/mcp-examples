# LangGraph (Python) MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect LangGraph (Python) to Gmail, Slack, GitHub and Jira Cloud through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Gmail MCP with LangGraph Python](docs/app-recipes.md#gmail-mcp-with-langgraph-python)
- [Slack MCP with LangGraph Python](docs/app-recipes.md#slack-mcp-with-langgraph-python)
- [GitHub MCP with LangGraph Python](docs/app-recipes.md#github-mcp-with-langgraph-python)
- [Jira Cloud MCP with LangGraph Python](docs/app-recipes.md#jira-cloud-mcp-with-langgraph-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Uses the LangChain MCP adapter to bind server-discovered tools into a LangGraph ReAct workflow. Configure Weavz in Tool Mode or Code Mode first; local `--mode` validates the expected names and cannot switch a live server.

Requires Python 3.11 or 3.12, uv, a custom MCP URL, and its MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

The independent fixture is a real bearer-protected MCP SDK server with synthetic data. It requires no model. Copy `.env.example` to `.env`; use `uv run --env-file .env python main.py --mode tools` or `--mode code` to inspect live tools. For an optional model run, connect an app containing the data needed for your prompt, set `WEAVZ_MODEL` and `OPENAI_API_KEY`, and pass `--prompt`. LangGraph executes the MCP-backed graph while the tools remain attached.
