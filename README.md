# MCP integration examples for AI agent frameworks

Give your agent access to the apps people use. Choose your framework, connect an AI client, or start with a practical read-only workflow.

Weavz manages app connections and exposes their tools over MCP. These examples use the framework or client's native MCP adapter, so app access stays separate from your model provider and agent logic.

Connect Slack, Gmail, GitHub, Notion, Google Sheets and other apps to LangChain, LangGraph, Mastra, Google ADK, PydanticAI, OpenAI Agents SDK and more. Browse the [app and framework directory](docs/integrations.md) for specific combinations such as Slack MCP with LangChain or Gmail MCP with Google ADK. The [machine-readable example index](examples-index.json) includes framework, language, authentication, app recipes, and verification scope for each project.

## Choose your path

- **Use your existing AI:** open a client example and connect the hosted Weavz MCP resource with OAuth. Sign in and choose the intended workspace; no backend API key is needed in the client.
- **Build an agent:** choose a framework starter. Its custom MCP endpoint uses an end-user MCP access token from your trusted backend. The local fixture runs without a Weavz account or paid model.
- **Solve a task:** choose a workflow. It adds task instructions, scoped inputs, a typed report, source references, and tests in both MCP modes.

**Tool Mode** exposes app actions as individual MCP tools. **Code Mode** lets the agent discover apps, inspect APIs, and compose related calls with JavaScript through MCP. Set the mode on the server; a client flag does not change it.

## Build with your framework

