from database import get_all_tasks
from agent import generate_followup

tasks = get_all_tasks()

for task in tasks:

    if task[4] in ["Pending", "Unknown"]:

        print(generate_followup(task))

        print("=" * 50)