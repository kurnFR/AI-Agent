from ollama import Client

from app.config import MODEL_NAME
from app.config import OLLAMA_HOST


class LLMService:

    def __init__(self):

        self.client = Client(host=OLLAMA_HOST)

    def ask(self, prompt: str) -> str:

        response = self.client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False
        )

        return response.message.content
