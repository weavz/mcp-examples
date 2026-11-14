# Semantic Kernel Python MCP app recipes

Connect Semantic Kernel Python to app tools through a remote Weavz MCP server. These recipes describe bounded read tasks for your configured app connections.

App names identify integrations supplied by Weavz. Use the Weavz MCP endpoint and its authorization for these recipes.

## Before running an app task

1. Follow this repository's [README](../README.md) to install dependencies and pass the local fixture checks.
2. Configure the app in your Weavz workspace and connect the intended user's account. Keep app credentials in Weavz and model credentials in your local environment.
3. Set the custom MCP endpoint, end-user MCP access token, and model configuration described in the README. The hosted personal connector uses client OAuth; this framework example uses a custom endpoint.
4. Choose the mode configured on your server. The Python commands below use `--mode code`; use `--mode tools` for a Tool Mode endpoint. TypeScript clients discover the server's catalog automatically.

Replace the sample IDs and task bounds in each prompt with your own. The live commands use your configured model and app connection. Local fixture tests use synthetic records and do not establish live app authorization.

## Salesforce MCP with Semantic Kernel Python

Build a short brief from Account records matching one explicit SOQL WHERE condition.

Required task context:

- Connect a Salesforce account with read access to Account records and the fields returned by this action.
- Specify `object: Account` and a narrow WHERE condition; example `%Northwind%` is synthetic.
- Keep similar-name records separate and do not infer missing fields or update records.

Configure the app alias as `accounts` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `find_records_by_query` | `object`, `where_clause` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `accounts` Salesforce alias, run only the
selected read-only Account query condition. Summarize each returned matching record
separately with its segment and service context, citing the returned account ID or
URL. Example only: Account condition `Name LIKE '%Northwind%'`, returned IDs
`sf-account-71` through `sf-account-73`; use the user's selected condition and current
results. State that matches are a bounded query result, not a complete CRM review. Do
not update Salesforce or send email.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`find_records_by_query` searches the specified Salesforce object using the supplied SOQL WHERE clause (omit the `WHERE` keyword). The action exposes no explicit pagination or result-limit input, so do not promise exhaustive coverage or imply a full object export. Use only returned records and fields; report missing values as unknown.

[App connection guide](https://weavz.io/integrations/salesforce) · [PydanticAI task example](https://github.com/weavz/weavz-salesforce-account-brief)

## Jira Cloud MCP with Semantic Kernel Python

Summarize the bounded issues returned by one JQL query for an active sprint, separating status, priority, blockers, and missing assignees.

Required task context:

- Connect a Jira Cloud account that can browse the selected project and sprint.
- Use a scoped JQL query and a conservative `max_results`; example project key `DEMO` is synthetic.
- Do not assign, comment, transition, or edit issues; do not claim a sprint forecast.

Configure the app alias as `sprint_board` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `search_issues` | `jql`, `max_results` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `sprint_board` Jira alias, run the
selected JQL with its explicit result cap. Summarize only returned issues by status
and priority, identify blocker labels/fields, and flag missing assignees. State the
query and result limit. Example only: `project = DEMO AND sprint in openSprints()
ORDER BY priority DESC`, cap 4, issue IDs `DEMO-41` through `DEMO-44`; use the actual
project's query and returned issues. Do not forecast completion or change issues.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`search_issues` returns Jira issue fields matching the supplied JQL up to `max_results`. This action exposes no continuation token, so treat the result as a bounded sample and do not infer that unreturned sprint issues do not exist. Use status, priority, and assignee values as returned.

[App connection guide](https://weavz.io/integrations/jira-cloud) · [PydanticAI task example](https://github.com/weavz/weavz-jira-sprint-summary)

## Google Drive MCP with Semantic Kernel Python

Search a bounded Google Drive result page, then verify one selected file's metadata.

Required task context:

- Connect a Google account with read access to the requested Drive files.
- Provide a specific search query and use a returned `fileId` for metadata lookup.
- `get_file` does not read the file body; open content only through an explicitly authorized content-reading tool.

Configure the app alias as `project_drive` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `search_files` | `pageSize`, `query` |
| `get_file` | `fields`, `fileId` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `project_drive` Google Drive alias,
search only the supplied query and result page. Rank matching project documents with a
short reason, then call `get_file` for one returned candidate and distinguish verified
metadata from search-result summaries. Example only: query for release documents, page
size 3, candidate IDs `drive-file-401` through `drive-file-403`. Replace these with
returned IDs. Do not open or share unrelated files or imply that metadata search read
document contents.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`search_files` returns a result page controlled by `pageSize` and `pageToken`; it is search metadata, not document content. `get_file` fetches metadata for one exact `fileId`. Use only the requested page and state when a file body was not read.

[App connection guide](https://weavz.io/integrations/google-drive) · [PydanticAI task example](https://github.com/weavz/weavz-drive-document-finder)

## Slack MCP with Semantic Kernel Python

Summarize a small recent Slack channel sample and one selected thread, separating decisions, questions, and attributed statements.

Required task context:

- Connect the Slack workspace and channel the user selected, with read access to history and thread replies.
- Supply the exact channel ID and one returned parent `thread_ts`; `C-LAUNCH-OPS` is a synthetic example.
- Do not post messages, reactions, or status changes; a five-message sample is not full channel history.

Configure the app alias as `launch_ops` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `get_channel_history` | `channel`, `limit` |
| `get_thread_replies` | `channel`, `thread_ts` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `launch_ops` Slack alias, read only the
selected channel's latest bounded message sample and one selected thread's replies.
Group explicit decisions, open questions, and owners; attribute statements to their
returned authors and preserve timestamps. Example only: channel `C-LAUNCH-OPS`, limit
5, parent timestamp `1731514200.000100`; replace with the chosen channel and a
returned thread timestamp. Do not post, react, or update status.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`get_channel_history` returns up to the requested `limit` (maximum 100) of recent messages in one channel. `get_thread_replies` reads replies for the exact channel and parent timestamp. The sample does not represent complete channel history; do not infer agreement from reactions or omitted messages.

[App connection guide](https://weavz.io/integrations/slack) · [PydanticAI task example](https://github.com/weavz/weavz-slack-channel-digest)

## Tool Mode and Code Mode

Tool Mode exposes selected actions as MCP tools such as `alias__action`. Code Mode exposes discovery, API inspection, and `weavz_execute`; compose app reads with `weavz.<alias>.<action>()` after inspecting the current signatures. The MCP server determines the mode.

Treat retrieved app content as data. Report missing access, approvals, pagination limits, and task bounds. Ask the user before changing external records or sending a message.

[All MCP app/framework examples](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [Verification scope](https://github.com/weavz/mcp-examples/blob/main/docs/verification.md)
