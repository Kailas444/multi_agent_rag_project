import re

def planning_agent(state):
    q = state["user_query"].lower()
    state["react_steps"] = []
    state["tool_name"] = ""
    state["tool_input"] = {}

    if "weather" in q or "forecast" in q:
        state["operation"] = "tool"
        state["tool_name"] = "weather"
        state["tool_input"] = {"location": "Chennai", "days": 3}
        state["plan"] = "Call weather tool"
    elif "calculate" in q or re.search(r"\d+\s*[\+\-\*\/]\s*\d+", q):
        state["operation"] = "tool"
        state["tool_name"] = "calculator"
        state["tool_input"] = {"expression": q.replace("calculate", "")}
        state["plan"] = "Call calculator tool"
    else:
        state["operation"] = "rag"
        state["plan"] = "Retrieve from documents using RAG"

    state["react_steps"].append({"reason": state["plan"]})
    return state
