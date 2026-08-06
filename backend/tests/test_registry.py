from app.tools.registry import ToolRegistry
from backend.app.tools.filesystem.tool import FileSystemTool
from backend.app.tools.shell.tool import ShellTool
from backend.app.tools.python.tool import PythonTool

registry = ToolRegistry()

registry.register(FileSystemTool())
registry.register(ShellTool())
registry.register(PythonTool())

print(registry.list_tools())
