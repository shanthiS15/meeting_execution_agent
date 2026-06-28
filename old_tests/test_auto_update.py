from agent import extract_progress_updates
from database import update_task_by_name

meeting_text = """
Shanthi completed UI Design.

Arun is working on Database Integration.
"""

updates = extract_progress_updates(meeting_text)

for update in updates:

    update_task_by_name(
        update["task_name"],
        update["status"]
    )

print("Database Updated Successfully")