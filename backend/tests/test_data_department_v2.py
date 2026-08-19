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
            output=[{"customer_id": 1, "name": "Alice"}],
            error=None
        )


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "agent" in prompt:
            return '{"agent":"sql"}'
        return '{"tool":"postgres", "action":"query", "target":"SELECT * FROM customer", "payload":{"sql":"SELECT * FROM customer"}, "reason":"Fetch customer"}'


def test_data_department_v2():
    registry = ToolRegistry()
    registry.register(MockPostgresTool())

    mock_llm = MockLLM()
    department = DataDepartment(registry)
    department.planner.llm = mock_llm
    department.register(SQLAgent(registry, llm=mock_llm))

    result = department.execute("SELECT * FROM customer")
    assert result.success is True
    assert len(result.output) == 1
    assert result.output[0]["name"] == "Alice"


if __name__ == "__main__":
    test_data_department_v2()
    print("test_data_department_v2: PASS")