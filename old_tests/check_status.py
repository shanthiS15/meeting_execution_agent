from database import get_all_tasks

tasks = get_all_tasks()

for task in tasks:
    print(task)