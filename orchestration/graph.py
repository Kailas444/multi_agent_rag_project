from langgraph.graph import StateGraph, END
from agents.planner_agent import planning_agent
from agents.tool_agent import tool_execution_agent
from agents.synthesis_agent import synthesis_agent

graph = StateGraph(dict)
graph.add_node("planner", planning_agent)
graph.add_node("tool", tool_execution_agent)
graph.add_node("synth", synthesis_agent)

graph.set_entry_point("planner")
graph.add_edge("planner", "tool")
graph.add_edge("tool", "synth")
graph.add_edge("synth", END)

app_graph = graph.compile()
