"""Persistent storage service using SQLite for EduGenie history, quizzes, and progress metrics."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from config import settings


class StorageService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = str(db_path or settings.DATABASE_PATH)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for concurrency and performance
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # Table for all learning activities (Q&A, Explanations, Summaries, Learning Paths)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id TEXT PRIMARY KEY,
                    activity_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subtitle TEXT,
                    payload TEXT NOT NULL,
                    score REAL,
                    accuracy REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Table for Quizzes with question cache and evaluation state
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    quiz_id TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    num_questions INTEGER NOT NULL,
                    questions_json TEXT NOT NULL,
                    user_answers_json TEXT,
                    score REAL,
                    accuracy REAL,
                    is_completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Index for fast filtering and ordering
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(activity_type);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_activities_date ON activities(created_at DESC);")
            conn.commit()

    def record_activity(
        self,
        activity_type: str,
        title: str,
        payload: Dict[str, Any],
        subtitle: Optional[str] = None,
        score: Optional[float] = None,
        accuracy: Optional[float] = None,
    ) -> str:
        activity_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO activities (id, activity_type, title, subtitle, payload, score, accuracy, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    activity_id,
                    activity_type,
                    title[:250],
                    (subtitle or "")[:250],
                    json.dumps(payload),
                    score,
                    accuracy,
                    created_at,
                ),
            )
            conn.commit()
        return activity_id

    def get_activities(
        self,
        activity_type: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        query = "SELECT id, activity_type, title, subtitle, payload, score, accuracy, created_at FROM activities WHERE 1=1"
        params: List[Any] = []

        if activity_type and activity_type != "all":
            query += " AND activity_type = ?"
            params.append(activity_type)

        if search_query:
            query += " AND (title LIKE ? OR subtitle LIKE ?)"
            wildcard = f"%{search_query.strip()}%"
            params.extend([wildcard, wildcard])

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            results = []
            for row in rows:
                try:
                    payload = json.loads(row["payload"])
                except Exception:
                    payload = {}
                results.append({
                    "id": row["id"],
                    "activity_type": row["activity_type"],
                    "title": row["title"],
                    "subtitle": row["subtitle"],
                    "payload": payload,
                    "score": row["score"],
                    "accuracy": row["accuracy"],
                    "created_at": row["created_at"],
                })
            return results

    def get_activity_by_id(self, activity_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM activities WHERE id = ?", (activity_id,)).fetchone()
            if not row:
                return None
            try:
                payload = json.loads(row["payload"])
            except Exception:
                payload = {}
            return {
                "id": row["id"],
                "activity_type": row["activity_type"],
                "title": row["title"],
                "subtitle": row["subtitle"],
                "payload": payload,
                "score": row["score"],
                "accuracy": row["accuracy"],
                "created_at": row["created_at"],
            }

    def delete_activity(self, activity_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_activities(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM activities;")
            conn.commit()
            return cursor.rowcount

    # ---------------- Quiz Storage ----------------
    def store_quiz(
        self,
        quiz_id: str,
        topic: str,
        difficulty: str,
        num_questions: int,
        questions: List[Dict[str, Any]],
    ):
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO quizzes (quiz_id, topic, difficulty, num_questions, questions_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    quiz_id,
                    topic,
                    difficulty,
                    num_questions,
                    json.dumps(questions),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()

    def get_quiz(self, quiz_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM quizzes WHERE quiz_id = ?", (quiz_id,)).fetchone()
            if not row:
                return None
            try:
                questions = json.loads(row["questions_json"])
            except Exception:
                questions = []
            return {
                "quiz_id": row["quiz_id"],
                "topic": row["topic"],
                "difficulty": row["difficulty"],
                "num_questions": row["num_questions"],
                "questions": questions,
                "score": row["score"],
                "accuracy": row["accuracy"],
                "is_completed": bool(row["is_completed"]),
                "created_at": row["created_at"],
            }

    def complete_quiz(
        self,
        quiz_id: str,
        user_answers: Dict[int, str],
        score: float,
        accuracy: float,
    ):
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE quizzes
                SET user_answers_json = ?, score = ?, accuracy = ?, is_completed = 1
                WHERE quiz_id = ?
                """,
                (json.dumps(user_answers), score, accuracy, quiz_id),
            )
            conn.commit()

    # ---------------- Real Analytics & Progress Metrics ----------------
    def get_progress_metrics(self) -> Dict[str, Any]:
        """Calculates authentic, real-time learning metrics strictly from the database."""
        with self._get_connection() as conn:
            # Count activities per type
            counts = {
                "qa": 0,
                "explain": 0,
                "quiz": 0,
                "summary": 0,
                "learning_path": 0,
            }
            rows = conn.execute(
                "SELECT activity_type, COUNT(*) as cnt FROM activities GROUP BY activity_type"
            ).fetchall()
            for r in rows:
                if r["activity_type"] in counts:
                    counts[r["activity_type"]] = r["cnt"]

            total_activities = sum(counts.values())

            # Real quiz accuracy average
            quiz_acc_row = conn.execute(
                "SELECT AVG(accuracy) as avg_acc, COUNT(*) as comp_cnt FROM activities WHERE activity_type = 'quiz' AND accuracy IS NOT NULL"
            ).fetchone()
            avg_accuracy = round(quiz_acc_row["avg_acc"], 1) if quiz_acc_row and quiz_acc_row["avg_acc"] is not None else 0.0

            # Weekly learning activity (last 7 days counts)
            weekly_data = []
            today = datetime.now(timezone.utc).date()
            for i in range(6, -1, -1):
                day = today - timedelta(days=i)
                day_str = day.strftime("%Y-%m-%d")
                day_label = day.strftime("%a")  # Mon, Tue, etc.
                cnt_row = conn.execute(
                    "SELECT COUNT(*) as day_cnt FROM activities WHERE DATE(created_at) = ?",
                    (day_str,),
                ).fetchone()
                day_count = cnt_row["day_cnt"] if cnt_row else 0
                weekly_data.append({
                    "date": day_str,
                    "day": day_label,
                    "count": day_count,
                })

            # Fetch recent 5 activities
            recent_rows = conn.execute(
                "SELECT id, activity_type, title, subtitle, created_at, score, accuracy FROM activities ORDER BY created_at DESC LIMIT 5"
            ).fetchall()
            recent_activities = [
                {
                    "id": r["id"],
                    "activity_type": r["activity_type"],
                    "title": r["title"],
                    "subtitle": r["subtitle"],
                    "created_at": r["created_at"],
                    "score": r["score"],
                    "accuracy": r["accuracy"],
                }
                for r in recent_rows
            ]

            return {
                "total_activities": total_activities,
                "questions_asked": counts["qa"],
                "concepts_explained": counts["explain"],
                "quizzes_completed": counts["quiz"],
                "average_quiz_accuracy": avg_accuracy,
                "summaries_generated": counts["summary"],
                "learning_paths_created": counts["learning_path"],
                "weekly_activity": weekly_data,
                "recent_activities": recent_activities,
            }


storage = StorageService()
