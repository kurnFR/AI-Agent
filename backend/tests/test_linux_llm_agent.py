from app.tools.registry import ToolRegistry
from backend.app.tools.shell.tool import ShellTool
from app.agents.linux.agent import LinuxAgent


registry = ToolRegistry()

registry.register(ShellTool())

agent = LinuxAgent(registry)


tests = [
    "find current directory",
    "show current user",
    "show current files"
]


for goal in tests:

    print("=" * 60)
    print("Goal :", goal)

    result = agent.execute(goal)

    print(result)
