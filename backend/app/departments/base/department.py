from abc import ABC

from app.agents.registry import AgentRegistry
from app.execution.engine import ExecutionEngine


class BaseDepartment(ABC):

    name = ""

    def __init__(self, tool_registry):

        self.registry = AgentRegistry()

        self.engine = ExecutionEngine(tool_registry)

        self.planner = None

    def register(self, agent):

        self.registry.register(agent)

    def get_agent(self, name):

        return self.registry.get(name)

    def agents(self):

        return self.registry.names()