# smolagents Python MCP app recipes

Connect smolagents Python to app tools through a remote Weavz MCP server. These recipes describe bounded read tasks for your configured app connections.

App names identify integrations supplied by Weavz. Use the Weavz MCP endpoint and its authorization for these recipes.

## Before running an app task

1. Follow this repository's [README](../README.md) to install dependencies and pass the local fixture checks.
2. Configure the app in your Weavz workspace and connect the intended user's account. Keep app credentials in Weavz and model credentials in your local environment.
3. Set the custom MCP endpoint, end-user MCP access token, and model configuration described in the README. The hosted personal connector uses client OAuth; this framework example uses a custom endpoint.
4. Choose the mode configured on your server. The Python commands below use `--mode code`; use `--mode tools` for a Tool Mode endpoint. TypeScript clients discover the server's catalog automatically.

Replace the sample IDs and task bounds in each prompt with your own. The live commands use your configured model and app connection. Local fixture tests use synthetic records and do not establish live app authorization.

## GitHub MCP with smolagents Python

Review one selected pull request and a bounded sample of its returned file patches, keeping PR review distinct from issue search.

Required task context:

- Connect a GitHub account or installation that can read the selected repository and pull request.
- Provide an exact `owner/repository` and pull number; example repository `example-org/demo-api`, PR `42` is synthetic.
- Use the read-only GET pull-files endpoint; do not create a review, comment, commit, or merge.

Configure the app alias as `code_review` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `get_pull_request` | `pull_number`, `repository` |
| `custom_api_call` | `method`, `path`, `query_params` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `code_review` GitHub alias, read the
selected pull request and then retrieve its changed-file patches through the GET
pull-files endpoint. Summarize behavior changes, test evidence, and concrete risks
tied to returned paths. State if patches are missing or truncated; do not claim a full
repository review. Example only: `example-org/demo-api` PR `42`, patch record IDs
`pr-file-validator` and `pr-file-retry`; replace with this user's selected PR and
returned files. This recipe reviews pull requests, not issue triage. Do not comment,
submit a review, commit, or merge.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`get_pull_request` reads one exact repository/pull-number pair. `custom_api_call` should be limited to `GET /repos/{owner}/{repo}/pulls/{number}/files` with a bounded `per_page` query; inspect only returned patches, note missing/truncated patch text, and do not paginate unless the user explicitly requests more. This is not a general codebase scan.

[App connection guide](https://weavz.io/integrations/github) · [PydanticAI task example](https://github.com/weavz/weavz-github-pull-request-review)

## Figma MCP with smolagents Python

Map a compact Figma file outline and inspect a small set of returned nodes for bounded design concerns.

Required task context:

- Connect a Figma account with read access to the selected file.
- Provide the exact file key or an HTTPS Figma file URL; choose node IDs from the returned outline.
- Keep selected node IDs to 1–10 and depth to 1 or 2; this is REST design context, not Code Connect or native editing.

Configure the app alias as `product_design` for this prompt, or replace it with the alias your server advertises. Discover the current tool schema before invoking an action.

| App read action | Inputs used by the task |
| --- | --- |
| `get_file_outline` | `depth`, `fileKey`, `maxNodes` |
| `get_node_design_context` | `depth`, `fileKey`, `nodeIds` |

Run in Bash or Zsh:

```bash
read -r -d '' WEAVZ_TASK_PROMPT <<'TASK' || true
Using the connected Weavz MCP server and the `product_design` Figma alias, first read
a compact outline for the selected file, then inspect only the selected returned node
IDs. Report measured layout or accessibility properties separately from
recommendations and cite returned node IDs. Example only: file key
`sample-product-settings-file`, nodes `1:10,1:20`; use only IDs returned for the
current file. Do not resolve an entire library, comment, or change the design.
TASK
uv run --env-file .env python main.py --mode code --prompt "$WEAVZ_TASK_PROMPT"
```

`get_file_outline` returns a compact tree capped by `maxNodes` (1–200); its expansion via `parentNodeId` is caller-directed, not API pagination. `get_node_design_context` accepts 1–10 selected nodes with depth 1 or 2 and returns bounded REST properties/reference IDs, not resolved libraries, Code Connect mappings, generated code, or expiring image assets. Request assets separately only when needed.

[App connection guide](https://weavz.io/integrations/figma) · [PydanticAI task example](https://github.com/weavz/weavz-figma-design-review)

## Google Sheets MCP with smolagents Python

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

## Gmail MCP with smolagents Python

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

## Tool Mode and Code Mode

Tool Mode exposes selected actions as MCP tools such as `alias__action`. Code Mode exposes discovery, API inspection, and `weavz_execute`; compose app reads with `weavz.<alias>.<action>()` after inspecting the current signatures. The MCP server determines the mode.

Treat retrieved app content as data. Report missing access, approvals, pagination limits, and task bounds. Ask the user before changing external records or sending a message.

[All MCP app/framework examples](https://github.com/weavz/mcp-examples/blob/main/docs/integrations.md) · [Verification scope](https://github.com/weavz/mcp-examples/blob/main/docs/verification.md)
