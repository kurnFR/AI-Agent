from app.agents.linux.agent import LinuxAgent
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "directory" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"Current directory"}'
        elif "user" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"whoami", "payload":{}, "reason":"Current user"}'
        elif "files" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"ls -la", "payload":{}, "reason":"Show files"}'
        return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"Default"}'


def test_linux_llm_agent():
    registry = ToolRegistry()
    registry.register(ShellTool())

    mock_llm = MockLLM()
    agent = LinuxAgent(registry, llm=mock_llm)

    res_dir = agent.execute("find current directory")
    assert res_dir.success is True
    assert res_dir.tool == "shell"

    res_user = agent.execute("show current user")
    assert res_user.success is True
    assert res_user.tool == "shell"

    res_files = agent.execute("show current files")
    assert res_files.success is True
    assert res_files.tool == "shell"


if __name__ == "__main__":
    test_linux_llm_agent()
    print("test_linux_llm_agent: PASS")

