import sqlite3

conn = sqlite3.connect("data/meeting_agent.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM team_members")

conn.commit()

conn.close()

print("All team members deleted")