import sqlite3

conn = sqlite3.connect("data/meeting_agent.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE tasks
SET deadline = REPLACE(deadline, '.', '')
""")

conn.commit()
conn.close()

print("Deadlines Updated")