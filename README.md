# Weavz MCP examples

Give your agent access to the apps people use. Choose your framework, connect an AI client, or start with a practical read-only workflow.

Weavz manages app connections and exposes their tools over MCP. These examples use the framework or client's native MCP adapter, so app access stays separate from your model provider and agent logic.

## Choose your path

- **Use your existing AI:** open a client example and connect the hosted Weavz MCP resource with OAuth. Sign in and choose the intended workspace; no backend API key is needed in the client.
- **Build an agent:** choose a framework starter. Its custom MCP endpoint uses an end-user MCP access token from your trusted backend. The local fixture runs without a Weavz account or paid model.
- **Solve a task:** choose a workflow. It adds task instructions, scoped inputs, a typed report, source references, and tests in both MCP modes.

**Tool Mode** exposes app actions as individual MCP tools. **Code Mode** lets the agent discover apps, inspect APIs, and compose related calls with JavaScript through MCP. Set the mode on the server; a client flag does not change it.

## Build with your framework

| Example | Language | Framework or apps |
| --- | --- | --- |
| [OpenAI Agents SDK with Weavz MCP](https://github.com/weavz/weavz-openai-agents-python) | python | OpenAI Agents SDK |
| [PydanticAI with Weavz MCP](https://github.com/weavz/weavz-pydantic-ai) | python | PydanticAI |
| [Google ADK with Weavz MCP](https://github.com/weavz/weavz-google-adk-python) | python | Google ADK |
| [LangChain with Weavz MCP](https://github.com/weavz/weavz-langchain-python) | python | LangChain |
| [LangGraph with Weavz MCP](https://github.com/weavz/weavz-langgraph-python) | python | LangGraph |
| [LlamaIndex with Weavz MCP](https://github.com/weavz/weavz-llamaindex) | python | LlamaIndex |
| [CrewAI with Weavz MCP](https://github.com/weavz/weavz-crewai) | python | CrewAI |
| [Agno with Weavz MCP](https://github.com/weavz/weavz-agno) | python | Agno |
| [Strands Agents with Weavz MCP](https://github.com/weavz/weavz-strands) | python | Strands Agents |
| [smolagents with Weavz MCP](https://github.com/weavz/weavz-smolagents) | python | smolagents |
| [AutoGen with Weavz MCP](https://github.com/weavz/weavz-autogen) | python | AutoGen |
| [Semantic Kernel with Weavz MCP](https://github.com/weavz/weavz-semantic-kernel) | python | Semantic Kernel |
| [Vercel AI SDK with Weavz MCP](https://github.com/weavz/weavz-vercel-ai-sdk) | typescript | Vercel AI SDK |
| [Mastra with Weavz MCP](https://github.com/weavz/weavz-mastra) | typescript | Mastra |
| [LangChain.js with Weavz MCP](https://github.com/weavz/weavz-langchain-js) | typescript | LangChain.js |
| [LangGraph.js with Weavz MCP](https://github.com/weavz/weavz-langgraph-js) | typescript | LangGraph.js |
| [OpenAI Agents SDK for TypeScript with Weavz MCP](https://github.com/weavz/weavz-openai-agents-js) | typescript | OpenAI Agents SDK for TypeScript |
| [Google ADK for TypeScript with Weavz MCP](https://github.com/weavz/weavz-google-adk-js) | typescript | Google ADK for TypeScript |

## Connect your AI client

| Example | Language | Framework or apps |
| --- | --- | --- |
| [Weavz for OpenCode](https://github.com/weavz/weavz-opencode) | configuration | OpenCode |
| [Weavz for Hermes Agent](https://github.com/weavz/weavz-hermes) | configuration | Hermes Agent |
| [Weavz for OpenClaw](https://github.com/weavz/weavz-openclaw) | configuration | OpenClaw |
| [Weavz for Pi](https://github.com/weavz/weavz-pi) | configuration | Pi |
| [Weavz for Claude Code](https://github.com/weavz/weavz-claude-code) | configuration | Claude Code |
| [Weavz for Codex](https://github.com/weavz/weavz-codex) | configuration | Codex |
| [Weavz for Cursor](https://github.com/weavz/weavz-cursor) | configuration | Cursor |

## Start with a task

| Example | Language | Framework or apps |
| --- | --- | --- |
| [Morning Brief](https://github.com/weavz/weavz-morning-brief) | python | gmail, google-calendar |
| [Gmail Inbox Briefing](https://github.com/weavz/weavz-gmail-inbox-briefing) | python | gmail |
| [Meeting Preparation](https://github.com/weavz/weavz-meeting-prep) | python | google-calendar, gmail |
| [Slack Channel Digest](https://github.com/weavz/weavz-slack-channel-digest) | python | slack |
| [GitHub Issue Triage](https://github.com/weavz/weavz-github-issue-triage) | python | github |
| [Notion Knowledge Research](https://github.com/weavz/weavz-notion-knowledge-research) | python | notion |
| [Google Drive Document Finder](https://github.com/weavz/weavz-drive-document-finder) | python | google-drive |
| [Google Sheets Sales Report](https://github.com/weavz/weavz-sheets-sales-report) | python | google-sheets |
| [HubSpot Pipeline Review](https://github.com/weavz/weavz-hubspot-pipeline-review) | python | hubspot |
| [Salesforce Account Brief](https://github.com/weavz/weavz-salesforce-account-brief) | python | salesforce |
| [Linear Backlog Review](https://github.com/weavz/weavz-linear-backlog-review) | python | linear |
| [Jira Sprint Summary](https://github.com/weavz/weavz-jira-sprint-summary) | python | jira-cloud |
| [Zendesk Ticket Handoff](https://github.com/weavz/weavz-zendesk-ticket-handoff) | python | zendesk |
| [Intercom Conversation Brief](https://github.com/weavz/weavz-intercom-conversation-brief) | python | intercom |
| [Airtable Inventory Report](https://github.com/weavz/weavz-airtable-inventory-report) | python | airtable |
| [Trello Project Health](https://github.com/weavz/weavz-trello-project-health) | python | trello |
| [Asana Weekly Status](https://github.com/weavz/weavz-asana-weekly-status) | python | asana |
| [Figma Design Review](https://github.com/weavz/weavz-figma-design-review) | python | figma |
| [Stripe Subscription Review](https://github.com/weavz/weavz-stripe-subscription-review) | python | stripe |
| [Shopify Orders Report](https://github.com/weavz/weavz-shopify-orders-report) | python | shopify |
| [Support Knowledge Assistant](https://github.com/weavz/weavz-support-knowledge-assistant) | python | gmail, notion |
| [Files Research Notebook](https://github.com/weavz/weavz-files-research-notebook) | python | storage |
| [Todoist Day Plan](https://github.com/weavz/weavz-todoist-day-plan) | python | todoist |
| [Google Docs Document Review](https://github.com/weavz/weavz-google-docs-document-review) | python | google-docs |
| [GitHub Pull Request Review](https://github.com/weavz/weavz-github-pull-request-review) | python | github |

## Custom server setup

For framework examples, configure app access in an existing Weavz workspace. Run setup only on a trusted backend using a customer API key; agents receive a separate MCP access token.

```sh
uv sync --locked
# Set WEAVZ_API_KEY locally; never paste it into an agent prompt.
uv run python tools/setup_weavz.py \
  --workspace-id 00000000-0000-4000-8000-000000000001 \
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
