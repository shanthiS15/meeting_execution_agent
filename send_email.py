import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(receiver_email, subject, body):

    print("========== SENDING EMAIL ==========")
    print("To:", receiver_email)

    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [receiver_email],
            "subject": subject,
            "text": body,
        })

        print("✅ Email sent")
        print(response)

    except Exception as e:
        print("❌ RESEND ERROR:")
        print(e)
        raise