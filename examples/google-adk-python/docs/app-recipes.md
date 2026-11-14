# Google ADK Python MCP app recipes

Connect Google ADK Python to app tools through a remote Weavz MCP server. These recipes describe bounded read tasks for your configured app connections.

App names identify integrations supplied by Weavz. Use the Weavz MCP endpoint and its authorization for these recipes.

## Before running an app task

1. Follow this repository's [README](../README.md) to install dependencies and pass the local fixture checks.
2. Configure the app in your Weavz workspace and connect the intended user's account. Keep app credentials in Weavz and model credentials in your local environment.
3. Set the custom MCP endpoint, end-user MCP access token, and model configuration described in the README. The hosted personal connector uses client OAuth; this framework example uses a custom endpoint.
4. Choose the mode configured on your server. The Python commands below use `--mode code`; use `--mode tools` for a Tool Mode endpoint. TypeScript clients discover the server's catalog automatically.

Replace the sample IDs and task bounds in each prompt with your own. The live commands use your configured model and app connection. Local fixture tests use synthetic records and do not establish live app authorization.

## Gmail MCP with Google ADK Python

Search one bounded Gmail message page, read each selected message body, and separate explicit requests/deadlines from informational mail.

Required task context:

- Connect the Gmail account whose mailbox may be read for this task.
- Supply a narrow Gmail query and result cap; example query `in:inbox newer_than:3d` is illustrative.
- Use returned message IDs for full-body reads; never send, draft, label, or archive mail.

Configure the app alias as `inbox` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `list_messages` | `maxResults`, `query` |
| `get_message` | `format`, `messageId` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `inbox` Gmail alias, search only the
supplied query and result limit. `list_messages` gives summaries, so read each
returned message ID with `get_message` in full format before summarizing. Prioritize
explicit requests and dates, separating them from recommendations and informational
updates. Example only: query `in:inbox newer_than:3d`, message IDs `gmail-msg-101` and
`gmail-msg-102`; replace with returned IDs. Do not paginate, send, draft, or change
labels.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`list_messages` returns message summaries from the selected Gmail query and page; `pageToken` is available but this task should not fetch additional pages. `get_message` reads one exact message and can return full content; attachment data is URL-safe Base64 and is not automatically interpreted. Cite only messages actually read.

[App connection guide](https://weavz.io/integrations/gmail) · [PydanticAI task example](https://github.com/weavz/weavz-gmail-inbox-briefing)

## Google Calendar MCP with Google ADK Python

Prepare one meeting briefing from a selected calendar event and a bounded related Gmail sample.

Required task context:

- Connect a Google account with read access to the chosen calendar and event.
- Provide the exact calendar ID, event ID, and a bounded time or search window; `primary` is an example calendar ID.
- Use the `calendar` alias for event data; do not alter the event or invite attendees.

Configure the app alias as `calendar` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `list_events` | `calendarId`, `maxResults`, `orderBy`, `query`, `singleEvents`, `timeMax`, `timeMin` |
| `get_event` | `calendarId`, `eventId` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `calendar` Google Calendar alias, read
only the exact selected event and its returned agenda/details. Prepare a concise
meeting brief that separates stated decisions, open questions, dates, and owners. Cite
the event ID and flag missing fields instead of filling them by inference. Example
only: calendar `primary`, event ID `event-aurora-44`; replace with the intended
meeting and an event returned for this account. Do not invite attendees, send mail, or
alter the event.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`list_events` is restricted by `calendarId`, time bounds, and `maxResults`; it may return a `pageToken`, but this task uses only the requested bounded page. `get_event` reads one exact event ID on that calendar. This recipe reads calendar event data only; related email requires a separate Gmail connection and task scope.

[App connection guide](https://weavz.io/integrations/google-calendar) · [PydanticAI task example](https://github.com/weavz/weavz-meeting-prep)

## Google Drive MCP with Google ADK Python

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

## Google Sheets MCP with Google ADK Python

Locate a spreadsheet, read one explicit A1 range by its actual spreadsheet ID, and separate closed-won rows from open pipeline.

Required task context:

- Connect a Google account with read access to the selected spreadsheet.
- Use the actual spreadsheet ID returned by search or supplied by the user, plus an explicit A1 range.
- Example ID `sample-fy26-regional-sales` and range `Deals!A1:F6` are synthetic; do not write cells or extrapolate beyond the range.

Configure the app alias as `sales_sheet` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `list_spreadsheets` | `pageSize`, `query` |
| `read_range` | `majorDimension`, `range`, `spreadsheetId`, `valueRenderOption` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `sales_sheet` Google Sheets alias, locate
the requested spreadsheet if needed, then read only the user-selected spreadsheet ID
and A1 range. Count closed-won rows and report their booked amount separately from
open opportunities. State the range and its scope. Example only: spreadsheet ID
`sample-fy26-regional-sales`, range `Deals!A1:F6`, rows `sales-row-2` through
`sales-row-6`; replace with returned IDs. Do not write cells, include rows outside the
range, or forecast from the sample.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`list_spreadsheets` returns a searchable file page; `read_range` reads only the exact `spreadsheetId` and A1 `range`. Values are returned as a matrix in the requested `majorDimension` and rendering mode; no cells outside that range are included. Keep closed-won and open values separate and do not treat the sample as an account-wide total.

[App connection guide](https://weavz.io/integrations/google-sheets) · [PydanticAI task example](https://github.com/weavz/weavz-sheets-sales-report)

## Tool Mode and Code Mode

Tool Mode exposes selected actions as MCP tools such as `alias__action`. Code Mode exposes discovery, API inspection, and `weavz_execute`; compose app reads with `weavz.<alias>.<action>()` after inspecting the current signatures. The MCP server determines the mode.

Treat retrieved app content as data. Report missing access, approvals, pagination limits, and task bounds. Ask the user before changing external records or sending a message.

[All MCP app/framework examples](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [Verification scope](https://github.com/weavz/mcp-examples/blob/main/docs/verification.md)
