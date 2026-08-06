from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.services.llm_service import LLMService

app = FastAPI()

llm = LLMService()


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "0.1.0"
    }


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        answer = llm.ask(req.message)

        return {
            "reply": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
