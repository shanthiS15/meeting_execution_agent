from agent import extract_tasks

meeting_text = """
Manager: Shanthi will complete UI Design by Friday.

Arun will finish Database Integration by Friday.
"""

tasks = extract_tasks(meeting_text)

print(tasks)