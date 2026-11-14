from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.mcp import MCPTools
from connection import validate_catalog, validate_live_connection
from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def names_for(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {"weavz_search", "weavz_read_api", "weavz_execute"}


async def run_agent(prompt: str, mcp_tools: MCPTools) -> object:
    model_id = os.getenv("WEAVZ_MODEL")
    api_key = os.getenv("OPENAI_API_KEY")
    if not model_id or not api_key:
        raise RuntimeError("Set WEAVZ_MODEL and OPENAI_API_KEY for the optional Agno run")
    agent = Agent(model=OpenAIResponses(id=model_id, api_key=api_key), tools=[mcp_tools])
    return await agent.arun(prompt)


async def exercise(mode: str, url: str, token: str, *, fixture: bool = False, prompt: str | None = None) -> None:
    async with MCPTools(
        url=url,
        transport="streamable-http",
        headers={"Authorization": f"Bearer {token}"},
    ) as mcp_tools:
        assert mcp_tools.session is not None
        listed = await mcp_tools.session.list_tools()
        names = {tool.name for tool in listed}
        validate_catalog(mode, names)
        if fixture and not names_for(mode).issubset(names):
            raise RuntimeError(f"Expected fixture tools {sorted(names_for(mode))}; got {sorted(names)}")
        if not fixture and prompt is None:
            print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode, "tools": sorted(names)}))
            return
        if prompt:
            response = await run_agent(prompt, mcp_tools)
            print(getattr(response, "content", str(response)))
            return
        if mode == "tools":
            result = await mcp_tools.session.call_tool("demo__lookup_record", {"recordId": "record-1"})
            assert_fixture_result(mode, result)
            results = {"lookup": str(result)}
        else:
            search = await mcp_tools.session.call_tool("weavz_search", {"query": "fixture"})
            read_api = await mcp_tools.session.call_tool("weavz_read_api", {"alias": "demo", "action": "lookup_record"})
            result = await mcp_tools.session.call_tool("weavz_execute", {"code": CODE_EXAMPLE})
            assert_fixture_result(mode, search)
            assert_fixture_result(mode, result)
            if "demo" not in json.dumps(read_api, default=str):
                raise AssertionError(f"Unexpected demo API result: {read_api}")
            results = {"search": str(search), "read_api": str(read_api), "execute": str(result)}
        print(json.dumps({"proof": "local fixture Agno MCPTools calls", "mode": mode, "tools": sorted(names), "results": results}))


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--mode", choices=("tools", "code"), default=os.getenv("WEAVZ_MCP_MODE", "tools"))
    parser.add_argument("--prompt")
    args = parser.parse_args()
    if args.fixture:
        if args.prompt:
            raise SystemExit("--prompt uses a model provider; run without --fixture for a live model run")
        with FixtureServer(args.mode) as fixture:
            fixture.reject_bad_token()
            await exercise(args.mode, fixture.url, "local-fixture-token", fixture=True)
    else:
        try:
            url, token = validate_live_connection(os.getenv("WEAVZ_MCP_URL"), os.getenv("WEAVZ_MCP_TOKEN"))
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        await exercise(args.mode, url, token, prompt=args.prompt)


if __name__ == "__main__":
    asyncio.run(main())
