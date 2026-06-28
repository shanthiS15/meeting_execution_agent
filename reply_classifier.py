from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def classify_reply(reply):

    prompt = f"""
You are a task status classifier.

Read the user's reply and classify it into exactly ONE of these:

Completed
In Progress
Pending

Rules:
- Return ONLY one word or phrase.
- Do not explain.
- Do not add punctuation.

Reply:
{reply}
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

    return response.choices[0].message.content.strip()