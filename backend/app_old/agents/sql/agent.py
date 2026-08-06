import json

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan


class SQLAgent(BaseAgent):

    name = "sql"

    def build_prompt(self, goal):

        return f"""
You are a senior SQL expert.

Return ONLY JSON.

Example:

{{
    "action":"query",
    "sql":"SELECT * FROM customer",
    "reason":"Retrieve customer data"
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
            tool="postgres",
            action=data["action"],
            command=data["sql"]
        )