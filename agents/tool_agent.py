from tools.weather_tool import weather_tool
from tools.calculator_tool import calculator_tool



ALLOWED_TOOLS = {"weather", "calculator"}

def tool_agent(state):
    name = state["tool_name"]

    if name not in ALLOWED_TOOLS:
        state["final_answer"] = "Tool not allowed"
        return state

    if name == "weather":
        result = weather_tool(state["tool_input"])
    else:
        result = calculator_tool(state["tool_input"])

    state["tool_result"] = result
    state["final_answer"] = str(result)
    return state
