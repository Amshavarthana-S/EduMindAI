import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'chat_history.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, session_id TEXT, role TEXT,
        content TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        username TEXT, title TEXT, created_at TEXT)''')
    conn.commit()
    conn.close()

def save_message(username, session_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, session_id, role, content, timestamp) VALUES (?, ?, ?, ?, ?)',
              (username, session_id, role, content, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def save_session(username, session_id, title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO sessions (session_id, username, title, created_at) VALUES (?, ?, ?, ?)',
              (session_id, username, title, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_all_sessions(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT session_id, title, created_at FROM sessions WHERE username = ? ORDER BY created_at DESC', (username,))
    result = c.fetchall()
    conn.close()
    return result

def get_session_messages(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY id', (session_id,))
    result = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in result]

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
    c.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()
    conn.close()