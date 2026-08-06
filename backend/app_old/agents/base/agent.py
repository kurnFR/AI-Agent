from abc import ABC, abstractmethod

from app.execution.engine import ExecutionEngine
from app.services.llm_service import LLMService


class BaseAgent(ABC):

    name = ""

    def __init__(self, registry):

        self.registry = registry
        self.llm = LLMService()
        self.engine = ExecutionEngine(registry)

    @abstractmethod
    def build_prompt(self, goal):
        pass

    @abstractmethod
    def parse_response(self, response):
        pass

    def execute(self, goal):

        prompt = self.build_prompt(goal)

        response = self.llm.ask(prompt)

        plan = self.parse_response(response)

        return self.engine.execute(plan)