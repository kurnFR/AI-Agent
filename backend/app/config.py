import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:7b")
