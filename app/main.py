from fastapi import FastAPI
from orchestration.graph import app_graph

app = FastAPI(title="Multi-Agent RAG System")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "healthy"}

@app.post("/ask")
def ask(query: str):
    state = {
        "user_query": query,
        "operation": "",
        "plan": "",
        "react_steps": [],
        "retrieved_context": "",
        "citations": [],
        "tool_name": "",
        "tool_input": {},
        "tool_result": {},
        "final_answer": "",
        "error": "",
    }
    result = app_graph.invoke(state)
    return {
        "answer": result["final_answer"],
        "citations": result["citations"],
        "react_steps": result["react_steps"],
    }
