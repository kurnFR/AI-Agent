from app.execution.engine import ExecutionEngine
from app.schemas.execution_plan import ExecutionPlan

from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


registry = ToolRegistry()
registry.register(ShellTool())

engine = ExecutionEngine(registry)

plan = ExecutionPlan(
    tool="shell",
    action="run",
    arguments={
        "command": "pwd"
    }
)

print(engine.execute(plan))
