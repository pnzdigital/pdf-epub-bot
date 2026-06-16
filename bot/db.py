import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.getenv("DB_PATH", "/bots/volumes/pdf-epub-bot/data.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            credits INTEGER DEFAULT 0,
            plan_type TEXT,
            plan_expires DATE,
            default_language TEXT DEFAULT 'pt-BR',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ignore_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            credits_used INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_user(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(user_id: int, plan_type: str, credits: int, expires_days: int = 30):
    conn = get_conn()
    cursor = conn.cursor()
    expires = (datetime.now() + timedelta(days=expires_days)).date().isoformat()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, credits, plan_type, plan_expires)
        VALUES (?, ?, ?, ?)
    """, (user_id, credits, plan_type, expires))
    conn.commit()
    conn.close()


def update_credits(user_id: int, credits: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = ? WHERE user_id = ?", (credits, user_id))
    conn.commit()
    conn.close()


def get_ignore_words(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM ignore_words WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [r["word"] for r in rows]


def add_ignore_word(user_id: int, word: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ignore_words (user_id, word) VALUES (?, ?)",
        (user_id, word)
    )
    conn.commit()
    conn.close()


def remove_ignore_word(user_id: int, word: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM ignore_words WHERE user_id = ? AND word = ?",
        (user_id, word)
    )
    conn.commit()
    conn.close()


def clear_ignore_words(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ignore_words WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_to_queue(user_id: int, file_name: str, file_path: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO queue (user_id, file_name, file_path, status)
        VALUES (?, ?, ?, 'pending')
    """, (user_id, file_name, file_path))
    conn.commit()
    conn.close()


def get_queue(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM queue WHERE user_id = ? AND status = 'pending' ORDER BY created_at",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_queue_status(queue_id: int, status: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE queue SET status = ? WHERE id = ?", (status, queue_id))
    conn.commit()
    conn.close()


def clear_queue(user_id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM queue WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def add_transaction(user_id: int, action: str, credits_used: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, action, credits_used)
        VALUES (?, ?, ?)
    """, (user_id, action, credits_used))
    conn.commit()
    conn.close()


def update_user_language(user_id: int, language: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET default_language = ? WHERE user_id = ?",
        (language, user_id)
    )
    conn.commit()
    conn.close()
