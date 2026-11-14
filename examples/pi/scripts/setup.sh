#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
python3 -m unittest discover -s tests -v
export PI_CODING_AGENT_DIR="$root/.local/pi"
pi mcp login weavz
