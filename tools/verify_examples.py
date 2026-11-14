"""Install and exercise each example from an independent, clean source copy."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".venv", "node_modules", "dist", "__pycache__", ".pytest_cache", ".local"}


def ignore(directory: str, names: list[str]) -> list[str]:
    return [name for name in names if name in EXCLUDED or (name.startswith(".env") and name != ".env.example") or name.endswith(".log")]


def commands(entry: dict) -> list[list[str]]:
    if entry["category"] == "client":
        result = [["bash", "scripts/validate.sh"]]
        if entry["id"] == "opencode": result.append(["bash", "scripts/test-native.sh"])
        return result
    if entry["language"] == "typescript":
        return [["npm", "ci", "--no-audit", "--no-fund"], ["npm", "run", "build"], ["npm", "test"], ["npm", "run", "smoke", "--", "--fixture", "--mode", "tools"], ["npm", "run", "smoke", "--", "--fixture", "--mode", "code"]]
    return [["uv", "sync", "--locked"], ["uv", "run", "pytest"], ["uv", "run", "python", "main.py", "--fixture", "--mode", "tools"], ["uv", "run", "python", "main.py", "--fixture", "--mode", "code"]]


def verify(entry: dict, logs: Path) -> dict:
    identifier = entry["id"]
    result = {"id": identifier, "repository": entry["repository"], "checks": [], "liveAccountVerified": False}
    log_path = logs / f"{identifier}.log"
    with tempfile.TemporaryDirectory(prefix=f"weavz-{identifier}-") as temporary:
        target = Path(temporary) / "example"
        shutil.copytree(ROOT / entry["path"], target, ignore=ignore)
        # Preserve the provider-free contract even when the operator has keys in
        # their shell. The fixtures must never make a paid inference request.
        env = {key: value for key, value in os.environ.items() if key not in {"OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY", "WEAVZ_API_KEY", "WEAVZ_MCP_TOKEN", "WEAVZ_MCP_URL", "WEAVZ_MODEL"}}
        with log_path.open("w") as log:
            for command in commands(entry):
                log.write("$ " + " ".join(command) + "\n"); log.flush()
                try:
                    process = subprocess.run(command, cwd=target, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=600)
                    code = process.returncode
                except subprocess.TimeoutExpired:
                    code = 124
                result["checks"].append({"command": " ".join(command), "exitCode": code})
                if code:
                    result["status"] = "failed"; break
            else:
                result["status"] = "passed"
    result["scope"] = "static client contract" if entry["category"] == "client" and identifier != "opencode" else "native MCP synthetic fixture"
    print(f"{identifier}: {result['status']}", flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--logs", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    args.logs.mkdir(parents=True, exist_ok=True)
    entries = json.loads((ROOT / "catalog.json").read_text())["examples"]
    selected = [entry for entry in entries if not args.ids or entry["id"] in args.ids]
    missing = [entry["id"] for entry in selected if not (ROOT / entry["path"] / "README.md").is_file()]
    if missing: raise SystemExit(f"Missing example source: {', '.join(missing)}")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda entry: verify(entry, args.logs), selected))
    receipt = {"checkedAt": datetime.now(timezone.utc).isoformat(), "examples": results}
    (args.logs / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    raise SystemExit(any(result["status"] != "passed" for result in results))
