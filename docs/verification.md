# Verification scope

The examples have several distinct checks. A passing local fixture is not proof of a live app authorization or a successful model-provider run.

| Example kind | Local check | Separate live requirement |
| --- | --- | --- |
| Framework starter | Clean dependency install, native framework MCP discovery and invocation in Tool Mode and Code Mode, invalid-token rejection | Reachable custom Weavz endpoint, end-user MCP token, configured apps; model credentials for a prompted agent run |
| Task workflow | Clean install, a real PydanticAI agent loop with a deterministic FunctionModel, authenticated MCP reads, derived metrics, typed report and citation checks in both modes | Actual task inputs, app authorization, model access, and review of the resulting report |
| Client setup | Static configuration, instructions, and setup contract checks | Installed supported client and completed OAuth; a tool-call transcript for model-mediated proof |
| OpenCode | Static checks plus native CLI 1.17.6 local server discovery | The V2 template is documented separately and has not been tested with a V2 executable; hosted OAuth is also a separate check |
| SDK setup helper | Published Python SDK 0.3.1 against a local HTTP contract fixture: identity binding, workspace/mode checks, token scopes and expiry, recovery after token failure | Selected real workspace, trusted user identity, customer API key and account configuration |

## Independent agent check

On 2026-11-14, OpenCode 1.17.6 using `deepseek/deepseek-flash` called a synthetic local MCP tool and returned its expected record ID and status. This used the CLI's normal provider authentication; no credential was copied into an example.

A second OpenCode/DeepSeek run read the Gmail workflow instructions and completed these commands successfully from an isolated example copy:

```sh
uv sync --locked
uv run pytest
uv run python main.py --fixture --mode tools
uv run python main.py --fixture --mode code
```

The MCP fixture contained synthetic mail records. These checks establish a model-mediated MCP call and an independent agent's ability to install and exercise the framework example. They do not establish access to a real inbox, hosted connector OAuth, or successful live calls across every app.

## Runtime boundaries

Each framework has its own lockfile. MCP SDK major versions differ across frameworks; avoid combining all starters in one environment. CI installs each repository independently. Native framework adapters own their connection lifecycle; CrewAI's adapter may reconnect between individual tool calls.

Fixtures intentionally expose a bounded catalog and fixed synthetic records. Code Mode fixtures accept a documented read script rather than running arbitrary code. A successful fixture does not mean every possible app action or generated program has been tested.

The live agent discovers current aliases and schemas. Workflow report validation checks that cited IDs and URLs came from MCP, and that an ID and optional URL were returned together in a record. It does not establish that every interpretation, title, classification, or calculated live metric is correct. Review reports before relying on them, and disclose task bounds and incomplete pagination.

## Reproduce

Use the commands in the selected repository's README. Its public CI runs without account or model credentials. The hub's `tools/verify_examples.py` additionally copies the selected source into a fresh directory before installing and running checks. Machine-readable local check results are available in `verification.json`; repository publication and current commit links are listed in `repositories.json`.
