from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.postgres.tool import PostgresTool

from app.config import DATABASE_URL


class ToolRegistry:

    def __init__(self):

        self.tools = {}

        self.register(ShellTool())
        self.register(FileSystemTool())
        self.register(PythonTool())
        self.register(
            PostgresTool(DATABASE_URL)
        )

    def register(self, tool):

        self.tools[tool.name] = tool

    def get(self, name):

        return self.tools.get(name)

    def exists(self, name):

        return name in self.tools

    def names(self):

        return sorted(self.tools.keys())