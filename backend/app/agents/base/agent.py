from abc import ABC, abstractmethod

from app.services.llm_service import LLMService


class BaseAgent(ABC):

    name = ""

    def __init__(self):

        self.llm = LLMService()

    @abstractmethod
    def build_prompt(self, message):

        pass

    @abstractmethod
    def parse_response(self, response):

        pass

    def plan(self, message):

        prompt = self.build_prompt(message)

        response = self.llm.ask(prompt)

        return self.parse_response(response)