import os
import requests
from dotenv import load_dotenv

load_dotenv()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

print("BREVO KEY =", BREVO_API_KEY)
print("KEY LENGTH =", len(BREVO_API_KEY) if BREVO_API_KEY else None)


def send_email(receiver_email, subject, body):

    print("========== SENDING EMAIL ==========")
    print("To:", receiver_email)

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Meeting Execution Agent",
            "email": "23d151@psgitech.ac.in"
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": subject,
        "textContent": body
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print(response.text)

    response.raise_for_status()

    print("✅ Email Sent Successfully")