from app.departments.data.department import DataDepartment
from app.agents.sql.agent import SQLAgent
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool
from app.tools.registry import ToolRegistry


class MockPostgresTool(BaseTool):
    name = "postgres"

    def execute(self, plan):
        return ExecutionResult(
            success=True,
            tool=self.name,
            output=[{"count": 42}],
            error=None
        )


class MockLLM:
    def ask(self, prompt: str) -> str:
        return '{"tool":"postgres", "action":"query", "target":"SELECT COUNT(*)", "payload":{"sql":"SELECT COUNT(*)"}, "reason":"query"}'


def test_data_department():
    registry = ToolRegistry()
    registry.register(MockPostgresTool())

    department = DataDepartment(registry)
    mock_llm = MockLLM()
    department.register(SQLAgent(registry, llm=mock_llm))

    res = department.execute("sql", "SELECT COUNT(*) FROM sales")
    assert res.success is True
    assert res.output == [{"count": 42}]


if __name__ == "__main__":
    test_data_department()
    print("test_data_department: PASS")