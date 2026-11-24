#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON="${PYTHON_BIN:-python3}"
exec "$PYTHON" "$ROOT/scripts/download_guardian.py" --destination "${1:-downloads}"
