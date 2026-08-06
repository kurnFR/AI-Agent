from app.services.llm_service import LLMService
from app.tools.registry import ToolRegistry

from .prompt import SYSTEM_PROMPT
from .parser import parse


class LinuxAgent:

    name = "linux"

    def __init__(self, registry: ToolRegistry):

        self.registry = registry
        self.llm = LLMService()

    def execute(self, goal: str):

        prompt = f"""
{SYSTEM_PROMPT}

Goal:

{goal}
"""

        response = self.llm.ask(prompt)

        plan = parse(response)

        tool = self.registry.get(plan["tool"])

        return tool.run(plan["command"])
