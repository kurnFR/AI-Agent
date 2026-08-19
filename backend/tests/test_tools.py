import tempfile
from pathlib import Path

from app.execution.engine import ExecutionEngine
from app.schemas.task_plan import TaskPlan
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


def test_tools():
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ToolRegistry()
        registry.register(ShellTool())
        registry.register(FileSystemTool(workspace_root=tmpdir))
        registry.register(PythonTool())

        engine = ExecutionEngine(registry)

        # 1. Shell tool execution
        res_sh = engine.execute(TaskPlan(
            tool="shell",
            action="execute",
            target="pwd"
        ))
        assert res_sh.success is True
        assert res_sh.tool == "shell"

        # 2. Filesystem tool execution
        test_file = Path(tmpdir) / "sample.txt"
        res_fs = engine.execute(TaskPlan(
            tool="filesystem",
            action="write",
            target=str(test_file),
            payload={"content": "sample"}
        ))
        assert res_fs.success is True
        assert res_fs.tool == "filesystem"
        assert test_file.exists()

        # 3. Python tool execution
        res_py = engine.execute(TaskPlan(
            tool="python",
            action="execute",
            target="print('hello')"
        ))
        assert res_py.success is True
        assert res_py.tool == "python"
        assert "hello" in res_py.output


if __name__ == "__main__":
    test_tools()
    print("test_tools: PASS")

