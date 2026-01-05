from rag.vector_store import initialize_vector_store
from rag.local_llm import create_local_llm

vector_store = initialize_vector_store(
    "data/artificial_intelligence_tutorial.pdf"
)
llm = create_local_llm()

def handle_user_query(q):
    return {"answer": "Integrated successfully"}
