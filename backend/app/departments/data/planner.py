from typing import Optional

from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class DataPlanner:

    def __init__(self, llm: Optional[LLMService] = None):

        self.llm = llm or LLMService()

    def create_plan(self, message: str):

        prompt = f"""
You are the manager of the Data Department.

Available agents:

- sql

Return ONLY JSON.

Example:

{{
    "agent":"sql"
}}

User:

{message}
"""

        try:
            response = self.llm.ask(prompt)
            plan = extract_json(response)
        except Exception:
            plan = {}

        if "agent" not in plan or not plan["agent"]:
            plan = {"agent": "sql"}

        return plan