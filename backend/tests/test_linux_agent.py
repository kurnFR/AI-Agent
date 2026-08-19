from app.agents.linux.agent import LinuxAgent
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "pwd" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"Current directory"}'
        elif "whoami" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"whoami", "payload":{}, "reason":"Current user"}'
        return '{"tool":"shell", "action":"execute", "target":"ls", "payload":{}, "reason":"List directory"}'


def test_linux_agent():
    registry = ToolRegistry()
    registry.register(ShellTool())

    mock_llm = MockLLM()
    agent = LinuxAgent(registry, llm=mock_llm)

    # 1. Plan pwd
    plan1 = agent.plan("pwd")
    assert plan1.tool == "shell"
    assert plan1.target == "pwd"

    # 2. Plan whoami
    plan2 = agent.plan("whoami")
    assert plan2.tool == "shell"
    assert plan2.target == "whoami"

    # 3. Execute pwd
    res = agent.execute("pwd")
    assert res.success is True
    assert res.tool == "shell"
    assert "stdout" in res.output


if __name__ == "__main__":
    test_linux_agent()
    print("test_linux_agent: PASS")