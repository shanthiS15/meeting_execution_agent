from agent import extract_progress_updates

meeting_text = """
Shanthi completed UI Design.

Arun is working on Database Integration.
"""

updates = extract_progress_updates(meeting_text)

print(updates)