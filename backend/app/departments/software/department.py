from typing import Any, Optional

from app.agents.python.agent import PythonAgent
from app.departments.base.department import BaseDepartment
from app.departments.software.planner import SoftwarePlanner
from app.execution.result import ExecutionResult


class SoftwareDepartment(BaseDepartment):

    name = "software"

    def __init__(self, tool_registry: Optional[Any] = None):

        super().__init__(tool_registry)

        self.planner = SoftwarePlanner()
        self.register(PythonAgent())

    def plan(self, message: str) -> ExecutionResult:

        department_plan = self.planner.create_plan(message)

        agent_name = department_plan.get("agent", "python") if isinstance(department_plan, dict) else "python"
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