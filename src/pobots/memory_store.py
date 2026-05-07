from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class MemoryLesson:
    category: str
    problem: str
    solution: str
    result: str
    confidence: float = 0.7


def ensure_memory_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project TEXT NOT NULL,
                sprint TEXT NOT NULL,
                category TEXT NOT NULL,
                problem TEXT NOT NULL,
                solution TEXT NOT NULL,
                result TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_name TEXT NOT NULL,
                project TEXT NOT NULL,
                task TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def record_run(db_path: Path, *, run_name: str, project: str, task: str, score: int) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO runs (run_name, project, task, score) VALUES (?, ?, ?, ?)",
            (run_name, project, task, int(score)),
        )
        conn.commit()


def add_lessons(db_path: Path, *, project: str, sprint: str, lessons: Iterable[MemoryLesson]) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            """
            INSERT INTO lessons (project, sprint, category, problem, solution, result, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (project, sprint, item.category, item.problem, item.solution, item.result, float(item.confidence))
                for item in lessons
            ],
        )
        conn.commit()


def fetch_relevant_lessons(db_path: Path, *, task: str, limit: int = 5) -> List[MemoryLesson]:
    tokens = [token.strip().lower() for token in task.split() if len(token.strip()) >= 4]
    if not tokens:
        tokens = ["projeto"]

    where = " OR ".join(["LOWER(problem) LIKE ?" for _ in tokens])
    params = [f"%{token}%" for token in tokens]

    query = f"""
        SELECT category, problem, solution, result, confidence
        FROM lessons
        WHERE {where}
        ORDER BY confidence DESC, id DESC
        LIMIT ?
    """
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(query, (*params, int(limit))).fetchall()

    return [
        MemoryLesson(
            category=row[0],
            problem=row[1],
            solution=row[2],
            result=row[3],
            confidence=float(row[4]),
        )
        for row in rows
    ]
