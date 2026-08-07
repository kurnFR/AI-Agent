from app.departments.base.department import BaseDepartment

from app.departments.software.planner import SoftwarePlanner


class SoftwareDepartment(BaseDepartment):

    name = "software"

    def __init__(self, tool_registry):

        super().__init__(tool_registry)

        self.planner = SoftwarePlanner()

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