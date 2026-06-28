from typing import TypedDict
from langgraph.graph import StateGraph, END

from llm_agent import extract_tasks_llm
from workflow_agent import (
    generate_workflow_llm,
    get_execution_plan_llm
)
from followup_agent import generate_followup_llm


class AgentState(TypedDict):

    meeting_text: str

    extracted_tasks: list

    workflows: list

    plans: list

    followups: list


def task_extraction_node(state):

    print("Extracting Tasks...")

    tasks = extract_tasks_llm(
        state["meeting_text"]
    )

    state["extracted_tasks"] = tasks

    return state


def workflow_node(state):

    print("Generating Workflows...")

    workflows = []

    for task in state["extracted_tasks"]:

        workflow = generate_workflow_llm(
            task["task_name"],
            task["deadline"]
        )

        workflows.append(workflow)

    state["workflows"] = workflows

    return state


def execution_node(state):

    print("Generating Execution Plans...")

    plans = []

    for task in state["extracted_tasks"]:

        plan = get_execution_plan_llm(
            task["task_name"],
            task["deadline"]
        )

        plans.append(plan)

    state["plans"] = plans

    return state


def followup_node(state):

    print("Generating Followups...")

    followups = []

    for task in state["extracted_tasks"]:

        followup = generate_followup_llm(
            task["task_name"],
            task["owner"],
            task["deadline"],
            task["status"]
        )

        followups.append(followup)

    state["followups"] = followups

    return state


graph = StateGraph(AgentState)

graph.add_node(
    "task_extraction",
    task_extraction_node
)

graph.add_node(
    "workflow_generation",
    workflow_node
)

graph.add_node(
    "execution_planning",
    execution_node
)

graph.add_node(
    "followup_generation",
    followup_node
)

graph.set_entry_point(
    "task_extraction"
)

graph.add_edge(
    "task_extraction",
    "workflow_generation"
)

graph.add_edge(
    "workflow_generation",
    "execution_planning"
)

graph.add_edge(
    "execution_planning",
    "followup_generation"
)

graph.add_edge(
    "followup_generation",
    END
)

app_graph = graph.compile()