import json

from app.services.llm_service import LLMService


class Planner:

    def __init__(self):

        self.llm = LLMService()

    def create_plan(self, message: str):

        prompt = f"""
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
    "reason":"Need Linux command"
}}

User:

{message}
"""

        response = self.llm.ask(prompt)

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)
