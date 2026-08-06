from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool

from app.agents.linux.agent import LinuxAgent


registry = ToolRegistry()
registry.register(ShellTool())

agent = LinuxAgent(registry)

tests = [
    "pwd",
    "whoami",
    "ls"
]

for cmd in tests:

    print("=" * 60)
    print(cmd)
    print(agent.execute(cmd))