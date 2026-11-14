# Contributing examples

Keep each example independently installable with a useful README, agent instructions, license, local verification commands, and provider-free CI. Pin runtime dependencies with the ecosystem's lockfile. Document the exact framework adapter and the live path separately from synthetic fixtures.

Use native MCP adapters for app access. Trusted-backend setup may use customer SDK management APIs, but agent execution must not substitute direct app or action REST calls for MCP. Preserve workspace and end-user identity. Never put a customer API key in MCP headers.

Run the example's README checks from a clean copy. For the hub, `python3 tools/verify_examples.py <id> --logs <local-log-directory>` installs and tests an independent snapshot. Logs can contain synthetic transcripts and local paths; keep them out of commits. Client checks must state whether they cover static configuration, native discovery, OAuth, or model-mediated tool use.

Workflow sources live in `workflows/` and `shared/workflow-python/`. After changing them, run `python3 tools/render_workflows.py <id>` and the example checks. Update `catalog.json` and run `python3 tools/render_index.py` when adding or renaming examples. Keep generated standalone files aligned with their templates.

Discovery sources are `discovery.json` and `discovery/app-recipes.json`. Use accurate framework and app names, useful task instructions, and source-backed action inputs. After editing them, run `python3 tools/discovery.py`, `python3 tools/render_index.py`, and the hub tests. Keep repository descriptions below 350 characters and topics below GitHub's 20-topic limit. Do not add popularity, search-volume, ranking, or live-verification claims without corresponding evidence.

Do not commit credentials, real customer data, local machine paths, private product internals, or raw provider traces. Synthetic records must be clearly labeled. Respect upstream licenses and write original examples and explanations.

Make meaningful commits with accurate dates. Release only tested examples, and distinguish local checks from live-account proof.
