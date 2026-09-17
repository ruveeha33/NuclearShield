from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def db_path() -> Path:
    root = Path(os.getenv("NUCLEARSHIELD_DATA_DIR", "data"))
    root.mkdir(parents=True, exist_ok=True)
    return root / "nuclearshield.db"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(db_path())
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS audit (
        id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, action TEXT NOT NULL,
        actor TEXT NOT NULL, evidence_digest TEXT NOT NULL, details TEXT NOT NULL)""")
    connection.execute("""CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY, created_at TEXT NOT NULL, filename TEXT NOT NULL,
        evidence_digest TEXT NOT NULL, event_count INTEGER NOT NULL,
        finding_count INTEGER NOT NULL, payload TEXT NOT NULL)""")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit(timestamp)")
    connection.execute("PRAGMA optimize")
    return connection


def append_audit(action: str, digest: str, details: dict) -> dict:
    entry = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "actor": "single-student-demo",
        "evidence_digest": digest,
        "details": details,
    }
    with connect() as connection:
        connection.execute(
            "INSERT INTO audit VALUES (?, ?, ?, ?, ?, ?)",
            (entry["id"], entry["timestamp"], action, entry["actor"], digest, json.dumps(details)),
        )
    return entry


def recent_audit(limit: int = 50) -> list[dict]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM audit ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return [{**dict(row), "details": json.loads(row["details"])} for row in rows]


def save_analysis(
    filename: str,
    evidence_digest: str,
    events: list,
    findings: list,
    summary: dict | None = None,
    rejected: list | None = None,
) -> dict:
    analysis_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "events": events,
        "findings": findings,
        "summary": summary or {},
        "rejected": rejected or [],
    }
    with connect() as connection:
        connection.execute(
            "INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                analysis_id,
                created_at,
                filename,
                evidence_digest,
                len(events),
                len(findings),
                json.dumps(payload),
            ),
        )
    return {
        "id": analysis_id,
        "created_at": created_at,
        "filename": filename,
        "digest": evidence_digest,
        "event_count": len(events),
        "finding_count": len(findings),
        **payload,
    }


def list_analyses(limit: int = 30) -> list[dict]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, created_at, filename, evidence_digest, event_count, finding_count FROM analyses ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "created_at": row["created_at"],
            "filename": row["filename"],
            "digest": row["evidence_digest"],
            "event_count": row["event_count"],
            "finding_count": row["finding_count"],
        }
        for row in rows
    ]


def get_analysis(analysis_id: str | None = None) -> dict | None:
    with connect() as connection:
        if analysis_id:
            row = connection.execute(
                "SELECT * FROM analyses WHERE id = ?", (analysis_id,)
            ).fetchone()
        else:
            row = connection.execute(
                "SELECT * FROM analyses ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
    if not row:
        return None
    payload = json.loads(row["payload"])
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "filename": row["filename"],
        "digest": row["evidence_digest"],
        "event_count": row["event_count"],
        "finding_count": row["finding_count"],
        **payload,
    }
