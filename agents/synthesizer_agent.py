def synthesis_agent(state):
    state["final_answer"] = (
        state.get("tool_result")
        if state["operation"] == "tool"
        else state.get("retrieved_context")
    )
    return state
