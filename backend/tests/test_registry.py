from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


def test_tool_registry():
    registry = ToolRegistry()

    fs = FileSystemTool()
    sh = ShellTool()
    py = PythonTool()

    registry.register(fs)
    registry.register(sh)
    registry.register(py)

    tools = registry.list_tools()
    assert "filesystem" in tools
    assert "shell" in tools
    assert "python" in tools

    assert registry.get("filesystem") is fs
    assert registry.get("shell") is sh
    assert registry.get("python") is py
    assert registry.get("unknown") is None


if __name__ == "__main__":
    test_tool_registry()
    print("test_tool_registry: PASS")

