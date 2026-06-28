import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "23d151@psgitech.ac.in"

APP_PASSWORD = "vuml eypf bghz xewz"


def send_email(receiver_email, subject, body):

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)

    print("Email Sent Successfully")