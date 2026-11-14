from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from connection import validate_catalog, validate_live_connection
from google.adk.agents import Agent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.genai import types
from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def names_for(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {"weavz_search", "weavz_read_api", "weavz_execute"}


async def run_agent(prompt: str, toolset: McpToolset, *, model_override: BaseLlm | None = None) -> str:
    model: str | BaseLlm = model_override or os.environ.get("WEAVZ_MODEL", "")
    if not model:
        raise RuntimeError("Set WEAVZ_MODEL and the credentials required by your Google ADK model")
    agent = Agent(name="weavz_assistant", model=model, instruction="Use the connected Weavz MCP tools to complete the user's request.", tools=[toolset])
    sessions = InMemorySessionService()
    session = await sessions.create_session(app_name="weavz_example", user_id="local_user")
    runner = Runner(agent=agent, app_name="weavz_example", session_service=sessions)
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    final = ""
    async for event in runner.run_async(user_id="local_user", session_id=session.id, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            final = "".join(part.text or "" for part in event.content.parts)
    if not final:
        raise RuntimeError("The ADK runner finished without a final text response")
    return final


class FixtureModel(BaseLlm):
    """Deterministic model responses that drive the real ADK tool runner."""

    mode: str
    turn: int = 0

    async def generate_content_async(self, llm_request, stream: bool = False):
        self.turn += 1
        if self.turn == 1:
            if self.mode == "tools":
                requested = [("demo__lookup_record", {"recordId": "record-1"})]
            else:
                requested = [
                    ("weavz_search", {"query": "record-1"}),
                    ("weavz_read_api", {"alias": "demo", "action": "lookup_record"}),
                    ("weavz_execute", {"code": CODE_EXAMPLE}),
                ]
            parts = [
                types.Part(function_call=types.FunctionCall(name=name, args=args))
                for name, args in requested
            ]
            yield LlmResponse(content=types.Content(role="model", parts=parts))
            return

        if self.turn != 2:
            raise RuntimeError("FixtureModel expected one tool-call turn followed by one final response")
        responses = [
            part.function_response
            for content in llm_request.contents
            for part in content.parts or []
            if part.function_response
        ]
        expected = {"demo__lookup_record"} if self.mode == "tools" else {
            "weavz_search", "weavz_read_api", "weavz_execute"
        }
        response_names = {response.name for response in responses}
        missing = expected - response_names
        if missing:
            raise AssertionError(f"ADK did not return fixture responses from {sorted(missing)}")
        payloads = {response.name: response.response for response in responses}
        serialized = json.dumps(payloads, default=str)
        assert_fixture_result(self.mode, serialized)
        if self.mode == "code" and "demo" not in json.dumps(payloads.get("weavz_read_api"), default=str):
            raise AssertionError("Fixture read_api response did not identify the demo alias")
        yield LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="The deterministic fixture tools returned the expected synthetic record.")],
            )
        )


async def exercise(mode: str, url: str, token: str, *, fixture: bool = False, prompt: str | None = None) -> None:
    params = StreamableHTTPConnectionParams(url=url, headers={"Authorization": f"Bearer {token}"})
    toolset = McpToolset(connection_params=params)
    try:
        tools = await toolset.get_tools()
        names = {tool.name for tool in tools}
        validate_catalog(mode, names)
        if fixture and not names_for(mode).issubset(names):
            raise RuntimeError(f"Expected fixture tools {sorted(names_for(mode))}; got {sorted(names)}")
        if not fixture and prompt is None:
            print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode, "tools": sorted(names)}))
            return
        if prompt:
            print(await run_agent(prompt, toolset))
            return
        if fixture:
            result = await run_agent(
                "Use the available tools to verify the synthetic record.",
                toolset,
                model_override=FixtureModel(model="fixture", mode=mode),
            )
            print(json.dumps({
                "proof": "local fixture ADK Runner tool invocations",
                "mode": mode,
                "tools": sorted(names),
                "result": result,
            }))
            return
        raise RuntimeError("A live tool call requires --prompt; use --fixture for synthetic calls")
    finally:
        await toolset.close()


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
