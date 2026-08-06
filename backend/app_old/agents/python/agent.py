import json

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan


class PythonAgent(BaseAgent):

    name = "python"

    def build_prompt(self, goal):

        return f"""
You are a senior Python developer.

Return ONLY JSON.

Example:

{{
    "code":"print('hello world')"
}}

User:

{goal}
"""

    def parse_response(self, response):

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        data = json.loads(response)

        return TaskPlan(
            tool="python",
            action="execute",
            command=data["code"]
        )