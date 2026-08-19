from app.agents.registry import AgentRegistry
from app.agents.linux.agent import LinuxAgent
from app.agents.filesystem.agent import FileSystemAgent
from app.agents.python.agent import PythonAgent
from app.tools.registry import ToolRegistry


def test_agent_registry():
    tools = ToolRegistry()
    agents = AgentRegistry()

    agents.register(LinuxAgent(tools))
    agents.register(FileSystemAgent(tools))
    agents.register(PythonAgent(tools))

    names = agents.names()
    assert "linux" in names
    assert "filesystem" in names
    assert "python" in names

    assert agents.get("linux") is not None
    assert agents.get("python") is not None
    assert agents.get("filesystem") is not None
    assert agents.get("unknown") is None
    assert len(agents.list()) == 3


if __name__ == "__main__":
    test_agent_registry()
    print("test_agent_registry: PASS")