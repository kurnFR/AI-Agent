from typing import Any, Optional

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class FileSystemAgent(BaseAgent):

    name = "filesystem"

    def __init__(self, tools_or_registry: Optional[Any] = None, llm: Optional[LLMService] = None):
        super().__init__(tools_or_registry=tools_or_registry, llm=llm)

    def build_prompt(self, message: str) -> str:

        return f"""
You are a filesystem expert.

Return ONLY JSON.

Example:

{{
    "tool":"filesystem",
    "action":"list",
    "target":"/app",
    "payload":{{}},
    "reason":"List application directory"
}}

User:

{message}
"""

    def parse_response(self, response: str) -> TaskPlan:

        plan = extract_json(response)

        tool = plan.get("tool", "filesystem")
        action = plan.get("action", "list")
        target = plan.get("target", "") or plan.get("path", "")
        payload = plan.get("payload", {})
        reason = plan.get("reason", "Filesystem action")

        return TaskPlan(
            tool=tool,
            action=action,
            target=target,
            payload=payload,
            reason=reason
        )