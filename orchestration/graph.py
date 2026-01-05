from langgraph.graph import StateGraph, END
from agents.planner import planner_agent
from agents.rag_agent import rag_agent
from agents.tool_agent import tool_agent
from agents.synth_agent import synth_agent

def router(state):
    return "tool" if state["operation"] == "tool" else "rag"

graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("rag", rag_agent)
graph.add_node("tool", tool_agent)
graph.add_node("synth", synth_agent)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    router,
    {"rag": "rag", "tool": "tool"}
)

graph.add_edge("rag", "synth")
graph.add_edge("tool", "synth")
graph.add_edge("synth", END)

app_graph = graph.compile()
