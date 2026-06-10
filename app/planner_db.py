import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'planner.db')

def init_planner_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, subject TEXT, exam_date TEXT,
        hours_per_day REAL, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, title TEXT, subject TEXT, due_date TEXT,
        priority TEXT, status TEXT DEFAULT 'pending', created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mood_checkin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, mood TEXT, checkin_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS student_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recurring_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, title TEXT, subject TEXT, days TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS day_checkin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, rating INTEGER, mood TEXT,
        study_hours REAL, checkin_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS xp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, total_xp INTEGER DEFAULT 0, last_updated TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, name TEXT, earned_at TEXT,
        UNIQUE(username, name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS wellness (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, sleep_hours REAL, ate_healthy TEXT,
        water_glasses INTEGER, phone_hours REAL, exercised TEXT,
        stress_level INTEGER, focus_rating INTEGER,
        mental_note TEXT, wellness_date TEXT)''')
    conn.commit()
    conn.close()

# ── PROFILE ───────────────────────────────────────────────
def save_student_name(username, name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO student_profile (username, name) VALUES (?, ?)', (username, name))
    conn.commit()
    conn.close()

def get_student_name(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT name FROM student_profile WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except:
        conn.close()
        return None

# ── EXAMS ─────────────────────────────────────────────────
def add_exam(username, subject, exam_date, hours_per_day):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO exams (username, subject, exam_date, hours_per_day, created_at) VALUES (?, ?, ?, ?, ?)',
              (username, subject, exam_date, hours_per_day, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_all_exams(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, subject, exam_date, hours_per_day FROM exams WHERE username = ? ORDER BY exam_date ASC', (username,))
    result = c.fetchall()
    conn.close()
    return result

def delete_exam(exam_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
    conn.commit()
    conn.close()

# ── TASKS ─────────────────────────────────────────────────
def add_task(username, title, subject, due_date, priority):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO tasks (username, title, subject, due_date, priority, status, created_at) VALUES (?, ?, ?, ?, ?, "pending", ?)',
              (username, title, subject, due_date, priority, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_tasks(username, status=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks WHERE username = ? AND status = ? ORDER BY due_date ASC', (username, status))
    else:
        c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks WHERE username = ? ORDER BY due_date ASC', (username,))
    result = c.fetchall()
    conn.close()
    return result

def get_today_tasks(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks WHERE username = ? AND created_at = ? ORDER BY priority ASC', (username, today))
    result = c.fetchall()
    conn.close()
    return result

def complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = "done" WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# ── MOOD ──────────────────────────────────────────────────
def save_mood(username, mood):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('DELETE FROM mood_checkin WHERE username = ? AND checkin_date = ?', (username, today))
    if mood:
        c.execute('INSERT INTO mood_checkin (username, mood, checkin_date) VALUES (?, ?, ?)', (username, mood, today))
    conn.commit()
    conn.close()

def get_today_mood(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('SELECT mood FROM mood_checkin WHERE username = ? AND checkin_date = ?', (username, today))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_mood_last_7_days(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT mood, checkin_date FROM mood_checkin WHERE username = ? ORDER BY checkin_date DESC LIMIT 7', (username,))
    result = c.fetchall()
    conn.close()
    return result

# ── RECURRING ─────────────────────────────────────────────
def add_recurring_task(username, title, subject, days):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO recurring_tasks (username, title, subject, days) VALUES (?, ?, ?, ?)',
              (username, title, subject, ','.join(days)))
    conn.commit()
    conn.close()

def get_recurring_tasks(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT id, title, subject, days FROM recurring_tasks WHERE username = ?', (username,))
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []

def delete_recurring_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM recurring_tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# ── DAY CHECKIN ───────────────────────────────────────────
def save_day_checkin(username, rating, mood, study_hours, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM day_checkin WHERE username = ? AND checkin_date = ?', (username, date))
    c.execute('INSERT INTO day_checkin (username, rating, mood, study_hours, checkin_date) VALUES (?, ?, ?, ?, ?)',
              (username, rating, mood, study_hours, date))
    conn.commit()
    conn.close()

def get_day_checkin(username, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT rating, mood, study_hours FROM day_checkin WHERE username = ? AND checkin_date = ?', (username, date))
        result = c.fetchone()
        conn.close()
        return result
    except:
        conn.close()
        return None

def get_checkin_last_7_days(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT rating, mood, study_hours, checkin_date FROM day_checkin WHERE username = ? ORDER BY checkin_date DESC LIMIT 7', (username,))
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []

# ── XP ────────────────────────────────────────────────────
def get_xp(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT total_xp FROM xp WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0
    except:
        conn.close()
        return 0

def add_xp(username, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT total_xp FROM xp WHERE username = ?', (username,))
    result = c.fetchone()
    if result:
        c.execute('UPDATE xp SET total_xp = ?, last_updated = ? WHERE username = ?',
                  (result[0] + amount, datetime.now().strftime("%Y-%m-%d"), username))
    else:
        c.execute('INSERT INTO xp (username, total_xp, last_updated) VALUES (?, ?, ?)',
                  (username, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_streak(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT checkin_date FROM day_checkin WHERE username = ? ORDER BY checkin_date DESC', (username,))
        dates = [row[0] for row in c.fetchall()]
        conn.close()
        if not dates:
            return 0
        streak = 0
        current = datetime.now().date()
        for d in dates:
            checkin = datetime.strptime(d, "%Y-%m-%d").date()
            if (current - checkin).days == streak:
                streak += 1
            else:
                break
        return streak
    except:
        conn.close()
        return 0

def get_badges(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT name, earned_at FROM badges WHERE username = ?', (username,))
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []

def award_badge(username, name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO badges (username, name, earned_at) VALUES (?, ?, ?)',
                  (username, name, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
    except:
        pass
    conn.close()

# ── WELLNESS ──────────────────────────────────────────────
def save_wellness(username, sleep_hours, ate_healthy, water_glasses, phone_hours, exercised, stress_level, focus_rating, mental_note, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM wellness WHERE username = ? AND wellness_date = ?', (username, date))
    c.execute('INSERT INTO wellness (username, sleep_hours, ate_healthy, water_glasses, phone_hours, exercised, stress_level, focus_rating, mental_note, wellness_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (username, sleep_hours, ate_healthy, water_glasses, phone_hours, exercised, stress_level, focus_rating, mental_note, date))
    conn.commit()
    conn.close()

def get_today_wellness(username, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT sleep_hours, ate_healthy, water_glasses, phone_hours, exercised, stress_level, focus_rating, mental_note FROM wellness WHERE username = ? AND wellness_date = ?', (username, date))
        result = c.fetchone()
        conn.close()
        return result
    except:
        conn.close()
        return None

def get_wellness_last_7_days(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT sleep_hours, ate_healthy, water_glasses, phone_hours, exercised, stress_level, focus_rating, wellness_date FROM wellness WHERE username = ? ORDER BY wellness_date DESC LIMIT 7', (username,))
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []