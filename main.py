from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="E-commerce Agentic RAG API")


class ChatRequest(BaseModel):
    query: str


@app.post("/agent/chat")
def agent_chat(req: ChatRequest):
    result = run_agent(req.query)
    return {
        "query": req.query,
        "intent": result["intent"],
        "answer": result["answer"]
    }