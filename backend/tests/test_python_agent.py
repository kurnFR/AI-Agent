from app.tools.registry import ToolRegistry
from backend.app.tools.python.tool import PythonTool
from backend.app.agents.python.agent import PythonAgent

registry = ToolRegistry()
registry.register(PythonTool())

agent = PythonAgent(registry)

tests = [
    "print('Hello AI')",
    "for i in range(3): print(i)",
    "x = 10\nprint(x * 2)",
]

for code in tests:

    print("=" * 60)
    print(code)
    print(agent.execute(code))
