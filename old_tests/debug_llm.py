from llm_agent import client

meeting_text = """
Shanthi will complete UI Design by Friday.
Arun will finish Database Integration by Saturday.
Karthik will prepare Project Presentation by Monday.
"""

prompt = f"""
Extract all assigned tasks from the meeting.

Return ONLY a valid Python list of dictionaries.

Example:

[
  {{
    "task_name": "UI Design",
    "owner": "Shanthi",
    "deadline": "Friday"
  }}
]

Meeting:
{meeting_text}
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)