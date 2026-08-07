import json

from app.services.llm_service import LLMService


class SoftwarePlanner:

    def __init__(self):

        self.llm = LLMService()

    def create_plan(self, message):

        prompt = f"""
You are the Software Manager.

Available agents:

- python

Return ONLY JSON.

Example:

{{
    "agent":"python"
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