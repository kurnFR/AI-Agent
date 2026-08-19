from typing import Any, Optional

from app.agents.filesystem.agent import FileSystemAgent
from app.agents.linux.agent import LinuxAgent
from app.departments.base.department import BaseDepartment
from app.departments.infrastructure.planner import InfrastructurePlanner
from app.execution.result import ExecutionResult


class InfrastructureDepartment(BaseDepartment):

    name = "infrastructure"

    def __init__(self, tool_registry: Optional[Any] = None):

        super().__init__(tool_registry)

        self.planner = InfrastructurePlanner()
        self.register(LinuxAgent())
        self.register(FileSystemAgent())

    def plan(self, message: str) -> ExecutionResult:

        department_plan = self.planner.create_plan(message)

        agent_name = department_plan.get("agent", "linux") if isinstance(department_plan, dict) else "linux"
        agent = self.get_agent(agent_name)

        if agent is None:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=f"Agent '{agent_name}' not found."
            )

        task_plan = agent.plan(message)

        return self.engine.execute(task_plan)