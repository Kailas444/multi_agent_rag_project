def retrieval_agent(state: WorkflowState) -> WorkflowState:
    q = state["user_query"]

    state["react_steps"].append({"act": "RAG.retrieve", "input": q})
    context, citations = retrieve_rag_chunks(vector_store, q, k=3)

    state["retrieved_context"] = context
    state["citations"] = citations

    state["react_steps"].append({"observe": f"Retrieved {len(citations)} chunks"})
    return state
