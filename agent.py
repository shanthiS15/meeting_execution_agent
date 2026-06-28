def extract_tasks(meeting_text):

    tasks = []

    lines = meeting_text.split("\n")

    for line in lines:

        line = line.strip()

        if "will complete" in line:

            parts = line.split("will complete")

            owner = (
                parts[0]
                .replace("Manager:", "")
                .replace("Project Manager:", "")
                .strip()
            )

            remaining = parts[1].strip()

            if "by" in remaining:

                task, deadline = remaining.split("by")

                tasks.append({
                    "task_name": task.strip(),
                    "owner": owner,
                    "deadline": deadline.strip().replace(".", ""),
                    "status": "Pending"
                })

        elif "will finish" in line:

            parts = line.split("will finish")

            owner = (
                parts[0]
                .replace("Manager:", "")
                .replace("Project Manager:", "")
                .strip()
            )

            remaining = parts[1].strip()

            if "by" in remaining:

                task, deadline = remaining.split("by")

                tasks.append({
                    "task_name": task.strip(),
                    "owner": owner,
                    "deadline": deadline.strip().replace(".", ""),
                    "status": "Pending"
                })

    return tasks

def extract_progress_updates(meeting_text):

    updates = []

    lines = meeting_text.split("\n")

    for line in lines:

        line = line.strip()

        if "completed" in line:

            parts = line.split("completed")

            task_name = parts[1].strip().replace(".", "")

            updates.append({
                "task_name": task_name,
                "status": "Completed"
            })

        elif "is working on" in line:

            parts = line.split("is working on")

            task_name = parts[1].strip().replace(".", "")

            updates.append({
                "task_name": task_name,
                "status": "In Progress"
            })

    return updates

def generate_followup(task):

    task_name = task[1]
    owner = task[2]
    deadline = task[3]
    status = task[4]

    message = f"""
Dear {owner},

The task "{task_name}" assigned during the meeting is currently {status}.

Deadline: {deadline}

Please provide a status update.

Thank you.
"""

    return message

def generate_workflow(task_name, deadline):

    task_name = task_name.lower()

    if "ui" in task_name:

        return [
            "Requirement Gathering",
            "Create Wireframes",
            "Design Screens",
            "Review Design",
            "Final Submission"
        ]

    elif "database" in task_name:

        return [
            "Database Design",
            "Schema Creation",
            "API Integration",
            "Testing",
            "Deployment"
        ]

    elif "presentation" in task_name:

        return [
            "Prepare Slides",
            "Content Review",
            "Presentation Practice",
            "Final Corrections",
            "Presentation Delivery"
        ]

    else:

        return [
            "Requirement Understanding",
            "Planning",
            "Implementation",
            "Review",
            "Final Submission"
        ]

def get_execution_plan(task_name, deadline):

    if deadline == "Monday":

        priority = "High"
        start_day = "Friday"

    elif deadline == "Friday":

        priority = "High"
        start_day = "Wednesday"

    elif deadline == "Saturday":

        priority = "Medium"
        start_day = "Thursday"

    else:

        priority = "Medium"
        start_day = "Today"

    workflow = generate_workflow(
        task_name,
        deadline
    )

    today_activity = workflow[1]

    return {
        "priority": priority,
        "start_day": start_day,
        "today_activity": today_activity
    }