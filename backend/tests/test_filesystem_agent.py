from app.tools.registry import ToolRegistry
from backend.app.tools.filesystem.tool import FileSystemTool
from backend.app.agents.filesystem.agent import FileSystemAgent

registry = ToolRegistry()
registry.register(FileSystemTool())

agent = FileSystemAgent(registry)

tests = [
    "list /app",
    "list /app/app",
    "read /app/requirements.txt",
]

for t in tests:
    print("=" * 60)
    print(t)
    print(agent.execute(t))
