from agent import extract_tasks
from database import insert_task, get_all_tasks

meeting_text = """
Manager: Shanthi will complete UI Design by Friday.

Arun will finish Database Integration by Friday.
"""

tasks = extract_tasks(meeting_text)

for task in tasks:
    insert_task(task)

all_tasks = get_all_tasks()

for task in all_tasks:
    print(task)

print("\nPossible Statuses:")
print("Pending")
print("In Progress")
print("Completed")
print("Unknown")