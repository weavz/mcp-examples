# Weavz MCP with Pi

Connect an AI coding client to the apps authorized in one Weavz workspace through remote MCP. This example keeps client MCP configuration separate from the model provider and from project instructions.

## Requirements

- A current Pi CLI or desktop client with remote Streamable HTTP MCP support.
- A reachable Weavz platform endpoint and a Weavz account.
- A model/provider configured in the isolated Pi agent directory. `PI_CODING_AGENT_DIR` starts separate config and auth state, so it will not inherit settings from `~/.pi/agent`. Weavz OAuth does not configure or pay for model access.

See the official [Pi MCP guide](https://docs.pi.dev/latest/mcp) for project trust, supported transports, and OAuth details.

## Setup

Pi project MCP servers live in `.pi/mcp.json` and are loaded only after the project is trusted. `AGENTS.md` and `.pi/APPEND_SYSTEM.md` are project instructions, separate from server setup. This example sets `PI_CODING_AGENT_DIR` to ignored `.local/pi`, so its personal MCP config and OAuth state are isolated from `~/.pi/agent`.

```sh
# Project config is checked in; isolate Pi's user config and OAuth state.
export PI_CODING_AGENT_DIR="$PWD/.local/pi"
pi mcp login weavz
```

Complete the browser sign-in, select the intended workspace, and approve the connector. The OAuth flow stores credentials in the client's own credential store. Do not add an `Authorization` header or paste a Weavz access token for the hosted personal connector.

For self-hosted Weavz, replace `https://platform.weavz.io/mcp/weavz` with `https://<your-public-weavz-host>/mcp/weavz`. The server must be reachable over HTTPS from the client.

## Verify

```sh
PI_CODING_AGENT_DIR="$PWD/.local/pi" pi --approve --print "Use a Weavz read/search tool to confirm access. Do not modify anything."
```

The one-shot prompt is the model-mediated check: count it as passed only if the transcript shows a Weavz tool call and result. Review tool arguments and output. Do not infer live auth or a successful app action from configuration files alone.

## Project instructions

This repo includes `AGENTS.md` guidance. It does not install or configure MCP. See the client-native instruction file for rules loaded into the agent.

## Local checks

Run the dependency-free static contract checks:

```sh
python3 -m unittest discover -s tests -v
```

These check the checked-in client config and instruction/setup contract only; they make no network calls and do not prove OAuth or tool execution.

## Credentials and safety

- Keep OAuth in the client credential store. No Weavz API key, MCP access token, connected-app secret, or model key belongs in this repo.
- The endpoint scopes the connector to the workspace selected during Weavz sign-in. To change workspaces, disconnect and reauthorize.
- Tool availability follows that workspace's configuration and permissions. This example does not promise MCP App UI support.
- Before writing, sending, publishing, deleting, or changing external data, inspect the proposed action and obtain user approval.

## License

MIT. See [LICENSE](LICENSE).
