import json

from app.planning.planner import BasePlanner
from app.services.llm_service import LLMService


class DepartmentPlanner(BasePlanner):

    def __init__(self, department: str, agents: list[str]):

        self.department = department
        self.agents = agents
        self.llm = LLMService()

    def build_prompt(self, message: str):

        agent_list = "\n".join(f"- {a}" for a in self.agents)

        return f"""
You are the manager of the {self.department} Department.

Available agents:

{agent_list}

Return ONLY JSON.

Example:

{{
    "agent":"sql",
    "reason":"Need SQL expert"
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
