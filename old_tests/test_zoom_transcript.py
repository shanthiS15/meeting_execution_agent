from zoom_agent import get_latest_zoom_transcript
from langgraph_agent import app_graph

transcript = get_latest_zoom_transcript()

result = app_graph.invoke({
    "meeting_text": transcript
})

print(result)