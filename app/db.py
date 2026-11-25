"""SQLite helper. OWNER: Role 4."""
import json
import sqlite3
from pathlib import Path

from app.config import Config

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / Config.DATABASE_PATH


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        language TEXT, target_text TEXT, overall_score REAL, result_json TEXT)""")
    return conn


def save_attempt(result: dict):
    with get_conn() as c:
        c.execute("INSERT INTO attempts (language, target_text, overall_score, result_json) VALUES (?,?,?,?)",
                  (result["language"], result["target_text"], result["overall_score"], json.dumps(result)))


def list_attempts(limit=50):
    with get_conn() as c:
        rows = c.execute("SELECT id, created_at, language, target_text, overall_score FROM attempts "
                         "ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]
