# LlamaIndex Python MCP app recipes

Connect LlamaIndex Python to app tools through a remote Weavz MCP server. These recipes describe bounded read tasks for your configured app connections.

App names identify integrations supplied by Weavz. Use the Weavz MCP endpoint and its authorization for these recipes.

## Before running an app task

1. Follow this repository's [README](../README.md) to install dependencies and pass the local fixture checks.
2. Configure the app in your Weavz workspace and connect the intended user's account. Keep app credentials in Weavz and model credentials in your local environment.
3. Set the custom MCP endpoint, end-user MCP access token, and model configuration described in the README. The hosted personal connector uses client OAuth; this framework example uses a custom endpoint.
4. Choose the mode configured on your server. The Python commands below use `--mode code`; use `--mode tools` for a Tool Mode endpoint. TypeScript clients discover the server's catalog automatically.

Replace the sample IDs and task bounds in each prompt with your own. The live commands use your configured model and app connection. Local fixture tests use synthetic records and do not establish live app authorization.

## Notion MCP with LlamaIndex Python

Find pages by title, retrieve selected page content, and answer only from the returned text.

Required task context:

- Connect a Notion account that can read the chosen pages.
- Search with title terms, then use the exact returned page/block ID as `parentId` to read content.
- A title-search match or snippet is not evidence of page contents; do not write or comment.

Configure the app alias as `knowledge` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `find_page` | `exact_match`, `limit`, `title` |
| `getPageOrBlockChildren` | `dynamic`, `markdown`, `parentId` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `knowledge` Notion alias, search for the
requested pages by title and read each selected result's actual page content using its
returned `parentId` before answering. Cite the page IDs and distinguish source
statements from synthesis. Example only: title `On-call escalation playbook`, page IDs
`notion-page-301` and `notion-page-302`; replace these with current search results. If
the page is missing or its returned content is empty, say so. Do not edit pages or add
comments.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`find_page` returns a capped set of title matches (limit 1–100), not authoritative page text. For each selected result, call `getPageOrBlockChildren` with the returned `parentId`, `markdown: true`, and `dynamic: {}`. Report only content in the returned block tree; do not assume unreturned descendants or additional pages were read.

[App connection guide](https://weavz.io/integrations/notion) · [PydanticAI task example](https://github.com/weavz/weavz-notion-knowledge-research)

## Google Drive MCP with LlamaIndex Python

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

## Google Docs MCP with LlamaIndex Python

Review one exact Google Doc's returned content for decisions, open questions, dates, and named owners.

Required task context:

- Connect a Google account with read access to the specific document.
- Provide an exact `documentId`; `google-doc-demo-501` is synthetic.
- Do not imply access to linked docs or comments unless the returned content includes them; do not edit, comment, or share.

Configure the app alias as `launch_docs` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `get_document` | `documentId` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `launch_docs` Google Docs alias, read
only the selected document ID. Summarize stated decisions and unresolved questions,
then list dates and owners exactly as returned. Mark missing owners or fields as
unknown and distinguish suggestions from written decisions. Example only: document
`google-doc-demo-501`, section IDs `doc-section-1` through `doc-section-3`; replace
with the user-selected document. Do not edit, comment on, or share it.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`get_document` returns content and metadata for one exact document ID. The tool does not imply that linked documents, comments, or external attachments were read. Base claims only on returned document content and cite the selected document/sections when identifiers are present.

[App connection guide](https://weavz.io/integrations/google-docs) · [PydanticAI task example](https://github.com/weavz/weavz-google-docs-document-review)

## Google Sheets MCP with LlamaIndex Python

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
