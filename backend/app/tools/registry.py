from typing import Dict, List, Optional
from app.tools.base.tool import BaseTool
from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.postgres.tool import PostgresTool

from app.config import DATABASE_URL


class ToolRegistry:

    def __init__(self):

        self.tools: Dict[str, BaseTool] = {}

        self.register(ShellTool())
        self.register(FileSystemTool())
        self.register(PythonTool())
        try:
            self.register(PostgresTool(DATABASE_URL))
        except Exception:
            pass

    def register(self, tool):

        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:

        return self.tools.get(name)

    def exists(self, name: str) -> bool:

        return name in self.tools

    def names(self) -> List[str]:

        return sorted(self.tools.keys())

    def list(self) -> List[BaseTool]:

        return list(self.tools.values())