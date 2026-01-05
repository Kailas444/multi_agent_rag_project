import re

def planning_agent(state):
    q = state["user_query"].lower()

    if "weather" in q:
        state["operation"] = "tool"
        state["tool_name"] = "weather"
        state["tool_input"] = {"location": "Chennai", "days": 3}
    elif re.search(r"\d+[\+\-\*\/]\d+", q):
        state["operation"] = "tool"
        state["tool_name"] = "calculator"
        state["tool_input"] = {"expression": q}
    else:
        state["operation"] = "rag"

    return state
