from abc import ABC
from abc import abstractmethod

from app.schemas.task_plan import TaskPlan


class BaseTool(ABC):

    name = ""

    @abstractmethod
    def execute(self, plan: TaskPlan):
        pass

