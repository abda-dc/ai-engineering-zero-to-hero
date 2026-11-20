import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import settings

def init_db():
    """Initializes the SQLite schema with tables for user progress and vectors."""
    db_path = settings.SQLITE_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.cursor()
        
        # Table: curriculum_progress
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS curriculum_progress (
                chapter_id TEXT PRIMARY KEY,
                completed BOOLEAN DEFAULT 0,
                quiz_score REAL DEFAULT 0.0,
                bookmarked BOOLEAN DEFAULT 0,
                notes TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table: vector_documents
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vector_documents (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                embedding_json TEXT NOT NULL,
                metadata_json TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

class ProgressRepository:
    @staticmethod
    def get_all_progress() -> Dict[str, Any]:
        with sqlite3.connect(str(settings.SQLITE_DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM curriculum_progress")
            rows = cursor.fetchall()
            return {
                row["chapter_id"]: {
                    "completed": bool(row["completed"]),
                    "quiz_score": float(row["quiz_score"]),
                    "bookmarked": bool(row["bookmarked"]),
                    "notes": row["notes"],
                    "updated_at": row["updated_at"]
                }
                for row in rows
            }

    @staticmethod
    def update_progress(chapter_id: str, completed: Optional[bool] = None, quiz_score: Optional[float] = None, bookmarked: Optional[bool] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        with sqlite3.connect(str(settings.SQLITE_DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM curriculum_progress WHERE chapter_id = ?", (chapter_id,))
            current = cursor.fetchone()
            
            new_completed = completed if completed is not None else (bool(current["completed"]) if current else False)
            new_score = quiz_score if quiz_score is not None else (float(current["quiz_score"]) if current else 0.0)
            new_bm = bookmarked if bookmarked is not None else (bool(current["bookmarked"]) if current else False)
            new_notes = notes if notes is not None else (current["notes"] if current else "")
            
            cursor.execute("""
                INSERT INTO curriculum_progress (chapter_id, completed, quiz_score, bookmarked, notes, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chapter_id) DO UPDATE SET
                    completed = excluded.completed,
                    quiz_score = excluded.quiz_score,
                    bookmarked = excluded.bookmarked,
                    notes = excluded.notes,
                    updated_at = CURRENT_TIMESTAMP
            """, (chapter_id, new_completed, new_score, new_bm, new_notes))
            
            conn.commit()
            
            return {
                "chapter_id": chapter_id,
                "completed": new_completed,
                "quiz_score": new_score,
                "bookmarked": new_bm,
                "notes": new_notes
            }

class VectorRepository:
    @staticmethod
    def upsert_vector(doc_id: str, content: str, embedding: List[float], metadata: Dict[str, Any] = None):
        with sqlite3.connect(str(settings.SQLITE_DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vector_documents (id, content, embedding_json, metadata_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    content = excluded.content,
                    embedding_json = excluded.embedding_json,
                    metadata_json = excluded.metadata_json
            """, (doc_id, content, json.dumps(embedding), json.dumps(metadata or {})))
            conn.commit()

    @staticmethod
    def get_all_vectors() -> List[Dict[str, Any]]:
        with sqlite3.connect(str(settings.SQLITE_DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, content, embedding_json, metadata_json FROM vector_documents")
            return [
                {
                    "id": row["id"],
                    "content": row["content"],
                    "embedding": json.loads(row["embedding_json"]),
                    "metadata": json.loads(row["metadata_json"])
                }
                for row in cursor.fetchall()
            ]
