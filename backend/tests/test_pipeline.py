from app.agents.filesystem.agent import FileSystemAgent
from app.agents.linux.agent import LinuxAgent
from app.departments.infrastructure.department import InfrastructureDepartment
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "agent" in prompt:
            return '{"agent":"linux"}'
        return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"Current directory"}'


def test_pipeline():
    registry = ToolRegistry()
    registry.register(ShellTool())
    registry.register(FileSystemTool())
    registry.register(PythonTool())

    mock_llm = MockLLM()
    department = InfrastructureDepartment(registry)
    department.planner.llm = mock_llm
    department.register(LinuxAgent(registry, llm=mock_llm))
    department.register(FileSystemAgent(registry, llm=mock_llm))

    plan = department.plan("show current directory")
    assert plan.tool == "shell"
    assert plan.target == "pwd"

    res = department.execute(plan)
    assert res.success is True
    assert res.tool == "shell"
    assert "stdout" in res.output


if __name__ == "__main__":
    test_pipeline()
    print("test_pipeline: PASS")

