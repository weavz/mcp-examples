# Example-specific guidance

- Use the native `pydantic_ai.mcp.MCPToolset` adapter.
- Keep this example independently installable; regenerate and commit `uv.lock` when dependencies change.
- Fixture checks prove local adapter behavior only. Do not describe them as live Weavz or model proof.
- Do not commit `.env` files or credentials.
