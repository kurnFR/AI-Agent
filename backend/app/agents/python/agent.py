from typing import Any, Optional

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class PythonAgent(BaseAgent):

    name = "python"

    def __init__(self, tools_or_registry: Optional[Any] = None, llm: Optional[LLMService] = None):
        super().__init__(tools_or_registry=tools_or_registry, llm=llm)

    def build_prompt(self, message: str) -> str:

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

    def parse_response(self, response: str) -> TaskPlan:

        plan = extract_json(response)

        tool = plan.get("tool", "python")
        action = plan.get("action", "execute")
        target = plan.get("target", "")
        payload = plan.get("payload", {})
        if "code" not in payload and "code" in plan:
            payload["code"] = plan["code"]

        reason = plan.get("reason", "Execute Python code")

        return TaskPlan(
            tool=tool,
            action=action,
            target=target,
            payload=payload,
            reason=reason
        )