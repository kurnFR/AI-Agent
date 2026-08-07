from app.tools.registry import ToolRegistry

from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool

from app.agents.linux.agent import LinuxAgent
from app.agents.filesystem.agent import FileSystemAgent

from app.departments.infrastructure.department import InfrastructureDepartment


registry = ToolRegistry()

registry.register(ShellTool())
registry.register(FileSystemTool())
registry.register(PythonTool())


department = InfrastructureDepartment(registry)

department.register(LinuxAgent())
department.register(FileSystemAgent())


print("=" * 60)

result = department.plan(
    "show current directory"
)

print(result)