| Example | Language | Framework or apps |
| --- | --- | --- |
| [OpenAI Agents SDK (Python) MCP integration examples with Weavz](https://github.com/weavz/weavz-openai-agents-python) | python | Slack, Gmail, GitHub, Notion |
| [PydanticAI MCP integration examples with Weavz](https://github.com/weavz/weavz-pydantic-ai) | python | Gmail, Google Sheets, Notion, Figma |
| [Google ADK (Python) MCP integration examples with Weavz](https://github.com/weavz/weavz-google-adk-python) | python | Gmail, Google Calendar, Google Drive, Google Sheets |
| [LangChain (Python) MCP integration examples with Weavz](https://github.com/weavz/weavz-langchain-python) | python | Slack, Gmail, Notion, GitHub |
| [LangGraph (Python) MCP integration examples with Weavz](https://github.com/weavz/weavz-langgraph-python) | python | Gmail, Slack, GitHub, Jira Cloud |
| [LlamaIndex MCP integration examples with Weavz](https://github.com/weavz/weavz-llamaindex) | python | Notion, Google Drive, Google Docs, Google Sheets |
| [CrewAI MCP integration examples with Weavz](https://github.com/weavz/weavz-crewai) | python | HubSpot, Gmail, Google Calendar, Slack |
| [Agno MCP integration examples with Weavz](https://github.com/weavz/weavz-agno) | python | Slack, GitHub, Figma, HubSpot |
| [Strands Agents MCP integration examples with Weavz](https://github.com/weavz/weavz-strands) | python | Slack, Gmail, GitHub, Google Calendar |
| [smolagents MCP integration examples with Weavz](https://github.com/weavz/weavz-smolagents) | python | GitHub, Figma, Google Sheets, Gmail |
| [AutoGen MCP integration examples with Weavz](https://github.com/weavz/weavz-autogen) | python | GitHub, Slack, Jira Cloud, Gmail |
| [Semantic Kernel MCP integration examples with Weavz](https://github.com/weavz/weavz-semantic-kernel) | python | Salesforce, Jira Cloud, Google Drive, Slack |
| [Vercel AI SDK MCP integration examples with Weavz](https://github.com/weavz/weavz-vercel-ai-sdk) | typescript | Slack, Gmail, HubSpot, GitHub |
| [Mastra MCP integration examples with Weavz](https://github.com/weavz/weavz-mastra) | typescript | GitHub, Slack, Notion, Gmail |
| [LangChain.js (TypeScript) MCP integration examples with Weavz](https://github.com/weavz/weavz-langchain-js) | typescript | Slack, Gmail, Notion, GitHub |
| [LangGraph.js (TypeScript) MCP integration examples with Weavz](https://github.com/weavz/weavz-langgraph-js) | typescript | GitHub, Slack, Zendesk, Gmail |
| [OpenAI Agents SDK for TypeScript MCP integration examples with Weavz](https://github.com/weavz/weavz-openai-agents-js) | typescript | Gmail, Slack, GitHub, Notion |
| [Google ADK for TypeScript MCP integration examples with Weavz](https://github.com/weavz/weavz-google-adk-js) | typescript | Gmail, Google Calendar, Google Sheets, Google Drive |

## Connect your AI client

| Example | Language | Framework or apps |
| --- | --- | --- |
| [OpenCode MCP setup for Weavz app integrations](https://github.com/weavz/weavz-opencode) | configuration | Slack, Gmail, GitHub, Notion |
| [Hermes Agent MCP setup for Weavz app integrations](https://github.com/weavz/weavz-hermes) | configuration | Slack, Gmail, GitHub, Notion |
| [OpenClaw MCP setup for Weavz app integrations](https://github.com/weavz/weavz-openclaw) | configuration | Slack, Gmail, GitHub, Notion |
| [Pi MCP setup for Weavz app integrations](https://github.com/weavz/weavz-pi) | configuration | Slack, Gmail, GitHub, Notion |
| [Claude Code MCP setup for Weavz app integrations](https://github.com/weavz/weavz-claude-code) | configuration | Slack, Gmail, GitHub, Notion |
| [Codex MCP setup for Weavz app integrations](https://github.com/weavz/weavz-codex) | configuration | Slack, Gmail, GitHub, Notion |
| [Cursor MCP setup for Weavz app integrations](https://github.com/weavz/weavz-cursor) | configuration | Slack, Gmail, GitHub, Notion |

## Start with a task

| Example | Language | Framework or apps |
| --- | --- | --- |
| [Gmail and Google Calendar MCP agent with PydanticAI: Morning Brief](https://github.com/weavz/weavz-morning-brief) | python | Gmail, Google Calendar |
| [Gmail MCP agent with PydanticAI: Gmail Inbox Briefing](https://github.com/weavz/weavz-gmail-inbox-briefing) | python | Gmail |
| [Google Calendar and Gmail MCP agent with PydanticAI: Meeting Preparation](https://github.com/weavz/weavz-meeting-prep) | python | Google Calendar, Gmail |
| [Slack MCP agent with PydanticAI: Slack Channel Digest](https://github.com/weavz/weavz-slack-channel-digest) | python | Slack |
| [GitHub MCP agent with PydanticAI: GitHub Issue Triage](https://github.com/weavz/weavz-github-issue-triage) | python | GitHub |
| [Notion MCP agent with PydanticAI: Notion Knowledge Research](https://github.com/weavz/weavz-notion-knowledge-research) | python | Notion |
| [Google Drive MCP agent with PydanticAI: Google Drive Document Finder](https://github.com/weavz/weavz-drive-document-finder) | python | Google Drive |
| [Google Sheets MCP agent with PydanticAI: Google Sheets Sales Report](https://github.com/weavz/weavz-sheets-sales-report) | python | Google Sheets |
| [HubSpot MCP agent with PydanticAI: HubSpot Pipeline Review](https://github.com/weavz/weavz-hubspot-pipeline-review) | python | HubSpot |
| [Salesforce MCP agent with PydanticAI: Salesforce Account Brief](https://github.com/weavz/weavz-salesforce-account-brief) | python | Salesforce |
| [Linear MCP agent with PydanticAI: Linear Backlog Review](https://github.com/weavz/weavz-linear-backlog-review) | python | Linear |
| [Jira Cloud MCP agent with PydanticAI: Jira Cloud Sprint Summary](https://github.com/weavz/weavz-jira-sprint-summary) | python | Jira Cloud |
| [Zendesk MCP agent with PydanticAI: Zendesk Ticket Handoff](https://github.com/weavz/weavz-zendesk-ticket-handoff) | python | Zendesk |
| [Intercom MCP agent with PydanticAI: Intercom Conversation Brief](https://github.com/weavz/weavz-intercom-conversation-brief) | python | Intercom |
| [Airtable MCP agent with PydanticAI: Airtable Inventory Report](https://github.com/weavz/weavz-airtable-inventory-report) | python | Airtable |
| [Trello MCP agent with PydanticAI: Trello Project Health](https://github.com/weavz/weavz-trello-project-health) | python | Trello |
| [Asana MCP agent with PydanticAI: Asana Weekly Status](https://github.com/weavz/weavz-asana-weekly-status) | python | Asana |
| [Figma MCP agent with PydanticAI: Figma Design Review](https://github.com/weavz/weavz-figma-design-review) | python | Figma |
| [Stripe MCP agent with PydanticAI: Stripe Subscription Review](https://github.com/weavz/weavz-stripe-subscription-review) | python | Stripe |
| [Shopify MCP agent with PydanticAI: Shopify Orders Report](https://github.com/weavz/weavz-shopify-orders-report) | python | Shopify |
| [Gmail and Notion MCP agent with PydanticAI: Support Knowledge Assistant](https://github.com/weavz/weavz-support-knowledge-assistant) | python | Gmail, Notion |
| [Filesystem MCP agent with PydanticAI: Files Research Notebook](https://github.com/weavz/weavz-files-research-notebook) | python | Filesystem |
| [Todoist MCP agent with PydanticAI: Todoist Day Plan](https://github.com/weavz/weavz-todoist-day-plan) | python | Todoist |
| [Google Docs MCP agent with PydanticAI: Google Docs Document Review](https://github.com/weavz/weavz-google-docs-document-review) | python | Google Docs |
| [GitHub MCP agent with PydanticAI: GitHub Pull Request Review](https://github.com/weavz/weavz-github-pull-request-review) | python | GitHub |

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
