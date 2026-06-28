from groq import Groq
import json

import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_tasks_llm(meeting_text):

    prompt = f"""
You are an intelligent Meeting-to-Execution Agent.

Your job is to extract ONLY the actionable tasks from the meeting transcript.

IMPORTANT RULES

1. Extract the COMPLETE task name.
Never shorten the task name.

Correct:
- User Profile Page
- Product Search Feature
- Inventory Management Module
- Payment Gateway Integration
- Fraud Detection and Payment Failure Handling

Wrong:
- UI
- Search
- Inventory
- Payment

--------------------------------------------------

2. Extract ONLY tasks that require action.

Examples:

Rahul will complete Product Search Feature by Thursday.
→ Extract

Rahul has completed Product Search Feature.
→ Do NOT extract (already completed)

--------------------------------------------------

3. If a completed task is followed by a NEW task,
extract ONLY the NEW task.

Example:

Rahul has completed Product Search Feature.
Rahul will complete Product Filtering by Thursday.

Extract

Product Filtering

--------------------------------------------------

4. If someone is still working on an existing task and NO new task is assigned,
extract that task.

Example

Shanthi is still working on the User Profile Page.

Extract

User Profile Page

--------------------------------------------------

5. If one employee receives multiple tasks,
extract every task separately.

--------------------------------------------------

6. If no deadline is mentioned,
return "Not Specified".

--------------------------------------------------

Return ONLY valid JSON.

Example

[
    {{
        "task_name":"Product Search Feature",
        "owner":"Rahul",
        "deadline":"Thursday"
    }},
    {{
        "task_name":"User Profile Page",
        "owner":"Shanthi",
        "deadline":"Friday"
    }}
]

Meeting Transcript:

{meeting_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    start = result.find("[")
    end = result.rfind("]") + 1

    if start == -1 or end == 0:
        return []

    json_text = result[start:end]

    try:

        data = json.loads(json_text)

        tasks = []

        for task in data:

            tasks.append({

                "task_name": task.get(
                    "task_name",
                    ""
                ).strip(),

                "owner": task.get(
                    "owner",
                    ""
                ).strip(),

                "deadline": task.get(
                    "deadline",
                    "Not Specified"
                ).strip(),

                "status": "Pending"

            })

        return tasks

    except Exception as e:

        print("Task JSON Error:", e)

        return []


def extract_progress_updates_llm(meeting_text):

    prompt = f"""
You are an AI Project Progress Analyzer.

Read the meeting transcript carefully.

Extract ONLY project progress updates.

Allowed Status values:

Completed

In Progress

Pending

--------------------------------------------

Completed

Examples

completed

finished

done

submitted

delivered

--------------------------------------------

In Progress

Examples

working

still working

currently working

ongoing

almost done

--------------------------------------------

Pending

Examples

not started

yet to begin

waiting

blocked

--------------------------------------------

Return ONLY valid JSON.

Example

[
    {{
        "task_name":"User Profile Page",
        "status":"In Progress"
    }},
    {{
        "task_name":"Refund Management Module",
        "status":"Completed"
    }}
]

Meeting Transcript:

{meeting_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    start = result.find("[")
    end = result.rfind("]") + 1

    if start == -1 or end == 0:
        return []

    json_text = result[start:end]

    try:

        data = json.loads(json_text)

        updates = []

        for update in data:

            updates.append({

                "task_name": update.get(
                    "task_name",
                    ""
                ).strip(),

                "status": update.get(
                    "status",
                    "Pending"
                ).strip()

            })

        return updates

    except Exception as e:

        print("Progress JSON Error:", e)

        return []