#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"
[[ -x "$PYTHON" ]] || { echo 'Run scripts/setup.sh first.' >&2; exit 1; }
exec "$PYTHON" "$ROOT/scripts/run-showcase.py" "$@"
