from app.agents.linux.agent import LinuxAgent
from app.departments.infrastructure.department import InfrastructureDepartment
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


class MockLLM:
    def ask(self, prompt: str) -> str:
        return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"print working dir"}'


def test_department_execute():
    tools = ToolRegistry()
    tools.register(ShellTool())

    mock_llm = MockLLM()
    department = InfrastructureDepartment(tools)
    department.register(LinuxAgent(tools, llm=mock_llm))

    agent_names = department.list()
    assert "linux" in agent_names

    result = department.execute("linux", "pwd")
    assert result.success is True
    assert result.tool == "shell"


if __name__ == "__main__":
    test_department_execute()
    print("test_department_execute: PASS")

