from email_reply_agent import get_latest_replies
from reply_classifier import classify_reply
from database import get_all_tasks
from workflow_agent import (
    generate_workflow_llm,
    get_execution_plan_llm
)

from followup_agent import (
    generate_followup_llm
)

from send_email import send_email

from database import (
    update_task_by_name,
    is_reply_processed,
    mark_reply_processed,
    save_execution_result,
    get_all_tasks,
    get_email_by_name,
    clear_execution_results
)


def process_email_replies():

    print("========== PROCESS EMAIL REPLIES STARTED ==========")
    print("Current Tasks in DB:", get_all_tasks())

    replies = get_latest_replies()

    print("Replies Found:", len(replies))

    # -------------------------------------------------
    # STEP 1 : Update task status from email replies
    # -------------------------------------------------

    for reply in replies:

        sender = reply["sender"]
        subject = reply["subject"]
        body = reply["body"]

        if is_reply_processed(subject, sender):

            print("Already Processed:", subject)
            continue

        try:

            # Subject format:
            # Re: Task Follow-Up | Shanthi | User Interface Design

            parts = subject.split("|")

            owner = parts[1].strip()
            task_name = parts[2].strip()

        except Exception:

            print("Invalid Subject:", subject)
            continue

        status = classify_reply(body)

        print("----------------------------------")
        print("Owner :", owner)
        print("Task  :", task_name)
        print("Reply :", body)
        print("Status:", status)

        update_task_by_name(
            task_name,
            status
        )

        mark_reply_processed(
            subject,
            sender
        )

        print("Reply Marked as Processed")

    # -------------------------------------------------
    # STEP 2 : Refresh Execution Results
    # -------------------------------------------------

    print("\nRefreshing Execution Results...")

    clear_execution_results()

    print("Current Tasks:", get_all_tasks())

    tasks = get_all_tasks()

    for task in tasks:

        task_name = task[1]
        owner = task[2]
        deadline = task[3]
        status = task[4]

        workflow = generate_workflow_llm(
            task_name,
            deadline
        )

        plan = get_execution_plan_llm(
            task_name,
            deadline
        )

        followup = generate_followup_llm(
            task_name,
            owner,
            deadline,
            status
        )

        email_sent = "No"

        # Send follow-up only for incomplete tasks

        if status != "Completed":

            email = get_email_by_name(owner)

            if email:

                subject = f"Task Follow-Up | {owner} | {task_name}"

                send_email(
                    email,
                    subject,
                    followup
                )

                print("Follow-up Sent:", owner)

                email_sent = "Yes"

        save_execution_result(

            task_name=task_name,

            workflow=workflow,

            priority=plan["priority"],

            start_day=plan["start_day"],

            today_activity=plan["today_activity"],

            followup_message=followup,

            email_sent=email_sent

        )

    print("========== PROCESS EMAIL REPLIES FINISHED ==========")


if __name__ == "__main__":

    process_email_replies()