"""Generate a deterministic Markdown audit summary from synthetic records."""

from collections import Counter
from datetime import date


def markdown_report(records: list[dict[str, str]], report_date: date) -> str:
    counts = Counter(row.get("status", "unknown") for row in records)
    lines = [f"# Audit report — {report_date.isoformat()}", "", f"Total records: {len(records)}", ""]
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: {count}")
    return "\n".join(lines) + "\n"

