
from groq import Groq
import json

import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_workflow_llm(task_name, deadline):

    prompt = f"""
You are an expert project execution planner.

Task: {task_name}
Deadline: {deadline}

Generate exactly 5 workflow steps.

Return ONLY a JSON array of strings.

Example:

[
    "Requirement Analysis",
    "System Design",
    "Implementation",
    "Testing",
    "Deployment"
]

Do not return explanations.
Do not return markdown.
Do not return dictionaries.
Return only JSON.
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

    result = response.choices[0].message.content.strip()

    try:

        start = result.find("[")
        end = result.rfind("]") + 1

        if start == -1 or end == 0:
            raise Exception("JSON array not found")

        workflow_json = result[start:end]

        workflow = json.loads(workflow_json)

        cleaned_workflow = []

        for step in workflow:

            if isinstance(step, dict):

                cleaned_workflow.append(
                    step.get("name", str(step))
                )

            else:

                cleaned_workflow.append(
                    str(step)
                )

        return cleaned_workflow

    except Exception as e:

        print("Workflow Error:", e)
        print("LLM Response:")
        print(result)

        return [
            "Requirement Analysis",
            "Planning",
            "Implementation",
            "Testing",
            "Deployment"
        ]


def get_execution_plan_llm(task_name, deadline):

    prompt = f"""
You are an expert project execution planner.

Task: {task_name}
Deadline: {deadline}

Determine:

1. Priority (High / Medium / Low)
2. Recommended Start Day
3. Today's Activity

Return ONLY JSON.

Example:

{{
    "priority": "High",
    "start_day": "Wednesday",
    "today_activity": "Requirement Analysis"
}}

Do not return explanations.
Do not return markdown.
Return only JSON.
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

    result = response.choices[0].message.content.strip()

    try:

        start = result.find("{")
        end = result.rfind("}") + 1

        if start == -1 or end == 0:
            raise Exception("JSON object not found")

        plan_json = result[start:end]

        plan = json.loads(plan_json)

        return {
            "priority": plan.get(
                "priority",
                "Medium"
            ),
            "start_day": plan.get(
                "start_day",
                "Today"
            ),
            "today_activity": plan.get(
                "today_activity",
                "Planning"
            )
        }

    except Exception as e:

        print("Execution Plan Error:", e)
        print("LLM Response:")
        print(result)

        return {
            "priority": "Medium",
            "start_day": "Today",
            "today_activity": "Planning"
        }