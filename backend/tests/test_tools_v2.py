from app.schemas.task_plan import TaskPlan

from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool


shell = ShellTool()

filesystem = FileSystemTool()

python = PythonTool()


print("=" * 60)

print(
    shell.execute(
        TaskPlan(
            tool="shell",
            action="run",
            parameters={
                "command": "pwd"
            }
        )
    )
)

print("=" * 60)

print(
    filesystem.execute(
        TaskPlan(
            tool="filesystem",
            action="list",
            parameters={
                "path": "/app"
            }
        )
    )
)

print("=" * 60)

print(
    python.execute(
        TaskPlan(
            tool="python",
            action="execute",
            parameters={
                "code": "print('hello')"
            }
        )
    )
)
