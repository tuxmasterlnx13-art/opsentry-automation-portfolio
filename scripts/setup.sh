#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$ROOT/.venv"
fi

"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/projects/operations-dashboard/demo/requirements.txt"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/projects/fraudguard-community/demo/requirements.txt"
"$ROOT/scripts/test-all.sh"

printf '\nOPSENTRY is ready.\nRun: ./scripts/run-showcase.sh\n'
printf 'GUI: .venv/bin/python projects/fraudguard-community/demo/run_fraudguard.py\n'
