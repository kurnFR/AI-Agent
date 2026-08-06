from app.departments.base.department import BaseDepartment


class SoftwareDepartment(BaseDepartment):

    name = "software"

    def execute(self, agent_name, message):

        agent = self.get(agent_name)

        if agent is None:

            return {
                "success": False,
                "error": f"Agent '{agent_name}' not found."
            }

        return agent.execute(message)