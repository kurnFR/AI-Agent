import json

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan


class FileSystemAgent(BaseAgent):

    name = "filesystem"

    def build_prompt(self, goal):

        return f"""
You are a filesystem expert.

Return ONLY JSON.

Example:

{{
    "action":"list",
    "path":"/app"
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
            tool="filesystem",
            action=data["action"],
            path=data["path"]
        )