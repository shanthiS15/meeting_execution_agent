from langgraph_agent import app_graph

from workflow_agent import (
    generate_workflow_llm,
    get_execution_plan_llm
)

from followup_agent import generate_followup_llm

from database import (
    clear_tasks,
    clear_execution_results,
    clear_processed_replies,
    insert_task,
    get_all_tasks,
    get_email_by_name,
    save_execution_result,
)


from send_email import send_email


def run_execution_cycle(meeting_text):

    print("========== EXECUTION AGENT STARTED ==========")

    '''meeting_title = "Meeting " + datetime.now().strftime("%d-%m-%Y %H:%M")

    meeting_id = create_meeting(
        meeting_title,
        meeting_text
    )

    print("Meeting Created:", meeting_title)
    print("Meeting ID:", meeting_id)'''


    # Step 1 - Clear old tasks
    # clear_tasks()
    clear_execution_results()
    # clear_processed_replies()

    # Step 2 - Extract Tasks
    print("Extracting Tasks...")

    result = app_graph.invoke({
        "meeting_text": meeting_text
    })                                          ### lanGraph is invoked and used here 

    tasks = result["extracted_tasks"]

    # Step 3 - Store Tasks
    print("Saving Tasks...")

    for task in tasks:

        '''print(task)
        print(type(task))'''

        insert_task(task)

        '''save_task_history(
            meeting_id,
            task["task_name"],
            task["owner"],
            task["deadline"],
            task["status"],
            "Created"
        )'''

    # Step 4 - Process Each Task
    print("Generating Execution Results...")

    for task in get_all_tasks():

        task_name = task[1]
        owner = task[2]
        deadline = task[3]
        status = task[4]

        workflow = [
            "Requirement Analysis",
            "Planning",
            "Implementation",
            "Testing",
            "Deployment"
        ]

        priority = "Medium"
        start_day = "Today"
        today_activity = "Planning"

        followup_message = f"""
            Please provide an update on the task '{task_name}'.

            Current Status: {status}
            Deadline: {deadline}

            Reply with:
            • Completed
            • In Progress
            • Pending
        """

        email_sent = "No"

        if status != "Completed":

            email = get_email_by_name(owner)

            if email:

                subject = f"Task Follow-Up | {owner} | {task_name}"

                print(f"Follow-up generated for {owner}")

                send_email(
                     email,
                     subject,
                     followup_message
                 )

                email_sent = "Yes"

            else:

                print("No email found for", owner)

        save_execution_result(

            task_name=task_name,
            workflow=workflow,
            priority=priority,
            start_day=start_day,
            today_activity=today_activity,
            followup_message=followup_message,
            email_sent=email_sent

        )

    print("========== EXECUTION AGENT FINISHED ==========")