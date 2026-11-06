"""Build reviewable change plans without connecting to external systems."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Change:
    customer_id: str
    field: str
    before: str
    after: str
    status: str = "PENDING_APPROVAL"


def plan(records: list[dict[str, str]]) -> list[Change]:
    changes: list[Change] = []
    for row in records:
        if row.get("state") in {"cancelled", "ambiguous"}:
            continue
        if row.get("observed") != row.get("expected"):
            changes.append(Change(
                customer_id=str(row["customer_id"]),
                field=str(row["field"]),
                before=str(row.get("observed", "")),
                after=str(row.get("expected", "")),
            ))
    return sorted(changes, key=lambda item: (item.customer_id, item.field))


def write_dry_run(changes: list[Change], destination: Path) -> None:
    destination.write_text(json.dumps([asdict(item) for item in changes], indent=2), encoding="utf-8")

