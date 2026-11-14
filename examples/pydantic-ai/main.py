from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connection import validate_catalog, validate_live_connection

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset

from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def expected_names(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {
        "weavz_search", "weavz_read_api", "weavz_execute"
    }


def validate_tools(mode: str, tools: list[Any]) -> None:
    names = {tool.name for tool in tools}
    missing = expected_names(mode) - names
    if missing:
        raise RuntimeError(f"Server does not advertise {mode} mode tools: {sorted(missing)}")


async def exercise(mode: str, url: str, token: str, *, fixture: bool = False,
                   prompt: str | None = None) -> None:
    toolset = MCPToolset(url, headers={"Authorization": f"Bearer {token}"})
    async with toolset:
        tools = await toolset.list_tools()
        names = {tool.name for tool in tools}
        validate_catalog(mode, names)
        if fixture:
            validate_tools(mode, tools)
        elif prompt is None:
            print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode,
                              "tools": sorted(tool.name for tool in tools)}))
            return
        if prompt:
            model = os.environ.get("WEAVZ_MODEL")
            if not model:
                raise RuntimeError("Set WEAVZ_MODEL to a model string supported by PydanticAI")
            agent = Agent(model, toolsets=[toolset], instructions="Use the available Weavz MCP tool for the requested lookup.")
            result = await agent.run(prompt)
            print(result.output)
            return

        if mode == "tools" and fixture:
            result = await toolset.direct_call_tool("demo__lookup_record", {"recordId": "record-1"})
            assert_fixture_result(mode, result)
            proof = {"lookup": str(result)}
        elif fixture:
            search = await toolset.direct_call_tool("weavz_search", {"query": "fixture"})
            read_api = await toolset.direct_call_tool("weavz_read_api", {"alias": "demo", "action": "lookup_record"})
            result = await toolset.direct_call_tool("weavz_execute", {"code": CODE_EXAMPLE})
            assert_fixture_result(mode, search)
            assert_fixture_result(mode, result)
            if isinstance(read_api, dict) and "demo" not in read_api.get("aliases", []):
                raise AssertionError(f"Unexpected demo API metadata: {read_api}")
            proof = {"search": str(search), "read_api": str(read_api), "execute": str(result)}
        else:
            raise RuntimeError("A live tool call requires --prompt; use --fixture for synthetic calls")
        print(json.dumps({"proof": "local fixture adapter calls", "mode": mode,
                          "tools": sorted(expected_names(mode)), "results": proof}))


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true", help="Start and call the local synthetic MCP fixture")
    parser.add_argument("--mode", choices=("tools", "code"), default=os.getenv("WEAVZ_MCP_MODE", "tools"))
    parser.add_argument("--prompt", help="Optional live model run; requires WEAVZ_MODEL and provider credentials")
    args = parser.parse_args()
    if args.fixture:
        if args.prompt:
            raise SystemExit("--prompt uses a model provider; run without --fixture for a live model run")
        with FixtureServer(args.mode) as fixture:
            fixture.reject_bad_token()
            await exercise(args.mode, fixture.url, "local-fixture-token", fixture=True)
    else:
        url = os.getenv("WEAVZ_MCP_URL")
        token = os.getenv("WEAVZ_MCP_TOKEN")
        if not url or not token:
            raise SystemExit("Set WEAVZ_MCP_URL and WEAVZ_MCP_TOKEN from your custom Weavz MCP setup")
        try:
            url, token = validate_live_connection(url, token)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        await exercise(args.mode, url, token, prompt=args.prompt)


if __name__ == "__main__":
    asyncio.run(main())
