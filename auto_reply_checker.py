import threading
import time

from process_email_replies import process_email_replies


def auto_check_replies():

    while True:

        try:

            print("\n===== AUTO CHECKING EMAIL REPLIES =====")

            process_email_replies()

        except Exception as e:

            print("Auto Reply Checker Error:", e)

        time.sleep(120)


def start_auto_reply_checker():

    thread = threading.Thread(
        target=auto_check_replies,
        daemon=True
    )

    thread.start()