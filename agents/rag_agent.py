from rag.vector_store import vector_store
from rag.local_llm import llm

def rag_agent(state):
    q = state["user_query"]
    docs = vector_store.similarity_search(q, k=3)

    if not docs:
        state["final_answer"] = "I don't know from the provided documents."
        return state

    context = "\n".join(d.page_content for d in docs)
    state["citations"] = [d.metadata for d in docs]

    prompt = f"Answer using context only:\n{context}\nQuestion:{q}"
    state["final_answer"] = llm.invoke(prompt)
    return state
