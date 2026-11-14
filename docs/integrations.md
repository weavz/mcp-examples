# MCP integration examples by app and agent framework

Choose the app you want an agent to use, then open a framework setup recipe or a task workflow. All app access goes through a configured Weavz MCP server using the framework's native MCP adapter.

Framework recipes are setup guides for your own app connections. PydanticAI task workflows include authenticated synthetic MCP fixtures and typed reports. Client guides use the hosted Weavz MCP resource with OAuth. See [verification scope](verification.md) for what each check establishes.

## Find an app and framework

| App | PydanticAI MCP workflow | More framework setup recipes |
| --- | --- | --- |
| [Airtable MCP](#airtable-mcp) | [Airtable Inventory Report](https://github.com/weavz/weavz-airtable-inventory-report) | Use the linked PydanticAI workflow |
| [Asana MCP](#asana-mcp) | [Asana Weekly Status](https://github.com/weavz/weavz-asana-weekly-status) | Use the linked PydanticAI workflow |
| [Figma MCP](#figma-mcp) | [Figma Design Review](https://github.com/weavz/weavz-figma-design-review) | [Figma MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#figma-mcp-with-pydanticai-python) · [Figma MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#figma-mcp-with-agno-python) · [Figma MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#figma-mcp-with-smolagents-python) |
| [Filesystem MCP](#filesystem-mcp) | [Files Research Notebook](https://github.com/weavz/weavz-files-research-notebook) | Use the linked PydanticAI workflow |
| [GitHub MCP](#github-mcp) | [GitHub Pull Request Review](https://github.com/weavz/weavz-github-pull-request-review) | [GitHub MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#github-mcp-with-openai-agents-sdk-python) · [GitHub MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#github-mcp-with-langchain-python) · [GitHub MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#github-mcp-with-langgraph-python) · [GitHub MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#github-mcp-with-agno-python) · [GitHub MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#github-mcp-with-strands-agents-python) · [All 12 setup recipes](#github-mcp) |
| [Gmail MCP](#gmail-mcp) | [Gmail Inbox Briefing](https://github.com/weavz/weavz-gmail-inbox-briefing) | [Gmail MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#gmail-mcp-with-openai-agents-sdk-python) · [Gmail MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#gmail-mcp-with-pydanticai-python) · [Gmail MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#gmail-mcp-with-google-adk-python) · [Gmail MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#gmail-mcp-with-langchain-python) · [Gmail MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#gmail-mcp-with-langgraph-python) · [All 15 setup recipes](#gmail-mcp) |
| [Google Calendar MCP](#google-calendar-mcp) | [Meeting Preparation](https://github.com/weavz/weavz-meeting-prep) | [Google Calendar MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-calendar-mcp-with-google-adk-python) · [Google Calendar MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#google-calendar-mcp-with-crewai-python) · [Google Calendar MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#google-calendar-mcp-with-strands-agents-python) · [Google Calendar MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-calendar-mcp-with-google-adk-for-typescript) |
| [Google Docs MCP](#google-docs-mcp) | [Google Docs Document Review](https://github.com/weavz/weavz-google-docs-document-review) | [Google Docs MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-docs-mcp-with-llamaindex-python) |
| [Google Drive MCP](#google-drive-mcp) | [Google Drive Document Finder](https://github.com/weavz/weavz-drive-document-finder) | [Google Drive MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-drive-mcp-with-google-adk-python) · [Google Drive MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-drive-mcp-with-llamaindex-python) · [Google Drive MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#google-drive-mcp-with-semantic-kernel-python) · [Google Drive MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-drive-mcp-with-google-adk-for-typescript) |
| [Google Sheets MCP](#google-sheets-mcp) | [Google Sheets Sales Report](https://github.com/weavz/weavz-sheets-sales-report) | [Google Sheets MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#google-sheets-mcp-with-pydanticai-python) · [Google Sheets MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-sheets-mcp-with-google-adk-python) · [Google Sheets MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-sheets-mcp-with-llamaindex-python) · [Google Sheets MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#google-sheets-mcp-with-smolagents-python) · [Google Sheets MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-sheets-mcp-with-google-adk-for-typescript) |
| [HubSpot MCP](#hubspot-mcp) | [HubSpot Pipeline Review](https://github.com/weavz/weavz-hubspot-pipeline-review) | [HubSpot MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#hubspot-mcp-with-crewai-python) · [HubSpot MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#hubspot-mcp-with-agno-python) · [HubSpot MCP with Vercel AI SDK TypeScript](https://github.com/weavz/weavz-vercel-ai-sdk/blob/main/docs/app-recipes.md#hubspot-mcp-with-vercel-ai-sdk-typescript) |
| [Intercom MCP](#intercom-mcp) | [Intercom Conversation Brief](https://github.com/weavz/weavz-intercom-conversation-brief) | Use the linked PydanticAI workflow |
| [Jira Cloud MCP](#jira-cloud-mcp) | [Jira Sprint Summary](https://github.com/weavz/weavz-jira-sprint-summary) | [Jira Cloud MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-langgraph-python) · [Jira Cloud MCP with AutoGen Python](https://github.com/weavz/weavz-autogen/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-autogen-python) · [Jira Cloud MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-semantic-kernel-python) |
| [Linear MCP](#linear-mcp) | [Linear Backlog Review](https://github.com/weavz/weavz-linear-backlog-review) | Use the linked PydanticAI workflow |
| [Notion MCP](#notion-mcp) | [Notion Knowledge Research](https://github.com/weavz/weavz-notion-knowledge-research) | [Notion MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#notion-mcp-with-openai-agents-sdk-python) · [Notion MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#notion-mcp-with-pydanticai-python) · [Notion MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#notion-mcp-with-langchain-python) · [Notion MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#notion-mcp-with-llamaindex-python) · [Notion MCP with Mastra TypeScript](https://github.com/weavz/weavz-mastra/blob/main/docs/app-recipes.md#notion-mcp-with-mastra-typescript) · [All 7 setup recipes](#notion-mcp) |
| [Salesforce MCP](#salesforce-mcp) | [Salesforce Account Brief](https://github.com/weavz/weavz-salesforce-account-brief) | [Salesforce MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#salesforce-mcp-with-semantic-kernel-python) |
| [Shopify MCP](#shopify-mcp) | [Shopify Orders Report](https://github.com/weavz/weavz-shopify-orders-report) | Use the linked PydanticAI workflow |
| [Slack MCP](#slack-mcp) | [Slack Channel Digest](https://github.com/weavz/weavz-slack-channel-digest) | [Slack MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#slack-mcp-with-openai-agents-sdk-python) · [Slack MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#slack-mcp-with-langchain-python) · [Slack MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#slack-mcp-with-langgraph-python) · [Slack MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#slack-mcp-with-crewai-python) · [Slack MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#slack-mcp-with-agno-python) · [All 13 setup recipes](#slack-mcp) |
| [Stripe MCP](#stripe-mcp) | [Stripe Subscription Review](https://github.com/weavz/weavz-stripe-subscription-review) | Use the linked PydanticAI workflow |
| [Todoist MCP](#todoist-mcp) | [Todoist Day Plan](https://github.com/weavz/weavz-todoist-day-plan) | Use the linked PydanticAI workflow |
| [Trello MCP](#trello-mcp) | [Trello Project Health](https://github.com/weavz/weavz-trello-project-health) | Use the linked PydanticAI workflow |
| [Zendesk MCP](#zendesk-mcp) | [Zendesk Ticket Handoff](https://github.com/weavz/weavz-zendesk-ticket-handoff) | [Zendesk MCP with LangGraph.js TypeScript](https://github.com/weavz/weavz-langgraph-js/blob/main/docs/app-recipes.md#zendesk-mcp-with-langgraphjs-typescript) |

## How app access works

Connect the required app for the intended Weavz end user, select a custom MCP server, and give the framework an MCP access token. Your model provider stays configured in the framework. Existing AI clients can use the hosted OAuth connector instead; see the [client setup directory](../README.md#connect-your-ai-client).

Tool Mode advertises individual app actions. Code Mode lets an agent search for apps, inspect their APIs, and compose related reads through MCP. A client flag does not change the remote server's mode.

## Airtable MCP

Find inventory rows at or below their reorder points in one selected base, table, formula filter, and result cap.

`list_records` returns records from the chosen base/table, optionally filtered by an Airtable formula and capped by `max_records`. Work from the rows actually returned and report the cap; do not treat them as the full table or assume additional pages were read.

[Weavz Airtable integration](https://weavz.io/integrations/airtable) · [PydanticAI workflow](https://github.com/weavz/weavz-airtable-inventory-report)

## Asana MCP

Review a bounded task sample from one Asana project, then inspect one selected task's details and notes.

`list_tasks` reads the named workspace/project and only the comma-separated `opt_fields` requested; this action has no page token input. `get_task` reads one exact task ID. Report absent fields as unknown and do not claim a complete project history.

[Weavz Asana integration](https://weavz.io/integrations/asana) · [PydanticAI workflow](https://github.com/weavz/weavz-asana-weekly-status)

## Figma MCP

Map a compact Figma file outline and inspect a small set of returned nodes for bounded design concerns.

`get_file_outline` returns a compact tree capped by `maxNodes` (1–200); its expansion via `parentNodeId` is caller-directed, not API pagination. `get_node_design_context` accepts 1–10 selected nodes with depth 1 or 2 and returns bounded REST properties/reference IDs, not resolved libraries, Code Connect mappings, generated code, or expiring image assets. Request assets separately only when needed.

[Weavz Figma integration](https://weavz.io/integrations/figma) · [PydanticAI workflow](https://github.com/weavz/weavz-figma-design-review)

Framework setup recipes:

- [Figma MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#figma-mcp-with-pydanticai-python)
- [Figma MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#figma-mcp-with-agno-python)
- [Figma MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#figma-mcp-with-smolagents-python)

## Filesystem MCP

List files under one storage prefix and read selected UTF-8 research notes as a cited evidence notebook.

`list_files` is filtered by `prefix` and returns paths in the current storage scope; it does not establish evidence outside that prefix. `read_file` returns the exact path's content as text or Base64 according to `outputEncoding`. Read only selected returned paths and avoid treating synthetic or user-provided notes as representative customer evidence.

[Weavz Filesystem integration](https://weavz.io/integrations/storage) · [PydanticAI workflow](https://github.com/weavz/weavz-files-research-notebook)

## GitHub MCP

Review one selected pull request and a bounded sample of its returned file patches, keeping PR review distinct from issue search.

`get_pull_request` reads one exact repository/pull-number pair. `custom_api_call` should be limited to `GET /repos/{owner}/{repo}/pulls/{number}/files` with a bounded `per_page` query; inspect only returned patches, note missing/truncated patch text, and do not paginate unless the user explicitly requests more. This is not a general codebase scan.

[Weavz GitHub integration](https://weavz.io/integrations/github) · [PydanticAI workflow](https://github.com/weavz/weavz-github-pull-request-review)

Framework setup recipes:

- [GitHub MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#github-mcp-with-openai-agents-sdk-python)
- [GitHub MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#github-mcp-with-langchain-python)
- [GitHub MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#github-mcp-with-langgraph-python)
- [GitHub MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#github-mcp-with-agno-python)
- [GitHub MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#github-mcp-with-strands-agents-python)
- [GitHub MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#github-mcp-with-smolagents-python)
- [GitHub MCP with AutoGen Python](https://github.com/weavz/weavz-autogen/blob/main/docs/app-recipes.md#github-mcp-with-autogen-python)
- [GitHub MCP with Vercel AI SDK TypeScript](https://github.com/weavz/weavz-vercel-ai-sdk/blob/main/docs/app-recipes.md#github-mcp-with-vercel-ai-sdk-typescript)
- [GitHub MCP with Mastra TypeScript](https://github.com/weavz/weavz-mastra/blob/main/docs/app-recipes.md#github-mcp-with-mastra-typescript)
- [GitHub MCP with LangChain.js TypeScript](https://github.com/weavz/weavz-langchain-js/blob/main/docs/app-recipes.md#github-mcp-with-langchainjs-typescript)
- [GitHub MCP with LangGraph.js TypeScript](https://github.com/weavz/weavz-langgraph-js/blob/main/docs/app-recipes.md#github-mcp-with-langgraphjs-typescript)
- [GitHub MCP with OpenAI Agents SDK for TypeScript](https://github.com/weavz/weavz-openai-agents-js/blob/main/docs/app-recipes.md#github-mcp-with-openai-agents-sdk-for-typescript)

## Gmail MCP

Search one bounded Gmail message page, read each selected message body, and separate explicit requests/deadlines from informational mail.

`list_messages` returns message summaries from the selected Gmail query and page; `pageToken` is available but this task should not fetch additional pages. `get_message` reads one exact message and can return full content; attachment data is URL-safe Base64 and is not automatically interpreted. Cite only messages actually read.

[Weavz Gmail integration](https://weavz.io/integrations/gmail) · [PydanticAI workflow](https://github.com/weavz/weavz-gmail-inbox-briefing)

Framework setup recipes:

- [Gmail MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#gmail-mcp-with-openai-agents-sdk-python)
- [Gmail MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#gmail-mcp-with-pydanticai-python)
- [Gmail MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#gmail-mcp-with-google-adk-python)
- [Gmail MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#gmail-mcp-with-langchain-python)
- [Gmail MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#gmail-mcp-with-langgraph-python)
- [Gmail MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#gmail-mcp-with-crewai-python)
- [Gmail MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#gmail-mcp-with-strands-agents-python)
- [Gmail MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#gmail-mcp-with-smolagents-python)
- [Gmail MCP with AutoGen Python](https://github.com/weavz/weavz-autogen/blob/main/docs/app-recipes.md#gmail-mcp-with-autogen-python)
- [Gmail MCP with Vercel AI SDK TypeScript](https://github.com/weavz/weavz-vercel-ai-sdk/blob/main/docs/app-recipes.md#gmail-mcp-with-vercel-ai-sdk-typescript)
- [Gmail MCP with Mastra TypeScript](https://github.com/weavz/weavz-mastra/blob/main/docs/app-recipes.md#gmail-mcp-with-mastra-typescript)
- [Gmail MCP with LangChain.js TypeScript](https://github.com/weavz/weavz-langchain-js/blob/main/docs/app-recipes.md#gmail-mcp-with-langchainjs-typescript)
- [Gmail MCP with LangGraph.js TypeScript](https://github.com/weavz/weavz-langgraph-js/blob/main/docs/app-recipes.md#gmail-mcp-with-langgraphjs-typescript)
- [Gmail MCP with OpenAI Agents SDK for TypeScript](https://github.com/weavz/weavz-openai-agents-js/blob/main/docs/app-recipes.md#gmail-mcp-with-openai-agents-sdk-for-typescript)
- [Gmail MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#gmail-mcp-with-google-adk-for-typescript)

## Google Calendar MCP

Prepare one meeting briefing from a selected calendar event and a bounded related Gmail sample.

`list_events` is restricted by `calendarId`, time bounds, and `maxResults`; it may return a `pageToken`, but this task uses only the requested bounded page. `get_event` reads one exact event ID on that calendar. This recipe reads calendar event data only; related email requires a separate Gmail connection and task scope.

[Weavz Google Calendar integration](https://weavz.io/integrations/google-calendar) · [PydanticAI workflow](https://github.com/weavz/weavz-meeting-prep)

Framework setup recipes:

- [Google Calendar MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-calendar-mcp-with-google-adk-python)
- [Google Calendar MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#google-calendar-mcp-with-crewai-python)
- [Google Calendar MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#google-calendar-mcp-with-strands-agents-python)
- [Google Calendar MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-calendar-mcp-with-google-adk-for-typescript)

## Google Docs MCP

Review one exact Google Doc's returned content for decisions, open questions, dates, and named owners.

`get_document` returns content and metadata for one exact document ID. The tool does not imply that linked documents, comments, or external attachments were read. Base claims only on returned document content and cite the selected document/sections when identifiers are present.

[Weavz Google Docs integration](https://weavz.io/integrations/google-docs) · [PydanticAI workflow](https://github.com/weavz/weavz-google-docs-document-review)

Framework setup recipes:

- [Google Docs MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-docs-mcp-with-llamaindex-python)

## Google Drive MCP

Search a bounded Google Drive result page, then verify one selected file's metadata.

`search_files` returns a result page controlled by `pageSize` and `pageToken`; it is search metadata, not document content. `get_file` fetches metadata for one exact `fileId`. Use only the requested page and state when a file body was not read.

[Weavz Google Drive integration](https://weavz.io/integrations/google-drive) · [PydanticAI workflow](https://github.com/weavz/weavz-drive-document-finder)

Framework setup recipes:

- [Google Drive MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-drive-mcp-with-google-adk-python)
- [Google Drive MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-drive-mcp-with-llamaindex-python)
- [Google Drive MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#google-drive-mcp-with-semantic-kernel-python)
- [Google Drive MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-drive-mcp-with-google-adk-for-typescript)

## Google Sheets MCP

Locate a spreadsheet, read one explicit A1 range by its actual spreadsheet ID, and separate closed-won rows from open pipeline.

`list_spreadsheets` returns a searchable file page; `read_range` reads only the exact `spreadsheetId` and A1 `range`. Values are returned as a matrix in the requested `majorDimension` and rendering mode; no cells outside that range are included. Keep closed-won and open values separate and do not treat the sample as an account-wide total.

[Weavz Google Sheets integration](https://weavz.io/integrations/google-sheets) · [PydanticAI workflow](https://github.com/weavz/weavz-sheets-sales-report)

Framework setup recipes:

- [Google Sheets MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#google-sheets-mcp-with-pydanticai-python)
- [Google Sheets MCP with Google ADK Python](https://github.com/weavz/weavz-google-adk-python/blob/main/docs/app-recipes.md#google-sheets-mcp-with-google-adk-python)
- [Google Sheets MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#google-sheets-mcp-with-llamaindex-python)
- [Google Sheets MCP with smolagents Python](https://github.com/weavz/weavz-smolagents/blob/main/docs/app-recipes.md#google-sheets-mcp-with-smolagents-python)
- [Google Sheets MCP with Google ADK for TypeScript](https://github.com/weavz/weavz-google-adk-js/blob/main/docs/app-recipes.md#google-sheets-mcp-with-google-adk-for-typescript)

## HubSpot MCP

Review the first bounded page of HubSpot deals using only selected stage, amount, pipeline, and close-date properties.

`list_deals` returns structured deal properties for the requested `limit`, `properties`, and optional page cursor (`after`). This task reads one page only. The data is deal state, not a complete pipeline or recognized revenue; report missing or unrequested fields as unknown.

[Weavz HubSpot integration](https://weavz.io/integrations/hubspot) · [PydanticAI workflow](https://github.com/weavz/weavz-hubspot-pipeline-review)

Framework setup recipes:

- [HubSpot MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#hubspot-mcp-with-crewai-python)
- [HubSpot MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#hubspot-mcp-with-agno-python)
- [HubSpot MCP with Vercel AI SDK TypeScript](https://github.com/weavz/weavz-vercel-ai-sdk/blob/main/docs/app-recipes.md#hubspot-mcp-with-vercel-ai-sdk-typescript)

## Intercom MCP

Find one bounded set of open Intercom conversations and read a selected conversation before preparing a support brief.

`find-conversation` searches by the specified field, match type, term, and optional status/date filters. It returns a matching conversation sample, not a full support history. `get-conversation` reads one exact returned `conversationId`; cite only content present in that result.

[Weavz Intercom integration](https://weavz.io/integrations/intercom) · [PydanticAI workflow](https://github.com/weavz/weavz-intercom-conversation-brief)

## Jira Cloud MCP

Summarize the bounded issues returned by one JQL query for an active sprint, separating status, priority, blockers, and missing assignees.

`search_issues` returns Jira issue fields matching the supplied JQL up to `max_results`. This action exposes no continuation token, so treat the result as a bounded sample and do not infer that unreturned sprint issues do not exist. Use status, priority, and assignee values as returned.

[Weavz Jira Cloud integration](https://weavz.io/integrations/jira-cloud) · [PydanticAI workflow](https://github.com/weavz/weavz-jira-sprint-summary)

Framework setup recipes:

- [Jira Cloud MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-langgraph-python)
- [Jira Cloud MCP with AutoGen Python](https://github.com/weavz/weavz-autogen/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-autogen-python)
- [Jira Cloud MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#jira-cloud-mcp-with-semantic-kernel-python)

## Linear MCP

Search a bounded Linear issue sample and read one selected issue before recommending a review order.

`search_issues` returns matches for the supplied query and `limit` (optionally scoped to a team). `get_issue` reads one exact returned Linear ID. The response may omit details not selected by the action; use only returned fields and do not infer dependencies or complete backlog coverage.

[Weavz Linear integration](https://weavz.io/integrations/linear) · [PydanticAI workflow](https://github.com/weavz/weavz-linear-backlog-review)

## Notion MCP

Find pages by title, retrieve selected page content, and answer only from the returned text.

`find_page` returns a capped set of title matches (limit 1–100), not authoritative page text. For each selected result, call `getPageOrBlockChildren` with the returned `parentId`, `markdown: true`, and `dynamic: {}`. Report only content in the returned block tree; do not assume unreturned descendants or additional pages were read.

[Weavz Notion integration](https://weavz.io/integrations/notion) · [PydanticAI workflow](https://github.com/weavz/weavz-notion-knowledge-research)

Framework setup recipes:

- [Notion MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#notion-mcp-with-openai-agents-sdk-python)
- [Notion MCP with PydanticAI Python](https://github.com/weavz/weavz-pydantic-ai/blob/main/docs/app-recipes.md#notion-mcp-with-pydanticai-python)
- [Notion MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#notion-mcp-with-langchain-python)
- [Notion MCP with LlamaIndex Python](https://github.com/weavz/weavz-llamaindex/blob/main/docs/app-recipes.md#notion-mcp-with-llamaindex-python)
- [Notion MCP with Mastra TypeScript](https://github.com/weavz/weavz-mastra/blob/main/docs/app-recipes.md#notion-mcp-with-mastra-typescript)
- [Notion MCP with LangChain.js TypeScript](https://github.com/weavz/weavz-langchain-js/blob/main/docs/app-recipes.md#notion-mcp-with-langchainjs-typescript)
- [Notion MCP with OpenAI Agents SDK for TypeScript](https://github.com/weavz/weavz-openai-agents-js/blob/main/docs/app-recipes.md#notion-mcp-with-openai-agents-sdk-for-typescript)

## Salesforce MCP

Build a short brief from Account records matching one explicit SOQL WHERE condition.

`find_records_by_query` searches the specified Salesforce object using the supplied SOQL WHERE clause (omit the `WHERE` keyword). The action exposes no explicit pagination or result-limit input, so do not promise exhaustive coverage or imply a full object export. Use only returned records and fields; report missing values as unknown.

[Weavz Salesforce integration](https://weavz.io/integrations/salesforce) · [PydanticAI workflow](https://github.com/weavz/weavz-salesforce-account-brief)

Framework setup recipes:

- [Salesforce MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#salesforce-mcp-with-semantic-kernel-python)

## Shopify MCP

Summarize one customer's bounded Shopify order page by returned order status.

`get_customer_orders` is scoped to one exact `customer_id`, optional status filter, and `limit`. It returns only that customer's matching order sample; do not treat it as a store-wide report or assume unseen pages were read. Currency and fulfillment claims must come from returned fields.

[Weavz Shopify integration](https://weavz.io/integrations/shopify) · [PydanticAI workflow](https://github.com/weavz/weavz-shopify-orders-report)

## Slack MCP

Summarize a small recent Slack channel sample and one selected thread, separating decisions, questions, and attributed statements.

`get_channel_history` returns up to the requested `limit` (maximum 100) of recent messages in one channel. `get_thread_replies` reads replies for the exact channel and parent timestamp. The sample does not represent complete channel history; do not infer agreement from reactions or omitted messages.

[Weavz Slack integration](https://weavz.io/integrations/slack) · [PydanticAI workflow](https://github.com/weavz/weavz-slack-channel-digest)

Framework setup recipes:

- [Slack MCP with OpenAI Agents SDK Python](https://github.com/weavz/weavz-openai-agents-python/blob/main/docs/app-recipes.md#slack-mcp-with-openai-agents-sdk-python)
- [Slack MCP with LangChain Python](https://github.com/weavz/weavz-langchain-python/blob/main/docs/app-recipes.md#slack-mcp-with-langchain-python)
- [Slack MCP with LangGraph Python](https://github.com/weavz/weavz-langgraph-python/blob/main/docs/app-recipes.md#slack-mcp-with-langgraph-python)
- [Slack MCP with CrewAI Python](https://github.com/weavz/weavz-crewai/blob/main/docs/app-recipes.md#slack-mcp-with-crewai-python)
- [Slack MCP with Agno Python](https://github.com/weavz/weavz-agno/blob/main/docs/app-recipes.md#slack-mcp-with-agno-python)
- [Slack MCP with Strands Agents Python](https://github.com/weavz/weavz-strands/blob/main/docs/app-recipes.md#slack-mcp-with-strands-agents-python)
- [Slack MCP with AutoGen Python](https://github.com/weavz/weavz-autogen/blob/main/docs/app-recipes.md#slack-mcp-with-autogen-python)
- [Slack MCP with Semantic Kernel Python](https://github.com/weavz/weavz-semantic-kernel/blob/main/docs/app-recipes.md#slack-mcp-with-semantic-kernel-python)
- [Slack MCP with Vercel AI SDK TypeScript](https://github.com/weavz/weavz-vercel-ai-sdk/blob/main/docs/app-recipes.md#slack-mcp-with-vercel-ai-sdk-typescript)
- [Slack MCP with Mastra TypeScript](https://github.com/weavz/weavz-mastra/blob/main/docs/app-recipes.md#slack-mcp-with-mastra-typescript)
- [Slack MCP with LangChain.js TypeScript](https://github.com/weavz/weavz-langchain-js/blob/main/docs/app-recipes.md#slack-mcp-with-langchainjs-typescript)
- [Slack MCP with LangGraph.js TypeScript](https://github.com/weavz/weavz-langgraph-js/blob/main/docs/app-recipes.md#slack-mcp-with-langgraphjs-typescript)
- [Slack MCP with OpenAI Agents SDK for TypeScript](https://github.com/weavz/weavz-openai-agents-js/blob/main/docs/app-recipes.md#slack-mcp-with-openai-agents-sdk-for-typescript)

## Stripe MCP

Review a bounded page of subscription statuses and flag records needing human review, without calculating revenue.

`search_subscriptions` accepts optional status, price, customer, and created-date filters, a result `limit`, `fetch_all`, and an optional customer-detail flag. Keep `fetch_all` false and the limit bounded; this is a sample, not an account-wide census. Use status counts only, not revenue or inferred payment outcomes.

[Weavz Stripe integration](https://weavz.io/integrations/stripe) · [PydanticAI workflow](https://github.com/weavz/weavz-stripe-subscription-review)

## Todoist MCP

Make a read-only day plan from one Todoist project and due/overdue filter, using an explicit as-of date.

`list_tasks` supports project, section, label, IDs or filter parameters and a result `limit`/cursor. Use only the selected project/filter page and state the as-of date. An empty response does not prove that tasks outside the query or current page do not exist.

[Weavz Todoist integration](https://weavz.io/integrations/todoist) · [PydanticAI workflow](https://github.com/weavz/weavz-todoist-day-plan)

## Trello MCP

Review open cards on one Trello board and inspect one selected card plus a bounded comments sample.

`list_cards` filters by the supplied board/list and filter, and returns only requested fields. `get_card` reads one exact card ID; `list_comments` reads its comment actions with an optional limit/cursor. Do not assume the card sample or comments cover all board activity.

[Weavz Trello integration](https://weavz.io/integrations/trello) · [PydanticAI workflow](https://github.com/weavz/weavz-trello-project-health)

## Zendesk MCP

Search one bounded page of open Zendesk tickets and read selected ticket details/comments for a safe handoff brief.

`search_tickets` enforces `type:ticket` and returns one bounded page (limit capped at 100). Search results are summaries; `get_ticket` reads one exact numeric ID and returns comments only if `include_comments` is enabled, with `comments_limit`. Do not claim all support tickets were reviewed.

[Weavz Zendesk integration](https://weavz.io/integrations/zendesk) · [PydanticAI workflow](https://github.com/weavz/weavz-zendesk-ticket-handoff)

Framework setup recipes:

- [Zendesk MCP with LangGraph.js TypeScript](https://github.com/weavz/weavz-langgraph-js/blob/main/docs/app-recipes.md#zendesk-mcp-with-langgraphjs-typescript)

## Agent-readable directory

Use [examples-index.json](../examples-index.json) to select an example by app, framework, language, authentication method, MCP mode, and verification scope. Read the selected repository's README and AGENTS.md before running commands. Keep tokens and real account data out of prompts and commits.
