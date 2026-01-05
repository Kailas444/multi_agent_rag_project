def tool_execution_agent(state: WorkflowState) -> WorkflowState:
    tname = state.get("tool_name", "")
    tinp = state.get("tool_input", {})

    state["react_steps"].append({"act": "Tool.call", "tool": tname, "input": tinp})
    # dispatch to appropriate tool based on name
    if tname == "weather":
        result = weather_tool_call(tinp)
    elif tname == "calculator":
        result = calculator_tool_call(tinp)
    else:
        result = {"ok": False, "error": f"Unknown tool: {tname}"}
    state["tool_result"] = result
    state["react_steps"].append({"observe": result})

    return state
