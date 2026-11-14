# Semantic Kernel MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect Semantic Kernel to Salesforce, Jira Cloud, Google Drive and Slack through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Salesforce MCP with Semantic Kernel Python](docs/app-recipes.md#salesforce-mcp-with-semantic-kernel-python)
- [Jira Cloud MCP with Semantic Kernel Python](docs/app-recipes.md#jira-cloud-mcp-with-semantic-kernel-python)
- [Google Drive MCP with Semantic Kernel Python](docs/app-recipes.md#google-drive-mcp-with-semantic-kernel-python)
- [Slack MCP with Semantic Kernel Python](docs/app-recipes.md#slack-mcp-with-semantic-kernel-python)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Connects Semantic Kernel's native `MCPStreamableHttpPlugin` to a Streamable HTTP endpoint. Configure a custom Weavz MCP server in Tools Mode or Code Mode first; `--mode` verifies the live tools and does not change server configuration. The personal `/mcp/weavz` connector uses OAuth and does not accept an arbitrary MCP bearer token.

Requires Python 3.11 or 3.12 and uv. `WEAVZ_MCP_TOKEN` must be a Weavz MCP access token, not a REST API key.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

Fixture checks use a separate bearer-protected local MCP SDK server and synthetic data; no model call or live Weavz account is involved. For live discovery, copy `.env.example` to `.env` and run `uv run --env-file .env python main.py --mode tools` or `--mode code`. For an optional Semantic Kernel agent run, connect an app that has task-relevant data, set `WEAVZ_MODEL` to a model identifier available to your OpenAI account and `OPENAI_API_KEY`, then add `--prompt "Summarize the records relevant to my current task"`.
