import os
import resend
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

print("EMAIL =", EMAIL)
print("PASSWORD LENGTH =", len(PASSWORD) if PASSWORD else None)
resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(receiver_email, subject, body):

    print("========== SENDING EMAIL ==========")
    print("To:", receiver_email)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email
    msg.set_content(body)

    try:
        print("Creating SMTP connection...")
        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        print("Logging in...")
        smtp.login(EMAIL, PASSWORD)

        print("Sending email...")
        smtp.send_message(msg)

        print("Closing connection...")
        smtp.quit()

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("❌ EMAIL ERROR:")
        print(type(e))
        print(e)
        raise