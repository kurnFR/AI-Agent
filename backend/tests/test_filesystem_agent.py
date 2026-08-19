from app.agents.filesystem.agent import FileSystemAgent
from app.tools.filesystem.tool import FileSystemTool
from app.tools.registry import ToolRegistry


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "list" in prompt:
            return '{"tool":"filesystem", "action":"list", "target":"/app", "payload":{}, "reason":"List app"}'
        elif "read" in prompt:
            return '{"tool":"filesystem", "action":"read", "target":"/app/requirements.txt", "payload":{}, "reason":"Read requirements"}'
        return '{"tool":"filesystem", "action":"list", "target":"/", "payload":{}, "reason":"Default"}'


def test_filesystem_agent():
    registry = ToolRegistry()
    registry.register(FileSystemTool())

    mock_llm = MockLLM()
    agent = FileSystemAgent(registry, llm=mock_llm)

    # 1. Plan list
    plan1 = agent.plan("list /app")
    assert plan1.tool == "filesystem"
    assert plan1.action == "list"
    assert plan1.target == "/app"

    # 2. Plan read
    plan2 = agent.plan("read /app/requirements.txt")
    assert plan2.tool == "filesystem"
    assert plan2.action == "read"
    assert plan2.target == "/app/requirements.txt"


if __name__ == "__main__":
    test_filesystem_agent()
    print("test_filesystem_agent: PASS")

