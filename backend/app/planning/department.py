from typing import List, Optional

from app.planning.planner import BasePlanner
from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class DepartmentPlanner(BasePlanner):

    def __init__(self, department: str, agents: List[str], llm: Optional[LLMService] = None):

        self.department = department
        self.agents = agents
        self.llm = llm or LLMService()

    def build_prompt(self, message: str) -> str:

        agent_list = "\n".join(f"- {a}" for a in self.agents)

        return f"""
You are the manager of the {self.department} Department.

Available agents:

{agent_list}

Return ONLY JSON.

Example:

{{
    "agent":"{self.agents[0] if self.agents else 'default'}",
    "reason":"Need expert"
}}

User:

{message}
"""

    def parse_response(self, response: str):

        plan = extract_json(response)
        if not plan or "agent" not in plan:
            fallback_agent = self.agents[0] if self.agents else "default"
            return {"agent": fallback_agent, "reason": "Default fallback"}
        return plan

    def create_plan(self, message: str):

        prompt = self.build_prompt(message)

        try:
            response = self.llm.ask(prompt)
            return self.parse_response(response)
        except Exception:
            fallback_agent = self.agents[0] if self.agents else "default"
            return {"agent": fallback_agent, "reason": "Execution fallback"}

