from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connection import validate_catalog, validate_live_connection
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.mcp import BasicMCPClient, aget_tools_from_mcp_url
from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def names_for(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {"weavz_search", "weavz_read_api", "weavz_execute"}


async def run_agent(prompt: str, tools: list[object]) -> str:
    model = os.environ.get("WEAVZ_MODEL")
    if not model or not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set WEAVZ_MODEL and OPENAI_API_KEY for the optional LlamaIndex model run")
    agent = FunctionAgent(tools=tools, llm=OpenAI(model=model), system_prompt="Use the connected Weavz MCP tools to complete the request.")
    result = await agent.run(prompt)
    return str(result)


async def exercise(mode: str, url: str, token: str, *, fixture: bool = False, prompt: str | None = None) -> None:
    client = BasicMCPClient(url, headers={"Authorization": f"Bearer {token}"})
    listed = await client.list_tools()
    names = {tool.name for tool in listed.tools}
    validate_catalog(mode, names)
    if fixture and not names_for(mode).issubset(names):
        raise RuntimeError(f"Expected fixture tools {sorted(names_for(mode))}; got {sorted(names)}")
    if not fixture and prompt is None:
        print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode, "tools": sorted(names)}))
        return
    tools = await aget_tools_from_mcp_url(url, client=client)
    by_name = {tool.metadata.name: tool for tool in tools}
    if prompt:
        print(await run_agent(prompt, tools))
        return
    if mode == "tools":
        result = await by_name["demo__lookup_record"].acall(recordId="record-1")
        assert_fixture_result(mode, result)
        results = {"lookup": str(result)}
    else:
        search = await by_name["weavz_search"].acall(query="fixture")
        read_api = await by_name["weavz_read_api"].acall(alias="demo", action="lookup_record")
        result = await by_name["weavz_execute"].acall(code=CODE_EXAMPLE)
        assert_fixture_result(mode, search)
        assert_fixture_result(mode, result)
        if "demo" not in json.dumps(read_api, default=str):
            raise AssertionError(f"Unexpected demo API result: {read_api}")
        results = {"search": str(search), "read_api": str(read_api), "execute": str(result)}
    print(json.dumps({"proof": "local fixture LlamaIndex FunctionTool calls", "mode": mode, "tools": sorted(names), "results": results}))


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
        url, token = os.getenv("WEAVZ_MCP_URL"), os.getenv("WEAVZ_MCP_TOKEN")
        if not url or not token:
            raise SystemExit("Set WEAVZ_MCP_URL and WEAVZ_MCP_TOKEN from your custom Weavz setup")
        try:
            url, token = validate_live_connection(url, token)
        except ValueError as error:
            raise SystemExit(str(error)) from error
        await exercise(args.mode, url, token, prompt=args.prompt)


if __name__ == "__main__":
    asyncio.run(main())
