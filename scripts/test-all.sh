#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"

[[ -x "$PYTHON" ]] || { echo 'Run scripts/setup.sh first.' >&2; exit 1; }

for demo in "$ROOT"/projects/*/demo; do
  [[ -d "$demo" ]] || continue
  echo "Testing $(basename "$(dirname "$demo")")..."
  (cd "$demo" && "$PYTHON" -m unittest discover -v)
done

"$PYTHON" "$ROOT/scripts/run-showcase.py" --check
echo 'All public tests passed.'
