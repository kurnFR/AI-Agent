from ollama import Client
from app.config import OLLAMA_HOST, MODEL_NAME

client = Client(host=OLLAMA_HOST)


class LLMService:

    def ask(self, prompt: str):

        print(f"Sending prompt: {prompt}")

        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=False
        )

        print("Received response from Ollama")

        print(response)

        return response.message.content
