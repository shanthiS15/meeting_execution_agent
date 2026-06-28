import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(receiver_email, subject, body):

    print("========== SENDING EMAIL ==========")
    print("To:", receiver_email)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        raise