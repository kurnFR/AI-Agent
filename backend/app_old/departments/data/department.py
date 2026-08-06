from app.agents.registry import AgentRegistry

from app.departments.data.planner import DataPlanner


class DataDepartment:

    name = "data"

    def __init__(self):

        self.registry = AgentRegistry()
        self.planner = DataPlanner()

    def register(self, agent):

        self.registry.register(agent)

    def execute(self, message: str):

        plan = self.planner.create_plan(message)

        agent = self.registry.get(plan["agent"])

        if agent is None:

            return {
                "success": False,
                "error": f"Agent '{plan['agent']}' not found."
            }

        return agent.execute(message)
