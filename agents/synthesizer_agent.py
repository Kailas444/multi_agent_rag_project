def synthesis_agent(state: WorkflowState) -> WorkflowState:
    op = state.get("operation", "")

    if op == "rag":
        q = state["user_query"]
        context = state.get("retrieved_context", "")

        state["react_steps"].append({"act": "LLM.generate_grounded_answer"})
        ans = generate_answer_from_context(llm, context, q)
        state["final_answer"] = ans

        # keep citations from retrieved docs (already in state)

    elif op == "tool":
        tname = state.get("tool_name", "")
        result = state.get("tool_result", {})

        # Tool output formatting
        if tname == "weather" and result.get("ok"):
            lines = [f"Weather Forecast for {result.get('location')}:"]
            for d in result.get("forecast", []):
                lines.append(
                    f"- {d['date']}: min {d['temp_min_c']}°C, max {d['temp_max_c']}°C, "
                    f"rain {d['precip_mm']}mm, wind {d['wind_max_kmh']}km/h"
                )
            state["final_answer"] = "\n".join(lines)

        elif tname == "calculator" and result.get("ok"):
            state["final_answer"] = f"Result: {result.get('result')}"

        else:
            state["final_answer"] = f"Tool '{tname}' failed: {json.dumps(result, indent=2)}"

        # Tools don't produce PDF citations; keep citations empty
        state["citations"] = []

    else:
        state["final_answer"] = "Unsupported operation."
        state["citations"] = []

    return state
