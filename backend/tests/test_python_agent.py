from app.agents.python.agent import PythonAgent
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "print('Hello AI')" in prompt:
            return '{"tool":"python", "action":"execute", "target":"print(\'Hello AI\')", "payload":{"code":"print(\'Hello AI\')"}, "reason":"Print hello"}'
        return '{"tool":"python", "action":"execute", "target":"print(1+1)", "payload":{"code":"print(1+1)"}, "reason":"Math"}'


def test_python_agent():
    registry = ToolRegistry()
    registry.register(PythonTool())

    mock_llm = MockLLM()
    agent = PythonAgent(registry, llm=mock_llm)

    # 1. Plan
    plan = agent.plan("print('Hello AI')")
    assert plan.tool == "python"
    assert plan.payload.get("code") == "print('Hello AI')"

    # 2. Execute
    res = agent.execute("print('Hello AI')")
    assert res.success is True
    assert res.tool == "python"
    assert "Hello AI" in res.output


if __name__ == "__main__":
    test_python_agent()
    print("test_python_agent: PASS")

