def planning_agent(state: WorkflowState) -> WorkflowState:
    q = state["user_query"].strip()
    ql = q.lower()

    # default
    state["react_steps"] = []
    state["error"] = ""
    state["retrieved_context"] = ""
    state["citations"] = []
    state["tool_result"] = {}
    state["tool_input"] = {}
    state["tool_name"] = ""

    # --- Routing rules ---
    if "weather" in ql or "temperature" in ql or "forecast" in ql:
        state["operation"] = "tool"
        state["tool_name"] = "weather"
        # Basic extraction: take words after "in"
        # Example: "weather in chennai"
        loc = q
        if " in " in ql:
            loc = q.split(" in ", 1)[1].strip()
        else:
            loc = "Chennai"  # fallback
        state["tool_input"] = {"location": loc, "days": 3}
        state["plan"] = "Call weather tool (no API key) using Open-Meteo."

    elif "calculate" in ql or re.search(r"\d+\s*[\+\-\*\/]\s*\d+", q):
        state["operation"] = "tool"
        state["tool_name"] = "calculator"
        expr = re.sub(r"(?i)\bcalculate\b", "", q).strip()
        state["tool_input"] = {"expression": expr if expr else q}
        state["plan"] = "Call calculator tool to compute the expression."

    else:
        state["operation"] = "rag"
        state["plan"] = "Use RAG to retrieve context from PDF and answer grounded with citations."

    state["react_steps"].append({"reason": state["plan"]})
    return state
