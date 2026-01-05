import re

def planner_agent(state):
    q = state["user_query"].lower()
    state["react_steps"] = []

    if "weather" in q:
        state["operation"] = "tool"
        state["tool_name"] = "weather"
        state["tool_input"] = {"location": "Chennai", "days": 3}
        state["plan"] = "Use weather tool"
    elif re.search(r"\d+[\+\-\*\/]\d+", q):
        state["operation"] = "tool"
        state["tool_name"] = "calculator"
        state["tool_input"] = {"expression": q}
        state["plan"] = "Use calculator"
    else:
        state["operation"] = "rag"
        state["plan"] = "Use RAG"

    state["react_steps"].append({"reason": state["plan"]})
    return state
