from app.agents.filesystem.agent import FileSystemAgent
from app.agents.linux.agent import LinuxAgent
from app.agents.python.agent import PythonAgent
from app.agents.sql.agent import SQLAgent
from app.ceo.ceo import CEO
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool
from app.tools.registry import ToolRegistry
from app.tools.shell.tool import ShellTool


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "infrastructure" in prompt.lower() or "linux" in prompt.lower() or "directory" in prompt.lower():
            if "agent" in prompt:
                return '{"agent":"linux"}'
            return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"Show current directory"}'
        elif "python" in prompt.lower():
            if "agent" in prompt:
                return '{"agent":"python"}'
            return '{"tool":"python", "action":"execute", "target":"", "payload":{"code":"print(\'hello world\')"}, "reason":"Python task"}'
        elif "sql" in prompt.lower() or "customer" in prompt.lower():
            if "agent" in prompt:
                return '{"agent":"sql"}'
            return '{"tool":"postgres", "action":"query", "target":"SELECT 1", "payload":{"sql":"SELECT 1"}, "reason":"SQL task"}'
        return '{"department":"software", "reason":"default"}'


def test_ceo_pipeline():
    mock_llm = MockLLM()
    registry = ToolRegistry()
    registry.register(ShellTool())
    registry.register(FileSystemTool())
    registry.register(PythonTool())

    infra = InfrastructureDepartment(registry)
    infra.planner.llm = mock_llm
    infra.register(LinuxAgent(registry, llm=mock_llm))
    infra.register(FileSystemAgent(registry, llm=mock_llm))

    data = DataDepartment(registry)
    data.planner.llm = mock_llm
    data.register(SQLAgent(registry, llm=mock_llm))

    software = SoftwareDepartment(registry)
    software.planner.llm = mock_llm
    software.register(PythonAgent(registry, llm=mock_llm))

    ceo = CEO(auto_register=False)
    ceo.planner.llm = mock_llm
    ceo.register(infra)
    ceo.register(data)
    ceo.register(software)

    result_py = software.plan("write hello world in python")
    assert result_py.success is True
    assert "hello world" in result_py.output


if __name__ == "__main__":
    test_ceo_pipeline()
    print("test_ceo_pipeline: PASS")

