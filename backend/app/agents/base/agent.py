from abc import ABC, abstractmethod
from typing import Any, Optional

from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.schemas.task_plan import TaskPlan
from app.services.llm_service import LLMService


class BaseAgent(ABC):

    name = ""

    def __init__(self, tools_or_registry: Optional[Any] = None, llm: Optional[LLMService] = None):

        self.llm = llm or LLMService()
        self.engine = None
        if tools_or_registry is not None:
            if hasattr(tools_or_registry, "get"):
                self.engine = ExecutionEngine(tools_or_registry)
            elif isinstance(tools_or_registry, ExecutionEngine):
                self.engine = tools_or_registry

    @abstractmethod
    def build_prompt(self, message: str) -> str:
        pass

    @abstractmethod
    def parse_response(self, response: str) -> TaskPlan:
        pass

    def plan(self, message: str) -> TaskPlan:

        prompt = self.build_prompt(message)
        response = self.llm.ask(prompt)
        return self.parse_response(response)

    def execute(self, message: str) -> ExecutionResult:

        task_plan = self.plan(message)
        if self.engine is None:
            raise RuntimeError(f"Agent '{self.name}' has no tool registry or execution engine configured.")
        return self.engine.execute(task_plan)