from langgraph.graph import StateGraph, END
from agents.planner_agent import planning_agent

def route(state):
    return "tool" if state["operation"] == "tool" else "rag"

graph = StateGraph(dict)
graph.add_node("planner", planning_agent)
graph.set_entry_point("planner")
graph.add_edge("planner", END)

app_graph = graph.compile()
