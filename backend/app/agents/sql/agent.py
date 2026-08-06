import json

from app.agents.base.agent import BaseAgent


class SQLAgent(BaseAgent):

    name = "sql"

    def build_prompt(self, message: str):

        return f"""
You are a senior SQL engineer.

Return ONLY JSON.

Example:

{{
    "tool":"postgres",
    "query":"SELECT * FROM customer",
    "reason":"Execute SQL"
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
