from app.departments.infrastructure.department import InfrastructureDepartment

from app.agents.linux.agent import LinuxAgent

from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


tools = ToolRegistry()
tools.register(ShellTool())


department = InfrastructureDepartment()

department.register(
    LinuxAgent(tools)
)

print("=" * 60)
print(department.list())

print("=" * 60)
print(
    department.execute(
        "linux",
        "pwd"
    )
)
