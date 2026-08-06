from abc import ABC
from abc import abstractmethod

from app.services.llm_service import LLMService


class BaseAgent(ABC):

    name = ""

    def __init__(self):

        self.llm = LLMService()

    @abstractmethod
    def build_prompt(self, message: str) -> str:
        pass

    @abstractmethod
    def parse_response(self, response: str):
        pass

    def plan(self, message: str):

        prompt = self.build_prompt(message)

        response = self.llm.ask(prompt)

        return self.parse_response(response)
