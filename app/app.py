from fastapi import FastAPI
from orchestration.graph import app_graph

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/ask")
def ask(query: str):
    return app_graph.invoke({"user_query": query})
