import imaplib
import email
import os

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def get_latest_replies():

    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    print("Connecting to Gmail...")

    mail.login(
        EMAIL,
        PASSWORD
    )

    print("Login Successful")

    mail.select("INBOX")

    print("Inbox Selected")

    status, messages = mail.search(
        None,
        "ALL"
    )

    print("Search Status:", status)

    email_ids = messages[0].split()

    # Read newest emails first
    email_ids = email_ids[::-1]

    # Process only latest 20 emails
    email_ids = email_ids[:20]

    print("Total Emails Found:", len(email_ids))

    replies = []

    for email_id in email_ids:

        status, data = mail.fetch(
            email_id,
            "(RFC822)"
        )

        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        sender = msg.get("From", "")
        subject = msg.get("Subject", "")

        # Process only follow-up replies
        if "Task Follow-Up" not in subject:
            continue

        if "Re:" not in subject:
            continue

        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()

                disposition = str(
                    part.get("Content-Disposition")
                )

                if (
                    content_type == "text/plain"
                    and "attachment" not in disposition
                ):

                    charset = (
                        part.get_content_charset()
                        or "utf-8"
                    )

                    body = part.get_payload(
                        decode=True
                    ).decode(
                        charset,
                        errors="ignore"
                    )

                    break

        else:

            charset = (
                msg.get_content_charset()
                or "utf-8"
            )

            body = msg.get_payload(
                decode=True
            ).decode(
                charset,
                errors="ignore"
            )

        # --------------------------------------------------
        # Keep only the user's reply
        # --------------------------------------------------

        separators = [
            "\r\nOn ",
            "\nOn ",
            "On Thu,",
            "On Fri,",
            "On Sat,",
            "On Sun,",
            "On Mon,",
            "On Tue,",
            "On Wed,"
        ]

        for separator in separators:

            if separator in body:

                body = body.split(separator)[0]

                break

        body = body.strip()

        print("\n----------------------------------")
        print("Sender :", sender)
        print("Subject:", subject)
        print("Body:\n")
        print(body)
        print("----------------------------------")

        replies.append({

            "sender": sender,

            "subject": subject,

            "body": body

        })

    mail.logout()

    return replies