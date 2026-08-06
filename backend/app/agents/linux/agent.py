from app.agents.base.agent import BaseAgent

from .parser import parse
from .prompt import SYSTEM_PROMPT


class LinuxAgent(BaseAgent):

    name = "linux"

    def build_prompt(self, message: str):

        return f"""
{SYSTEM_PROMPT}

User:

{message}
"""

    def parse_response(self, response: str):

        return parse(response)
