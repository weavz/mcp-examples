from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import exercise
from fixture.harness import FixtureServer


@pytest.mark.parametrize("mode", ["tools", "code"])
def test_actual_mcp_adapter_calls_local_fixture(mode: str) -> None:
    async def run() -> None:
        with FixtureServer(mode) as fixture:
            fixture.reject_bad_token()
            await exercise(mode, fixture.url, "local-fixture-token", fixture=True)

    asyncio.run(run())
