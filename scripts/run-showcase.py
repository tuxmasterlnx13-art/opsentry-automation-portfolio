"""Run the vendor-neutral OPSENTRY examples with synthetic data only."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run() -> dict:
    ip_guard = load("showcase_ip_guard", "projects/ip-autofix/demo/ip_guard.py")
    planner = load("showcase_change_planner", "projects/router-serial-automation/demo/change_planner.py")
    queue = load("showcase_queue", "projects/automation-orchestrator/demo/queue.py")
    report = load("showcase_report", "projects/audit-reporting/demo/report.py")

    ip_plan = ip_guard.build_plan([
        ip_guard.Candidate("CUSTOMER-001", "100.64.0.10", "100.64.0.20"),
        ip_guard.Candidate("CUSTOMER-002", "100.64.0.11", "203.0.113.8"),
    ])
    changes = planner.plan([
        {"customer_id": "CUSTOMER-001", "field": "router", "observed": "MODEL-A", "expected": "MODEL-B", "state": "active"},
        {"customer_id": "CUSTOMER-002", "field": "serial", "observed": "OLD", "expected": "NEW", "state": "cancelled"},
    ])
    with tempfile.TemporaryDirectory(prefix="opsentry-showcase-") as temporary:
        work = queue.WorkQueue(Path(temporary) / "queue.sqlite3")
        work.add("AUDIT-001")
        claimed = work.claim("demo-worker")
        completed = bool(claimed and work.complete(claimed, "demo-worker"))

    markdown = report.markdown_report(
        [{"status": "resolved"}, {"status": "pending"}, {"status": "resolved"}],
        date(2026, 1, 1),
    )
    return {
        "ip_plan": [item.__dict__ for item in ip_plan],
        "reviewable_changes": [item.__dict__ for item in changes],
        "queue": {"claimed": claimed, "completed": completed},
        "report": markdown,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without verbose output")
    args = parser.parse_args()
    result = run()
    if not result["queue"]["completed"] or len(result["ip_plan"]) != 2 or len(result["reviewable_changes"]) != 1:
        raise RuntimeError("showcase validation failed")
    if args.check:
        print("SHOWCASE_OK")
    else:
        print("OPSENTRY synthetic showcase")
        print("=" * 28)
        print(json.dumps({key: value for key, value in result.items() if key != "report"}, indent=2))
        print("\nGenerated report:\n")
        print(result["report"], end="")
        print("\nNo external service was contacted and no production write was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
