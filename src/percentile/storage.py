from __future__ import annotations

from contextlib import closing
from datetime import datetime
import json
import os
from pathlib import Path
import sqlite3
from typing import Iterable

from .models import ErrorCause
from .questions import QUESTION_BY_ID


def default_db_path() -> Path:
    configured = os.getenv("PERCENTILE_DB")
    if configured:
        return Path(configured)
    return Path("data/percentile.db")


class Store:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else default_db_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self):
        return sqlite3.connect(self.path)

    def _init(self) -> None:
        with closing(self.connect()) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    selected_index INTEGER NOT NULL,
                    correct INTEGER NOT NULL,
                    response_seconds REAL NOT NULL,
                    confidence REAL,
                    error_cause TEXT,
                    skill_ids TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS recognition_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    selected_archetype_id TEXT NOT NULL,
                    correct INTEGER NOT NULL,
                    response_seconds REAL NOT NULL,
                    confidence REAL
                );

                CREATE TABLE IF NOT EXISTS mocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    name TEXT NOT NULL,
                    total_score INTEGER,
                    quant_score INTEGER,
                    verbal_score INTEGER,
                    di_score INTEGER,
                    notes TEXT
                );
                """
            )
            conn.commit()

    def save_attempt(
        self,
        *,
        question_id: str,
        selected_index: int,
        correct: bool,
        response_seconds: float,
        confidence: float | None,
        error_cause: ErrorCause | None,
    ) -> None:
        q = QUESTION_BY_ID[question_id]
        with closing(self.connect()) as conn:
            conn.execute(
                """
                INSERT INTO attempts (
                    created_at, question_id, selected_index, correct,
                    response_seconds, confidence, error_cause, skill_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(),
                    question_id,
                    selected_index,
                    int(correct),
                    response_seconds,
                    confidence,
                    error_cause.value if error_cause else None,
                    json.dumps(q.skill_ids),
                ),
            )
            conn.commit()

    def skill_stats(self) -> dict[str, dict[str, float]]:
        stats: dict[str, dict[str, float]] = {}
        with closing(self.connect()) as conn:
            rows = conn.execute(
                "SELECT correct, response_seconds, error_cause, skill_ids FROM attempts"
            ).fetchall()

        for correct, seconds, error_cause, skill_ids_json in rows:
            for skill_id in json.loads(skill_ids_json):
                row = stats.setdefault(skill_id, {"attempts": 0.0, "correct": 0.0, "errors": 0.0, "slow": 0.0})
                row["attempts"] += 1
                row["correct"] += int(correct)
                row["errors"] += int(not correct)
                row["slow"] += int(seconds > 120)
        return stats

    def attempt_summary(self) -> dict[str, float | int]:
        with closing(self.connect()) as conn:
            attempts, correct, avg_seconds = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(correct), 0), COALESCE(AVG(response_seconds), 0) FROM attempts"
            ).fetchone()
        return {
            "attempts": attempts,
            "accuracy": (correct / attempts) if attempts else 0.0,
            "avg_seconds": float(avg_seconds or 0.0),
        }

    def save_recognition_attempt(
        self,
        *,
        question_id: str,
        selected_archetype_id: str,
        correct: bool,
        response_seconds: float,
        confidence: float | None,
    ) -> None:
        with closing(self.connect()) as conn:
            conn.execute(
                """
                INSERT INTO recognition_attempts (
                    created_at, question_id, selected_archetype_id, correct,
                    response_seconds, confidence
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(),
                    question_id,
                    selected_archetype_id,
                    int(correct),
                    response_seconds,
                    confidence,
                ),
            )
            conn.commit()

    def recognition_summary(self) -> dict[str, float | int]:
        with closing(self.connect()) as conn:
            attempts, correct, avg_seconds = conn.execute(
                "SELECT COUNT(*), COALESCE(SUM(correct), 0), COALESCE(AVG(response_seconds), 0) FROM recognition_attempts"
            ).fetchone()
        return {
            "attempts": attempts,
            "accuracy": (correct / attempts) if attempts else 0.0,
            "avg_seconds": float(avg_seconds or 0.0),
        }

    def save_mock(
        self,
        *,
        name: str,
        total_score: int | None,
        quant_score: int | None,
        verbal_score: int | None,
        di_score: int | None,
        notes: str | None,
    ) -> None:
        with closing(self.connect()) as conn:
            conn.execute(
                """
                INSERT INTO mocks (created_at, name, total_score, quant_score, verbal_score, di_score, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (datetime.utcnow().isoformat(), name, total_score, quant_score, verbal_score, di_score, notes),
            )
            conn.commit()

    def latest_mock(self) -> dict[str, object] | None:
        with closing(self.connect()) as conn:
            row = conn.execute(
                """
                SELECT created_at, name, total_score, quant_score, verbal_score, di_score, notes
                FROM mocks ORDER BY id DESC LIMIT 1
                """
            ).fetchone()
        if row is None:
            return None
        keys = ("created_at", "name", "total_score", "quant_score", "verbal_score", "di_score", "notes")
        return dict(zip(keys, row))
