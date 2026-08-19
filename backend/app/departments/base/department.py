from abc import ABC
from typing import Any, List, Optional

from app.agents.registry import AgentRegistry
from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.schemas.task_plan import TaskPlan
from app.tools.registry import ToolRegistry


class BaseDepartment(ABC):

    name = ""

    def __init__(self, tool_registry: Optional[Any] = None):

        if tool_registry is None:
            tool_registry = ToolRegistry()

        self.registry = AgentRegistry()

        if isinstance(tool_registry, ExecutionEngine):
            self.engine = tool_registry
        else:
            self.engine = ExecutionEngine(tool_registry)

        self.planner = None

    def register(self, agent):

        self.registry.register(agent)

    def get_agent(self, name: str):

        return self.registry.get(name)

    def agents(self) -> List[str]:

        return self.registry.names()

    def list(self) -> List[str]:

        return self.registry.names()

    def plan(self, message: str) -> ExecutionResult:

        raise NotImplementedError

    def execute(self, *args, **kwargs) -> ExecutionResult:

        if len(args) == 1 and isinstance(args[0], TaskPlan):
            return self.engine.execute(args[0])
        elif len(args) == 1 and isinstance(args[0], str):
            return self.plan(args[0])
        elif len(args) == 2:
            agent_name, message = args[0], args[1]
            agent = self.get_agent(agent_name)
            if not agent:
                return ExecutionResult(
                    success=False,
                    tool=self.name,
                    output=None,
                    error=f"Agent '{agent_name}' not found in department '{self.name}'."
                )
            task_plan = agent.plan(message)
            return self.engine.execute(task_plan)
        raise ValueError(f"Invalid execute arguments: {args}")