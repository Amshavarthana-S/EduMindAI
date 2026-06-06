import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'planner.db')

def init_planner_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            exam_date TEXT,
            hours_per_day REAL,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subject TEXT,
            due_date TEXT,
            priority TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS mood_checkin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            checkin_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_exam(subject, exam_date, hours_per_day):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO exams (subject, exam_date, hours_per_day, created_at)
        VALUES (?, ?, ?, ?)
    ''', (subject, exam_date, hours_per_day, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_all_exams():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, subject, exam_date, hours_per_day FROM exams ORDER BY exam_date ASC')
    exams = c.fetchall()
    conn.close()
    return exams

def delete_exam(exam_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM exams WHERE id = ?', (exam_id,))
    conn.commit()
    conn.close()

def add_task(title, subject, due_date, priority):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (title, subject, due_date, priority, status, created_at)
        VALUES (?, ?, ?, ?, 'pending', ?)
    ''', (title, subject, due_date, priority, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_tasks(status=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks WHERE status = ? ORDER BY due_date ASC', (status,))
    else:
        c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks ORDER BY due_date ASC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_today_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('SELECT id, title, subject, due_date, priority, status FROM tasks WHERE created_at = ? ORDER BY priority ASC', (today,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('done', task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def save_mood(mood):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('DELETE FROM mood_checkin WHERE checkin_date = ?', (today,))
    if mood:
        c.execute('INSERT INTO mood_checkin (mood, checkin_date) VALUES (?, ?)', (mood, today))
    conn.commit()
    conn.close()

def get_today_mood():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute('SELECT mood FROM mood_checkin WHERE checkin_date = ?', (today,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_mood_last_7_days():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT mood, checkin_date FROM mood_checkin ORDER BY checkin_date DESC LIMIT 7')
    result = c.fetchall()
    conn.close()
    return result
def save_student_name(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS student_profile (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    c.execute('DELETE FROM student_profile')
    c.execute('INSERT INTO student_profile (id, name) VALUES (1, ?)', (name,))
    conn.commit()
    conn.close()

def get_student_name():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT name FROM student_profile WHERE id = 1')
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except:
        conn.close()
        return None
def add_recurring_task(title, subject, days):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recurring_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subject TEXT,
            days TEXT
        )
    ''')
    c.execute('INSERT INTO recurring_tasks (title, subject, days) VALUES (?, ?, ?)',
              (title, subject, ','.join(days)))
    conn.commit()
    conn.close()

def get_recurring_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT id, title, subject, days FROM recurring_tasks')
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

def save_day_checkin(rating, mood, study_hours, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS day_checkin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            mood TEXT,
            study_hours REAL,
            checkin_date TEXT
        )
    ''')
    c.execute('DELETE FROM day_checkin WHERE checkin_date = ?', (date,))
    c.execute('INSERT INTO day_checkin (rating, mood, study_hours, checkin_date) VALUES (?, ?, ?, ?)',
              (rating, mood, study_hours, date))
    conn.commit()
    conn.close()

def get_day_checkin(date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT rating, mood, study_hours FROM day_checkin WHERE checkin_date = ?', (date,))
        result = c.fetchone()
        conn.close()
        return result
    except:
        conn.close()
        return None
def get_checkin_last_7_days():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT rating, mood, study_hours, checkin_date FROM day_checkin ORDER BY checkin_date DESC LIMIT 7')
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []
def get_xp():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS xp (
            id INTEGER PRIMARY KEY,
            total_xp INTEGER DEFAULT 0,
            last_updated TEXT
        )''')
        c.execute('SELECT total_xp FROM xp WHERE id = 1')
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0
    except:
        conn.close()
        return 0

def add_xp(amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS xp (
        id INTEGER PRIMARY KEY,
        total_xp INTEGER DEFAULT 0,
        last_updated TEXT
    )''')
    c.execute('SELECT total_xp FROM xp WHERE id = 1')
    result = c.fetchone()
    if result:
        new_xp = result[0] + amount
        c.execute('UPDATE xp SET total_xp = ?, last_updated = ? WHERE id = 1',
                  (new_xp, datetime.now().strftime("%Y-%m-%d")))
    else:
        c.execute('INSERT INTO xp (id, total_xp, last_updated) VALUES (1, ?, ?)',
                  (amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_streak():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT checkin_date FROM day_checkin ORDER BY checkin_date DESC')
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

def get_badges():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            earned_at TEXT
        )''')
        c.execute('SELECT name, earned_at FROM badges')
        result = c.fetchall()
        conn.close()
        return result
    except:
        conn.close()
        return []

def award_badge(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        earned_at TEXT
    )''')
    try:
        c.execute('INSERT INTO badges (name, earned_at) VALUES (?, ?)',
                  (name, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
    except:
        pass
    conn.close()