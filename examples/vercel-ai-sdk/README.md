# Vercel AI SDK MCP integration examples with Weavz

<!-- weavz:discovery:start -->

Connect Vercel AI SDK to Slack, Gmail, HubSpot and GitHub through a remote Weavz Model Context Protocol (MCP) server. Use the native MCP adapter, then try the app setup recipes with your configured connections.

App setup recipes:

- [Slack MCP with Vercel AI SDK TypeScript](docs/app-recipes.md#slack-mcp-with-vercel-ai-sdk-typescript)
- [Gmail MCP with Vercel AI SDK TypeScript](docs/app-recipes.md#gmail-mcp-with-vercel-ai-sdk-typescript)
- [HubSpot MCP with Vercel AI SDK TypeScript](docs/app-recipes.md#hubspot-mcp-with-vercel-ai-sdk-typescript)
- [GitHub MCP with Vercel AI SDK TypeScript](docs/app-recipes.md#github-mcp-with-vercel-ai-sdk-typescript)

The framework consumes app tools from your configured Weavz MCP server. App recipes require your own app connections; automated checks use synthetic records.

[MCP app and framework directory](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [All examples](https://github.com/weavz/mcp-examples) · [Weavz MCP guide](https://weavz.io/docs/guides/agent-framework-examples)

<!-- weavz:discovery:end -->

Vercel AI SDK `createMCPClient` exposes Weavz remote MCP tools to a reusable `ToolLoopAgent`. The local fixture exercises both Tool Mode and Code Mode without an inference provider.

## Requirements

- Node.js 22 or newer
- A custom Weavz MCP endpoint and MCP access token for live use
- OpenAI provider credentials and a model identifier only for a live agent run

## Install and check

```sh
npm ci
npm run build
npm test
```

Run either local MCP fixture mode without provider credentials:

```sh
npm run smoke -- --fixture --mode tools
npm run smoke -- --fixture --mode code
```

The fixture binds to loopback, requires a fake bearer token, and serves one synthetic record. Tool Mode exposes `demo__lookup_record`. Code Mode exposes `weavz_search`, `weavz_read_api`, and `weavz_execute`; the execute fixture accepts only the documented lookup snippet. The fixed execute input is `return await weavz.demo.lookup_record({recordId: "record-1"});`. These checks establish local framework-adapter interoperability. They do not prove a live Weavz connection or a model-provider run.

## Connect a custom MCP server

Copy `.env.example` to `.env` and set `WEAVZ_MCP_URL` and `WEAVZ_MCP_TOKEN` from your custom MCP setup. The token is an MCP access token, not a Weavz REST API key. Do not commit `.env`.

Without a prompt, the app uses Vercel AI SDK's MCP adapter to list the tools advertised by the server, then closes the connection:

```sh
npm start
```

For an agent run, also set the provider key and model identifier shown in `.env.example`, then pass a prompt:

```sh
npm start -- --prompt "Summarize the data available through the MCP tools"
```

The endpoint's server configuration determines whether it advertises Tool Mode or Code Mode. The fixture's `--mode` option only chooses a local test catalog; it does not switch a live server.

The hosted Weavz personal MCP resource at `/mcp/weavz` uses OAuth. This starter's bearer-token setup is for a custom endpoint and does not configure that hosted resource.

## Framework entry points

- Adapter: `@ai-sdk/mcp` (`createMCPClient`)
- Live agent: `src/index.ts`
- Local authenticated server fixture: `test/fixture.ts`
