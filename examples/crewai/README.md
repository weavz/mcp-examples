# CrewAI + Weavz MCP

Uses CrewAI's native `MCPServerHTTP` configuration and `Agent.get_mcp_tools`. CrewAI prefixes tool names internally; the example reports and calls their original MCP names. Configure a custom Weavz MCP server in Tools Mode or Code Mode first; `--mode` checks its actual tools and cannot switch a live server.

Requires Python 3.11 or 3.12, uv, a custom Streamable HTTP URL and MCP access token. Do not use a Weavz REST API key. The personal `/mcp/weavz` connector uses OAuth.

```sh
uv sync --locked
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
uv run pytest
```

Fixture proof uses a separate bearer-protected MCP SDK server with synthetic records, no model, and no live Weavz account. Copy `.env.example` to `.env` and run `uv run --env-file .env python main.py --mode tools` or `--mode code` for live discovery. For an optional CrewAI run, connect an app containing task data, set `WEAVZ_MODEL` to a model identifier supported by your provider and `OPENAI_API_KEY`, then add `--prompt "Summarize the records relevant to my current task"`.

CrewAI 1.15's native resolver opens a connection for tool discovery and makes a new managed connection for each tool invocation. That is the framework's lifecycle; this example does not keep one session open across the full run.
