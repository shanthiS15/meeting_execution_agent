from llm_agent import extract_progress_updates_llm

text = """
UI Design is not yet completed.
Database Integration is currently being worked on.
Project Presentation has been completed successfully.
"""

print(
    extract_progress_updates_llm(text)
)