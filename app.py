from auto_reply_checker import start_auto_reply_checker
from flask import Flask, render_template, request, redirect
from execution_agent import run_execution_cycle
from process_email_replies import process_email_replies
from transcript_reader import read_transcript
from zoom_agent import get_latest_zoom_transcript
from llm_agent import (
    extract_progress_updates_llm
)

from database import (
    create_database,
    get_all_tasks,
    get_execution_results,
    update_status,
    update_task_by_name,
    add_team_member,
    get_team_members
)

create_database()

app = Flask(__name__)


@app.route("/")
def home():

    tasks = get_all_tasks()

    total_tasks = len(tasks)

    completed = sum(
        1 for task in tasks
        if task[4] == "Completed"
    )

    pending = sum(
        1 for task in tasks
        if task[4] == "Pending"
    )

    results = get_execution_results()

    emails_sent = sum(
        1 for r in results
        if r["email_sent"] in ("Yes", "Generated")
    )

    return render_template(

        "index.html",

        total_tasks=total_tasks,

        completed=completed,

        pending=pending,

        emails_sent=emails_sent

    )


@app.route("/dashboard")
def dashboard():

    tasks = get_all_tasks()

    results = get_execution_results()

    owner_map = {}

    status_map = {}

    for task in tasks:

        owner_map[task[1]] = task[2]
        status_map[task[1]] = task[4]

    # ---------- Today's Plan ----------

    today_plans = []

    for result in results:

        today_plans.append({

            "owner": owner_map.get(result["task_name"], "Unknown"),

            "task_name": result["task_name"],

            "today_activity": result["today_activity"]

        })

    # ---------- Followups ----------

    followups = []

    for result in results:

        if status_map.get(result["task_name"]) == "Completed":
            continue

        followups.append({

            "owner": owner_map.get(result["task_name"], "Unknown"),

            "task_name": result["task_name"],

            "status": status_map.get(result["task_name"], "Pending"),

            "message": result["followup_message"],

            "email_sent": result["email_sent"]

        })

    completed = 0

    pending = 0

    for task in tasks:

        if task[4] == "Completed":
            completed += 1
        else:
            pending += 1

    return render_template(

        "dashboard.html",

        tasks=tasks,

        workflows=results,

        plans=today_plans,

        followups=followups,

        completed=completed,

        pending=pending,

        emails_sent=sum(
            1
            for item in results
            if item["email_sent"] in ("Yes", "Generated")
        )

    )

@app.route("/process", methods=["POST"])
def process_meeting():

    meeting_text = request.form.get(
        "meeting_text",
        ""
    )

    uploaded_file = request.files.get(
        "transcript_file"
    )

    if uploaded_file and uploaded_file.filename:

        try:

            meeting_text = read_transcript(
                uploaded_file
            )

        except Exception as e:

            return f"File Error: {str(e)}"

    if not meeting_text.strip():

        return (
            "Please upload a transcript "
            "or paste meeting text."
        )

    run_execution_cycle(meeting_text)

    return redirect("/dashboard")

@app.route("/update_status", methods=["POST"])
def update_task_status():

    task_id = request.form["task_id"]

    status = request.form["status"]

    update_status(task_id, status)

    return redirect("/dashboard")



@app.route("/workflow")
def workflow():

    workflows = get_execution_results()

    print("===== WORKFLOW DATA =====")
    for w in workflows:
        print(w["task_name"])

    return render_template(
        "workflow.html",
        workflows=workflows
    )

@app.route("/today")
def today():

    results = get_execution_results()

    plans = []

    tasks = get_all_tasks()

    owner_map = {}

    for task in tasks:

        owner_map[task[1]] = task[2]

    for result in results:

        plans.append({

            "owner": owner_map.get(
                result["task_name"],
                "Unknown"
            ),

            "task_name": result["task_name"],

            "today_activity": result["today_activity"]

        })

    return render_template(

        "today.html",

        plans=plans

    )

@app.route("/followups")
def followups():

    results = get_execution_results()

    tasks = get_all_tasks()

    status_map = {}

    owner_map = {}

    for task in tasks:

        owner_map[task[1]] = task[2]

        status_map[task[1]] = task[4]

    followup_list = []

    for result in results:

        if status_map.get(result["task_name"]) == "Completed":

            continue

        followup_list.append({

            "owner": owner_map.get(
                result["task_name"],
                "Unknown"
            ),

            "task_name": result["task_name"],

            "status": status_map.get(
                result["task_name"],
                "Pending"
            ),

            "message": result["followup_message"]

        })

    return render_template(

        "followups.html",

        followups=followup_list

    )

@app.route("/team")
def team():

    members = get_team_members()

    return render_template(
        "team.html",
        members=members
    )


@app.route("/add_member", methods=["POST"])
def add_member():

    name = request.form["name"].strip()

    email = request.form["email"].strip()

    add_team_member(
        name,
        email
    )

    return redirect("/team")


@app.route("/process_zoom")
def process_zoom():

    meeting_text = get_latest_zoom_transcript()

    run_execution_cycle(meeting_text)

    return redirect("/dashboard")

@app.route("/check_email_replies")
def check_email_replies():

    process_email_replies()

    return redirect("/dashboard")

if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )
