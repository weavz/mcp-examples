# Working with these examples

Use the example README for its supported runtime, install command, and test command. Keep each example independently installable and locked.

## App access

- Expose Weavz tools through the framework or client's MCP adapter. Keep the connection open until its tools finish and close it afterward.
- Tool Mode and Code Mode are server settings. A client flag cannot change a remote server's mode. Inspect the advertised tools before using them.
- Customer REST setup uses a Weavz API key on a trusted backend. MCP execution uses the selected MCP server's authentication. Do not substitute a customer API key for an MCP access token.
- Hosted personal-client setup uses OAuth at `https://platform.weavz.io/mcp/weavz`. Custom framework servers use the endpoint returned by their setup.
- Discover current tool schemas and executable aliases. Do not invent app actions or use display names as executable aliases.
- Follow the user's requested scope. Ask before an unrequested external write, message, or destructive operation. Respect pending, rejected, or expired approvals.

## Credentials and tests

- Keep credentials in local environment variables or the client's credential store. Never commit them, print them, or ask users to paste them into chat.
- Run local fixture checks first. Fixture results use synthetic records and are separate from live Weavz, connected-app, and model-provider proof.
- Do not change global client configuration to run an example. Use documented project settings or an isolated client profile.
- Keep dependencies pinned and test the framework's actual adapter. A raw HTTP replacement does not verify framework integration.
- Update the relevant README when commands, configuration, or behavior changes.
