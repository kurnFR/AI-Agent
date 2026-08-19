import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.config import DATABASE_URL, MODEL_NAME, OLLAMA_HOST

app = FastAPI(
    title="Aegis AI Agent API",
    description="Multi-department autonomous AI agent platform with DAG workflow engine",
    version="0.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "Aegis AI Agent",
        "ollama_host": OLLAMA_HOST,
        "model_name": MODEL_NAME
    }


app.include_router(api_router)