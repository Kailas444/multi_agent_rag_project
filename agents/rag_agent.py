from rag.vector_store import vector_store
from rag.vector_store import load_vector_store

vector_store = load_vector_store()

def rag_agent(state):
    query = state["user_query"]

    docs = vector_store.similarity_search(query, k=3)

    if not docs:
        state["final_answer"] = "I don't know from the provided documents."
        return state

    context = "\n".join(d.page_content for d in docs)
    state["citations"] = [d.metadata for d in docs]
    state["final_answer"] = context
    return state
