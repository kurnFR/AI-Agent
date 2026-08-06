import json

from app.services.llm_service import LLMService


class DataPlanner:

    def __init__(self):

        self.llm = LLMService()

    def create_plan(self, message: str):

        prompt = f"""
You are the manager of the Data Department.

Available agents:

- sql
- bi
- chat

Return ONLY JSON.

Example:

{{
    "agent":"sql",
    "reason":"SQL query"
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
