import json

from app.planning.planner import BasePlanner
from app.services.llm_service import LLMService


class CEOPlanner(BasePlanner):

    def __init__(self):

        self.llm = LLMService()

    def build_prompt(self, message: str):

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

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)

    def create_plan(self, message: str):

        prompt = self.build_prompt(message)

        response = self.llm.ask(prompt)

        return self.parse_response(response)
