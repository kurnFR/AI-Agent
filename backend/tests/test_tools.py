from app.execution.engine import ExecutionEngine
from app.schemas.task_plan import TaskPlan
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


registry = ToolRegistry()

registry.register(ShellTool())
registry.register(FileSystemTool())
registry.register(PythonTool())

engine = ExecutionEngine(registry)

tests = [

    TaskPlan(
        tool="shell",
        command="pwd"
    ),

    TaskPlan(
        tool="filesystem",
        action="list",
        path="/app"
    ),

    TaskPlan(
        tool="python",
        code="print('hello')"
    )

]

for plan in tests:

    print("=" * 60)

    print(engine.execute(plan))
