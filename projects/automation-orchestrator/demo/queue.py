"""Small SQLite work queue with atomic claims and explicit completion."""

from __future__ import annotations

from contextlib import closing
import sqlite3
from pathlib import Path


class WorkQueue:
    def __init__(self, database: Path):
        self.database = database
        with closing(self._connect()) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, state TEXT NOT NULL, worker TEXT)")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=10, isolation_level=None)
        connection.row_factory = sqlite3.Row
        return connection

    def add(self, job_id: str) -> None:
        with closing(self._connect()) as connection:
            connection.execute("INSERT OR IGNORE INTO jobs(id, state) VALUES (?, 'READY')", (job_id,))

    def claim(self, worker: str) -> str | None:
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT id FROM jobs WHERE state = 'READY' ORDER BY id LIMIT 1").fetchone()
            if row is None:
                connection.commit()
                return None
            connection.execute("UPDATE jobs SET state = 'CLAIMED', worker = ? WHERE id = ?", (worker, row["id"]))
            connection.commit()
            return str(row["id"])

    def complete(self, job_id: str, worker: str) -> bool:
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                "UPDATE jobs SET state = 'DONE' WHERE id = ? AND worker = ? AND state = 'CLAIMED'",
                (job_id, worker),
            )
            return cursor.rowcount == 1

