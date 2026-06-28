from llm_agent import extract_tasks_llm

meeting = """
Shanthi will complete UI Design by Friday.
Arun will finish Database Integration by Saturday.
Karthik will prepare the Project Presentation by Monday.
"""

result = extract_tasks_llm(meeting)

print(result)