from app.agents.filesystem.agent import FileSystemAgent
from app.agents.linux.agent import LinuxAgent
from app.agents.sql.agent import SQLAgent
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool
from app.tools.registry import ToolRegistry


class MockPostgresTool(BaseTool):
    name = "postgres"

    def execute(self, plan):
        return ExecutionResult(
            success=True,
            tool=self.name,
            output=[{"status": "ok"}],
            error=None
        )


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "agent" in prompt:
            if "Infrastructure" in prompt:
                return '{"agent":"linux"}'
            elif "Data" in prompt:
                return '{"agent":"sql"}'
        if "disk" in prompt:
            return '{"tool":"shell", "action":"execute", "target":"df -h", "payload":{}, "reason":"disk"}'
        elif "customer" in prompt:
            return '{"tool":"postgres", "action":"query", "target":"SELECT * FROM customer", "payload":{"sql":"SELECT * FROM customer"}, "reason":"sql"}'
        return '{"tool":"shell", "action":"execute", "target":"pwd", "payload":{}, "reason":"default"}'


def test_departments():
    tools = ToolRegistry()
    tools.register(MockPostgresTool())

    mock_llm = MockLLM()
    infra = InfrastructureDepartment(tools)
    infra.planner.llm = mock_llm
    infra.register(LinuxAgent(tools, llm=mock_llm))
    infra.register(FileSystemAgent(tools, llm=mock_llm))

    res_infra = infra.plan("show disk usage")
    assert res_infra.success is True
    assert res_infra.tool == "shell"

    data = DataDepartment(tools)
    data.planner.llm = mock_llm
    data.register(SQLAgent(tools, llm=mock_llm))

    res_data = data.plan("SELECT * FROM customer")
    assert res_data.success is True
    assert res_data.tool == "postgres"


if __name__ == "__main__":
    test_departments()
    print("test_departments: PASS")

