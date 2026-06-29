import sqlite3
import json

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

# Create the data folder if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, "meeting_agent.db")

def create_database():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    # ---------------- Tasks ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        owner TEXT,
        deadline TEXT,
        status TEXT
    )
    """)

    # ---------------- Team Members ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        email TEXT
    )
    """)

    # ---------------- Processed Replies ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        sender TEXT,
        processed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- Execution Results ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS execution_results (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_name TEXT UNIQUE,

        workflow TEXT,

        priority TEXT,

        start_day TEXT,

        today_activity TEXT,

        followup_message TEXT,

        email_sent TEXT

    )
    """)

    # =====================================================
    # NEW TABLE : Meetings
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings(

        meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,

        meeting_title TEXT,

        meeting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        transcript TEXT

    )
    """)

    # =====================================================
    # NEW TABLE : Task History
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_history(

        history_id INTEGER PRIMARY KEY AUTOINCREMENT,

        meeting_id INTEGER,

        task_name TEXT,

        owner TEXT,

        deadline TEXT,

        status TEXT,

        action TEXT,

        updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()

def insert_task(task):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tasks
    WHERE task_name = ?
    AND owner = ?
    """, (
        task["task_name"],
        task["owner"]
    ))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return

    cursor.execute("""
    INSERT INTO tasks
    (task_name, owner, deadline, status)
    VALUES (?, ?, ?, ?)
    """, (
        task["task_name"],
        task["owner"],
        task["deadline"],
        task["status"]
    ))

    conn.commit()
    conn.close()


def get_all_tasks():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return rows

def add_team_member(name, email):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO team_members
    (name, email)
    VALUES (?, ?)
    """, (name, email))

    conn.commit()
    conn.close()


def get_team_members():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM team_members")

    rows = cursor.fetchall()

    conn.close()

    return rows

def update_status(task_id, new_status):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET status = ?
    WHERE id = ?
    """, (new_status, task_id))

    conn.commit()
    conn.close()

def update_task_by_name(task_name, new_status):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    print("Updating Task:", repr(task_name))
    print("New Status:", new_status)

    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE TRIM(task_name) = TRIM(?)
    """, (
        new_status,
        task_name
    ))

    conn.commit()

    print("Rows Updated:", cursor.rowcount)

    cursor.execute("SELECT * FROM tasks")

    print(cursor.fetchall())

    conn.close()

def get_email_by_name(name):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT email
    FROM team_members
    WHERE name = ?
    """, (name,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def clear_tasks():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name='tasks'"
    )

    conn.commit()
    conn.close()

def clear_team_members():

    import sqlite3

    conn = sqlite3.connect("data/meeting_agent.db")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM team_members")

    conn.commit()

    conn.close()

def create_processed_reply_table():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_replies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        subject TEXT,

        sender TEXT,

        processed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()

def is_reply_processed(subject, sender):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM processed_replies
        WHERE subject = ? AND sender = ?
    """, (subject, sender))

    result = cursor.fetchone()

    conn.close()

    return result is not None

def mark_reply_processed(subject, sender):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO processed_replies(subject, sender)
        VALUES(?, ?)
    """, (subject, sender))

    conn.commit()
    conn.close()

def save_execution_result(
    task_name,
    workflow,
    priority,
    start_day,
    today_activity,
    followup_message,
    email_sent
):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO execution_results
    (
        task_name,
        workflow,
        priority,
        start_day,
        today_activity,
        followup_message,
        email_sent
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        task_name,
        json.dumps(workflow),
        priority,
        start_day,
        today_activity,
        followup_message,
        email_sent

    ))

    conn.commit()
    conn.close()

def get_execution_results():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        task_name,
        workflow,
        priority,
        start_day,
        today_activity,
        followup_message,
        email_sent
    FROM execution_results
    """)

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        results.append({

            "task_name": row[0],

            "workflow": json.loads(row[1]),

            "priority": row[2],

            "start_day": row[3],

            "today_activity": row[4],

            "followup_message": row[5],

            "email_sent": row[6]

        })

    return results

def clear_execution_results():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM execution_results")

    cursor.execute("""
    DELETE FROM sqlite_sequence
    WHERE name='execution_results'
    """)

    conn.commit()

    conn.close()

def clear_processed_replies():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM processed_replies")

    conn.commit()

    conn.close()

def create_meeting(meeting_title, transcript):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO meetings

        (meeting_title, transcript)

        VALUES (?, ?)

    """, (

        meeting_title,
        transcript

    ))

    meeting_id = cursor.lastrowid

    conn.commit()

    conn.close()

    return meeting_id

if __name__ == "__main__":
    create_database()
    print("Database Created Successfully")
