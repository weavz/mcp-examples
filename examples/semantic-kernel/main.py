from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.functions import KernelArguments
from connection import validate_catalog, validate_live_connection
from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def names_for(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {"weavz_search", "weavz_read_api", "weavz_execute"}


async def run_agent(prompt: str, kernel: Kernel) -> object:
    model_id = os.getenv("WEAVZ_MODEL")
    api_key = os.getenv("OPENAI_API_KEY")
    if not model_id or not api_key:
        raise RuntimeError("Set WEAVZ_MODEL and OPENAI_API_KEY for the optional Semantic Kernel agent run")
    service = OpenAIChatCompletion(ai_model_id=model_id, api_key=api_key)
    agent = ChatCompletionAgent(
        name="WeavzAssistant",
        instructions="Use the connected Weavz MCP functions to answer the user's task accurately.",
        service=service,
        kernel=kernel,
    )
    return await agent.get_response(messages=prompt)


async def exercise(mode: str, url: str, token: str, *, fixture: bool = False, prompt: str | None = None) -> None:
    kernel = Kernel()
    plugin = MCPStreamableHttpPlugin(
        name="weavz",
        url=url,
        headers={"Authorization": f"Bearer {token}"},
        load_tools=True,
        load_prompts=False,
    )
    async with plugin:
        kernel.add_plugin(plugin)
        functions = kernel.plugins["weavz"].functions
        names = set(functions)
        validate_catalog(mode, names)
        if fixture and not names_for(mode).issubset(names):
            raise RuntimeError(f"Expected fixture tools {sorted(names_for(mode))}; got {sorted(names)}")
        if not fixture and prompt is None:
            print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode, "tools": sorted(names)}))
            return
        if prompt:
            response = await run_agent(prompt, kernel)
            print(str(response))
            return

        async def call(name: str, **kwargs: object) -> object:
            result = await kernel.invoke(
                plugin_name="weavz",
                function_name=name,
                arguments=KernelArguments(**kwargs),
            )
            return getattr(result, "value", result)

        if mode == "tools":
            result = await call("demo__lookup_record", recordId="record-1")
            assert_fixture_result(mode, result)
            results = {"lookup": str(result)}
        else:
            search = await call("weavz_search", query="fixture")
            read_api = await call("weavz_read_api", alias="demo", action="lookup_record")
            result = await call("weavz_execute", code=CODE_EXAMPLE)
            assert_fixture_result(mode, search)
            assert_fixture_result(mode, result)
            if "demo" not in json.dumps(read_api, default=str):
                raise AssertionError(f"Unexpected demo API result: {read_api}")
            results = {"search": str(search), "read_api": str(read_api), "execute": str(result)}
        print(json.dumps({"proof": "local fixture Semantic Kernel native MCP plugin calls", "mode": mode, "tools": sorted(names), "results": results}))


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
