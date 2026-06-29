import sqlite3

conn = sqlite3.connect(DATABASE_PATH)

cursor = conn.cursor()

cursor.execute("SELECT * FROM tasks")

print(cursor.fetchall())

conn.close()