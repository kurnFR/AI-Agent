from abc import ABC, abstractmethod

from app.schemas.task_plan import TaskPlan
from app.execution.result import ExecutionResult


class BaseTool(ABC):

    name = ""

    @abstractmethod
    def execute(
        self,
        plan: TaskPlan
    ) -> ExecutionResult:
        pass