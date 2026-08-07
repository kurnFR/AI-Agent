import os

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://host.docker.internal:11434"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "qwen2.5:7b"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@host.docker.internal:5432/postgres"
)