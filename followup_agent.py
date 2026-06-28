from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_followup_llm(task_name, owner, deadline, status):

    prompt = f"""
You are a professional project manager.

Generate ONLY the follow-up message body.

STRICT RULES:

- Do NOT write a subject line.
- Do NOT write "Subject:".
- Do NOT write Dear, Hello, Hi.
- Do NOT write Best Regards.
- Do NOT write Thanks and Regards.
- Do NOT write signatures.
- Do NOT write [Your Name].
- Return only the follow-up message.

Task: {task_name}
Owner: {owner}
Deadline: {deadline}
Status: {status}

Keep it professional and under 80 words.
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

    message = response.choices[0].message.content.strip()

    bad_phrases = [
        "Subject:",
        "Best regards,",
        "Best Regards,",
        "Thanks and Regards,",
        "Regards,",
        "[Your Name]",
        "Dear",
        "Hello",
        "Hi"
    ]

    for phrase in bad_phrases:
        message = message.replace(phrase, "")

    message = message.strip()

    message += """

--------------------------------------------------

Please reply to this email with your latest progress.

You can reply naturally. Examples:

• Completed
• Finished yesterday.
• Still working on it.
• Almost done.
• Need one more day.
• Haven't started yet.

The Meeting-to-Execution Agent will automatically understand your reply and update your task status in the dashboard.

"""

    return message