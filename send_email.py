import smtplib
from email.message import EmailMessage
import os

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(receiver_email, subject, body):

    try:

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = receiver_email

        msg.set_content(body)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL,
                PASSWORD
            )

            smtp.send_message(msg)

        print("✅ Email Sent Successfully")

    except Exception as e:

        print("❌ Email Error:", e)