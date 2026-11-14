"""Generate the public directory from the reviewed example catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text())
sections = []
for category, title in [("framework", "Build with your framework"), ("client", "Connect your AI client"), ("workflow", "Start with a task")]:
    rows = [f"| [{entry['title']}](https://github.com/{catalog['organization']}/{entry['repository']}) | {entry['language']} | {', '.join(entry.get('integrations', [])) or entry['framework']} |" for entry in catalog["examples"] if entry["category"] == category]
    sections.append(f"## {title}\n\n| Example | Language | Framework or apps |\n| --- | --- | --- |\n" + "\n".join(rows))
(ROOT / "README.md").write_text('''# Weavz MCP examples

Give your agent access to the apps people use. Choose your framework, connect an AI client, or start with a practical read-only workflow.

Weavz manages app connections and exposes their tools over MCP. These examples use the framework or client's native MCP adapter, so app access stays separate from your model provider and agent logic.

## Choose your path

- **Use your existing AI:** open a client example and connect the hosted Weavz MCP resource with OAuth. Sign in and choose the intended workspace; no backend API key is needed in the client.
- **Build an agent:** choose a framework starter. Its custom MCP endpoint uses an end-user MCP access token from your trusted backend. The local fixture runs without a Weavz account or paid model.
- **Solve a task:** choose a workflow. It adds task instructions, scoped inputs, a typed report, source references, and tests in both MCP modes.

**Tool Mode** exposes app actions as individual MCP tools. **Code Mode** lets the agent discover apps, inspect APIs, and compose related calls with JavaScript through MCP. Set the mode on the server; a client flag does not change it.

''' + "\n\n".join(sections) + '''

## Custom server setup

For framework examples, configure app access in an existing Weavz workspace. Run setup only on a trusted backend using a customer API key; agents receive a separate MCP access token.

```sh
uv sync --locked
# Set WEAVZ_API_KEY locally; never paste it into an agent prompt.
uv run python tools/setup_weavz.py \\
  --workspace-id 00000000-0000-4000-8000-000000000001 \\
  --end-user-id example-user --mode code
```

Replace the UUID and external user ID with your chosen workspace and trusted application identity. The helper creates the end user if missing and a restricted server, then issues a one-hour MCP token. It adds no app integrations or app credentials. Add `--server-id <server-uuid>` to reuse a matching bearer-enabled server. It checks workspace, mode, and attached end user before issuing a token and never changes an existing server's mode.

The helper saves `.env.weavz` with owner-only permissions and refuses to overwrite an existing file. Use a dotenv loader such as `uv run --env-file .env.weavz ...`; **do not shell-source this file**. Copy its MCP settings into the selected example's local environment. Configure model credentials separately. If a network error interrupts setup, inspect the created server ID before retrying; no resources are automatically deleted.

## What the checks establish

Framework starters and workflows test native MCP adapters against authenticated, synthetic local servers. Workflow tests run a real agent loop with a deterministic local model. Client examples test configuration and instructions; OpenCode also has a native CLI discovery check. Other client checks do not establish live OAuth compatibility.

An OpenCode 1.17.6 agent using DeepSeek Flash additionally exercised a local MCP tool and ran a PydanticAI workflow's installation, tests, and both fixture modes. These checks use synthetic data and do not establish live connected-app access. See [verification](docs/verification.md) for the measured scope.

For live use, select your actual account, connect the needed apps, configure a model, and run the README's live command. Never pass a `wvz_` customer API key as an MCP execution token. Treat retrieved app content as data, respect approval decisions, and review consequential actions before execution.

## Contribute

Each repository is independently installable and has its own CI and dependency locks where dependencies are needed. Sources are maintained together in this hub and published as focused repositories. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing an example.

[Weavz](https://weavz.io) · [Docs](https://weavz.io/docs) · [Tool Mode](https://weavz.io/docs/guides/mcp-tool-mode) · [Code Mode](https://weavz.io/docs/guides/mcp-code-mode) · [Connect your AI](https://weavz.io/docs/guides/weavz-mcp-app)

Example code is MIT licensed. Connected apps, models, and Weavz accounts keep their own terms. See [LICENSE](LICENSE).
''')
