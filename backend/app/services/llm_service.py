from typing import Optional
from ollama import Client

from app.config import MODEL_NAME, OLLAMA_HOST


class LLMService:

    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):

        self.host = host or OLLAMA_HOST
        self.model = model or MODEL_NAME
        self.client = Client(host=self.host)

    def ask(self, prompt: str) -> str:

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=False
            )
            return response.message.content
        except Exception as ex:
            raise RuntimeError(f"Ollama request failed on {self.host} (model={self.model}): {ex}") from ex

