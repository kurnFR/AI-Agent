from typing import Any, Optional

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class LinuxAgent(BaseAgent):

    name = "linux"

    def __init__(self, tools_or_registry: Optional[Any] = None, llm: Optional[LLMService] = None):
        super().__init__(tools_or_registry=tools_or_registry, llm=llm)

    def build_prompt(self, message: str) -> str:

        return f"""
You are a senior Linux administrator.

Return ONLY JSON.

Example:

{{
    "tool":"shell",
    "action":"execute",
    "target":"pwd",
    "payload":{{}},
    "reason":"Show current directory"
}}

User:

{message}
"""

    def parse_response(self, response: str) -> TaskPlan:

        plan = extract_json(response)

        tool = plan.get("tool", "shell")
        action = plan.get("action", "execute")
        target = plan.get("target", "") or plan.get("command", "")
        payload = plan.get("payload", {})
        reason = plan.get("reason", "Linux command execution")

        return TaskPlan(
            tool=tool,
            action=action,
            target=target,
            payload=payload,
            reason=reason
        )