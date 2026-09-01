"""
query_logger.py

Basic per-query logging for the Policy DB Chatbot (PCOIS2-57).

Logs every question asked and answer given (timestamp, question,
retrieved chunks, final answer) to a local SQLite database. This is
the first piece of the audit-log requirement from the original
project proposal ("Log queries for quality assurance and continuous
improvement").

Why SQLite:
- It's a single file (policy_query_logs.db) - no separate DB server
  to set up, satisfies "somewhere simple like a file or database
  table" directly from the ticket description.
- Still queryable with SQL, so it's easy to build QA/reporting on
  top of it later without changing storage.

Usage (drop this file into your backend, next to your API code):

    from query_logger import log_query

    # inside your RAG endpoint handler, after you have the answer:
    log_query(
        question=user_question,
        retrieved_chunks=retrieved_chunks,   # list[str] or list[dict]
        final_answer=answer_text,
    )

See integration_examples.py for FastAPI / Flask snippets.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# DB file lives next to this module by default. Override by passing
# db_path=... to QueryLogger(), or by setting the module-level DB_PATH
# before the first call if you're using the module-level log_query().
DB_PATH = Path(__file__).parent / "policy_query_logs.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS query_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc   TEXT    NOT NULL,
    question        TEXT    NOT NULL,
    retrieved_chunks TEXT   NOT NULL,   -- JSON-encoded list
    final_answer    TEXT    NOT NULL,
    metadata        TEXT                -- JSON-encoded dict, optional extra context
);
"""

_INSERT = """
INSERT INTO query_logs (timestamp_utc, question, retrieved_chunks, final_answer, metadata)
VALUES (?, ?, ?, ?, ?);
"""

_lock = threading.Lock()


@dataclass
class QueryLogEntry:
    id: int
    timestamp_utc: str
    question: str
    retrieved_chunks: list
    final_answer: str
    metadata: Optional[dict]


class QueryLogger:
    """Thread-safe SQLite-backed logger for chatbot queries."""

    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_SCHEMA)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def log_query(
        self,
        question: str,
        retrieved_chunks: Iterable[Any],
        final_answer: str,
        metadata: Optional[dict] = None,
    ) -> int:
        """
        Record one question/answer interaction.

        Args:
            question: The user's raw question text.
            retrieved_chunks: Whatever your retriever returned - a list of
                strings, or a list of dicts like
                {"source": "Leave Policy", "text": "...", "score": 0.82}.
                Anything JSON-serialisable is fine.
            final_answer: The final answer text shown to the user
                (including citations, if you keep them inline).
            metadata: Optional extra context you want alongside the log,
                e.g. {"user_role": "student", "latency_ms": 812,
                "confidence": "high"}.

        Returns:
            The row id of the inserted log entry.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        chunks_json = json.dumps(_to_jsonable(retrieved_chunks))
        metadata_json = json.dumps(metadata) if metadata else None

        with _lock, self._connect() as conn:
            cursor = conn.execute(
                _INSERT,
                (timestamp, question, chunks_json, final_answer, metadata_json),
            )
            return cursor.lastrowid

    def get_logs(self, limit: int = 50) -> list[QueryLogEntry]:
        """Return the most recent `limit` logs, newest first."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM query_logs ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()

        return [
            QueryLogEntry(
                id=row["id"],
                timestamp_utc=row["timestamp_utc"],
                question=row["question"],
                retrieved_chunks=json.loads(row["retrieved_chunks"]),
                final_answer=row["final_answer"],
                metadata=json.loads(row["metadata"]) if row["metadata"] else None,
            )
            for row in rows
        ]


def _to_jsonable(chunks: Iterable[Any]) -> list:
    """Best-effort conversion of retrieved chunks to JSON-serialisable data."""
    result = []
    for c in chunks:
        if isinstance(c, (str, int, float, bool, type(None))):
            result.append(c)
        elif isinstance(c, dict):
            result.append(c)
        elif hasattr(c, "__dict__"):
            result.append(vars(c))
        else:
            result.append(str(c))
    return result


# ---------------------------------------------------------------------------
# Module-level convenience API - the simplest way to use this from an
# endpoint handler without instantiating anything yourself.
# ---------------------------------------------------------------------------

_default_logger: Optional[QueryLogger] = None


def _get_default_logger() -> QueryLogger:
    global _default_logger
    if _default_logger is None:
        _default_logger = QueryLogger(DB_PATH)
    return _default_logger


def log_query(
    question: str,
    retrieved_chunks: Iterable[Any],
    final_answer: str,
    metadata: Optional[dict] = None,
) -> int:
    """Convenience wrapper around QueryLogger().log_query() using a shared,
    lazily-created default logger writing to DB_PATH."""
    return _get_default_logger().log_query(
        question, retrieved_chunks, final_answer, metadata
    )


def get_logs(limit: int = 50) -> list[QueryLogEntry]:
    """Convenience wrapper to fetch recent logs from the default logger."""
    return _get_default_logger().get_logs(limit)


if __name__ == "__main__":
    # Quick manual smoke test: python query_logger.py
    log_query(
        question="How many days of annual leave am I entitled to?",
        retrieved_chunks=[
            {"source": "Leave Policy s.4.2", "text": "Full-time staff accrue..."},
            {"source": "Leave Policy s.4.5", "text": "Leave carries over..."},
        ],
        final_answer="Full-time staff accrue 20 days annual leave per year [Leave Policy s.4.2].",
        metadata={"confidence": "high"},
    )
    for entry in get_logs(limit=5):
        print(entry)
