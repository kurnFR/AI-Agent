import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST: str = os.getenv(
    "OLLAMA_HOST",
    "http://host.docker.internal:11434"
)

MODEL_NAME: str = os.getenv(
    "MODEL_NAME",
    "qwen2.5:7b"
)

POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "host.docker.internal")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5431"))
POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "postgres")
POSTGRES_USER: str = quote_plus(os.getenv("POSTGRES_USER", "postgres"))
POSTGRES_PASSWORD: str = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
)

WORKSPACE_ROOT: str = os.getenv("WORKSPACE_ROOT", "/app")
EXECUTION_TIMEOUT: int = int(os.getenv("EXECUTION_TIMEOUT", "30"))