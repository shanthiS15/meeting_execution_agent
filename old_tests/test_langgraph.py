from langgraph_agent import app_graph

result = app_graph.invoke({

    "meeting_text":
    """
    Shanthi will complete UI Design by Friday.
    Arun will finish Database Integration by Saturday.
    Karthik will prepare Project Presentation by Monday.
    """
})

print(result)