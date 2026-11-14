from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crewai import Agent, Crew, Process, Task
from crewai.mcp.config import MCPServerHTTP
from fixture.harness import CODE_EXAMPLE, FixtureServer, assert_fixture_result


def names_for(mode: str) -> set[str]:
    return {"demo__lookup_record"} if mode == "tools" else {"weavz_search", "weavz_read_api", "weavz_execute"}


def run_agent(prompt: str, tools: list[object]) -> object:
    model_id = os.getenv("WEAVZ_MODEL")
    api_key = os.getenv("OPENAI_API_KEY")
    if not model_id or not api_key:
        raise RuntimeError("Set WEAVZ_MODEL and OPENAI_API_KEY for the optional CrewAI run")
    agent = Agent(
        role="Weavz MCP assistant",
        goal="Use the connected Weavz tools to answer the user's task accurately.",
        backstory="You use only the MCP tools connected for this run.",
        llm=model_id,
        tools=tools,
        verbose=False,
    )
    task = Task(description=prompt, expected_output="A concise answer grounded in tool results.", agent=agent)
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()


def exercise(mode: str, url: str, token: str, *, fixture: bool = False, prompt: str | None = None) -> None:
    config = MCPServerHTTP(url=url, headers={"Authorization": f"Bearer {token}"}, streamable=True)
    # CrewAI resolves this native MCPServerConfig into its MCPNativeTool objects.
    agent = Agent(
        role="Weavz MCP assistant",
        goal="Use the connected Weavz tools to answer the user's task accurately.",
        backstory="You use only the MCP tools connected for this run.",
        mcps=[config],
        verbose=False,
    )
    tools = agent.get_mcp_tools(agent.mcps)
    by_name = {getattr(tool, "_original_tool_name", tool.name): tool for tool in tools}
    names = set(by_name)
    if fixture and not names_for(mode).issubset(names):
        raise RuntimeError(f"Expected fixture tools {sorted(names_for(mode))}; got {sorted(names)}")
    if not fixture and prompt is None:
        print(json.dumps({"proof": "live Weavz MCP tool discovery", "mode": mode, "tools": sorted(names)}))
        return
    if prompt:
        print(run_agent(prompt, tools))
        return
    if mode == "tools":
        result = by_name["demo__lookup_record"].run(recordId="record-1")
        assert_fixture_result(mode, result)
        results = {"lookup": str(result)}
    else:
        search = by_name["weavz_search"].run(query="fixture")
        read_api = by_name["weavz_read_api"].run(alias="demo", action="lookup_record")
        result = by_name["weavz_execute"].run(code=CODE_EXAMPLE)
        assert_fixture_result(mode, search)
        assert_fixture_result(mode, result)
        if "demo" not in json.dumps(read_api, default=str):
            raise AssertionError(f"Unexpected demo API result: {read_api}")
        results = {"search": str(search), "read_api": str(read_api), "execute": str(result)}
    print(json.dumps({"proof": "local fixture CrewAI native tool calls", "mode": mode, "tools": sorted(names), "results": results}))
    agent._cleanup_mcp_clients()


def main() -> None:
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
            exercise(args.mode, fixture.url, "local-fixture-token", fixture=True)
    else:
        url, token = os.getenv("WEAVZ_MCP_URL"), os.getenv("WEAVZ_MCP_TOKEN")
        if not url or not token:
            raise SystemExit("Set WEAVZ_MCP_URL and WEAVZ_MCP_TOKEN from your custom Weavz setup")
        if token.startswith("wvz_"):
            raise SystemExit("WEAVZ_MCP_TOKEN must be an MCP access token, not a Weavz REST API key")
        parsed = urlparse(url)
        if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise SystemExit("Use an HTTPS MCP URL except for loopback development")
        exercise(args.mode, url, token, prompt=args.prompt)


if __name__ == "__main__":
    main()
