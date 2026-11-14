# Weavz MCP with Claude Code

Connect an AI coding client to the apps authorized in one Weavz workspace through remote MCP. This example keeps client MCP configuration separate from the model provider and from project instructions.

## Requirements

- A current Claude Code CLI with remote HTTP MCP support.
- A reachable Weavz platform endpoint and a Weavz account.
- A model/provider configured in your client. Weavz OAuth does not configure or pay for model access.

See the official [Claude Code MCP guide](https://code.claude.com/docs/en/mcp) for project scope, OAuth, and CLI details.

## Setup

Claude Code project MCP servers live in `.mcp.json`; `CLAUDE.md` is the native project instruction file. The project server may require explicit approval in Claude Code. OAuth tokens remain in Claude Code credential storage, not this repository.

```sh
# The credential-free project config is checked in at .mcp.json.
claude mcp get weavz
claude mcp login weavz
```

If adding Weavz to another project, use `claude mcp add --transport http weavz --scope project https://platform.weavz.io/mcp/weavz` so Claude Code writes `.mcp.json` instead of user/global config. Review and approve the project server when Claude Code prompts.

Complete the browser sign-in, select the intended workspace, and approve the connector. The OAuth flow stores credentials in the client's own credential store. Do not add an `Authorization` header or paste a Weavz access token for the hosted personal connector.

For self-hosted Weavz, replace `https://platform.weavz.io/mcp/weavz` with `https://<your-public-weavz-host>/mcp/weavz`. The server must be reachable over HTTPS from the client.

## Verify

```sh
claude mcp get weavz
claude -p --output-format json "Use a Weavz read/search tool to confirm access. Do not modify anything."
```

`claude mcp get weavz` shows the configured entry; the one-shot prompt is the model-mediated check. Count it as passed only if the transcript shows a Weavz tool call and result. Review tool arguments and output. Do not infer live auth or a successful app action from configuration files alone.

## Project instructions

This repo includes `CLAUDE.md` guidance. It does not install or configure MCP. See the client-native instruction file for rules loaded into the agent.

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
