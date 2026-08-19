from typing import Any, Optional

from app.agents.base.agent import BaseAgent
from app.schemas.task_plan import TaskPlan
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class SQLAgent(BaseAgent):

    name = "sql"

    def __init__(self, tools_or_registry: Optional[Any] = None, llm: Optional[LLMService] = None):
        super().__init__(tools_or_registry=tools_or_registry, llm=llm)

    def build_prompt(self, message: str) -> str:

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

    def parse_response(self, response: str) -> TaskPlan:

        plan = extract_json(response)

        tool = plan.get("tool", "postgres")
        action = plan.get("action", "query")
        target = plan.get("target", "default")
        payload = plan.get("payload", {})
        if "sql" not in payload and "sql" in plan:
            payload["sql"] = plan["sql"]

        reason = plan.get("reason", "Execute SQL query")

        return TaskPlan(
            tool=tool,
            action=action,
            target=target,
            payload=payload,
            reason=reason
        )