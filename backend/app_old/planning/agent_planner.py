class Manager:

    def __init__(
        self,
        planner,
        agent_registry,
        tool_registry
    ):

        self.planner = planner
        self.agent_registry = agent_registry

        from app.execution.engine import ExecutionEngine

        self.engine = ExecutionEngine(tool_registry)

    def execute(self, goal: str):

        decision = self.planner.plan(goal)

        agent_name = decision["agent"]

        agent = self.agent_registry.get(agent_name)

        if agent is None:

            return {
                "success": False,
                "error": "Unknown agent."
            }

        plan = agent.plan(goal)

        return self.engine.execute(plan)