import json

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan


class PythonAgent(BaseAgent):

    name = "python"

    def build_prompt(self, message):

        return f"""
You are a senior Python developer.

Return ONLY JSON.

Example:

{{
    "tool":"python",
    "action":"execute",
    "target":"",
    "payload":{{
        "code":"print('hello')"
    }},
    "reason":"Execute Python code"
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