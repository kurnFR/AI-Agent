import tempfile
from pathlib import Path

from app.schemas.task_plan import TaskPlan
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.shell.tool import ShellTool


def test_tools_v2():
    with tempfile.TemporaryDirectory() as tmpdir:
        shell = ShellTool()
        filesystem = FileSystemTool(workspace_root=tmpdir)
        python = PythonTool()

        # Shell execution
        res_sh = shell.execute(
            TaskPlan(
                tool="shell",
                action="execute",
                target="pwd"
            )
        )
        assert res_sh.success is True
        assert res_sh.tool == "shell"

        # Filesystem execution
        res_fs = filesystem.execute(
            TaskPlan(
                tool="filesystem",
                action="list",
                target=tmpdir
            )
        )
        assert res_fs.success is True
        assert res_fs.tool == "filesystem"

        # Python execution
        res_py = python.execute(
            TaskPlan(
                tool="python",
                action="execute",
                target="print('hello')",
                payload={"code": "print('hello')"}
            )
        )
        assert res_py.success is True
        assert "hello" in res_py.output


if __name__ == "__main__":
    test_tools_v2()
    print("test_tools_v2: PASS")

