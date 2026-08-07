from app.departments.base.department import BaseDepartment

from app.departments.infrastructure.planner import InfrastructurePlanner


class InfrastructureDepartment(BaseDepartment):

    name = "infrastructure"

    def __init__(self, tool_registry):

        super().__init__(tool_registry)

        self.planner = InfrastructurePlanner()

    def plan(self, message):

        department_plan = self.planner.create_plan(message)

        agent = self.get_agent(
            department_plan["agent"]
        )

        if agent is None:

            raise Exception(
                f"Agent '{department_plan['agent']}' not found."
            )

        task_plan = agent.plan(message)

        return self.engine.execute(task_plan)