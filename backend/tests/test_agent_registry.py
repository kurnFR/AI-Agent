from app.agents.registry import AgentRegistry

from app.agents.linux.agent import LinuxAgent
from app.agents.filesystem.agent import FileSystemAgent
from app.agents.python.agent import PythonAgent

from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool


tools = ToolRegistry()

tools.register(ShellTool())
tools.register(FileSystemTool())
tools.register(PythonTool())


agents = AgentRegistry()

agents.register(LinuxAgent(tools))
agents.register(FileSystemAgent(tools))
agents.register(PythonAgent(tools))


print(agents.list())

print(agents.get("linux"))
print(agents.get("python"))
print(agents.get("filesystem"))