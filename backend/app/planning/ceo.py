from typing import Optional

from app.planning.planner import BasePlanner
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class CEOPlanner(BasePlanner):

    def __init__(self, llm: Optional[LLMService] = None):

        self.llm = llm or LLMService()

    def build_prompt(self, message: str) -> str:

        return f"""
You are the CEO of an AI company.

Available departments:

- infrastructure
- data
- software
- chat

Return ONLY JSON.

Example:

{{
    "department":"infrastructure",
    "reason":"Need Linux task"
}}

User:

{message}
"""

    def parse_response(self, response: str):

        plan = extract_json(response)
        if not plan or "department" not in plan:
            return {"department": "software", "reason": "Default fallback"}
        return plan

    def create_plan(self, message: str):

        prompt = self.build_prompt(message)

        try:
            response = self.llm.ask(prompt)
            return self.parse_response(response)
        except Exception:
            return {"department": "software", "reason": "Execution fallback"}

