import json

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan


class SQLAgent(BaseAgent):

    name = "sql"

    def build_prompt(self, message):

        return f"""
You are a senior SQL expert.

Return ONLY JSON.

Example:

{{
    "tool":"postgres",
    "action":"query",
    "target":"default",
    "payload":{{
        "sql":"SELECT * FROM customer"
    }},
    "reason":"Execute SQL query"
}}

User:

{message}
"""

    def parse_response(self, response):

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        plan = json.loads(response)

        return TaskPlan(
            tool=plan["tool"],
            action=plan["action"],
            target=plan.get("target", ""),
            payload=plan.get("payload", {}),
            reason=plan.get("reason", "")
        )