from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.schemas.execution_plan import ExecutionPlan
from app.tools.base.tool import BaseTool
from app.tools.registry import ToolRegistry


class MockTool(BaseTool):
    name = "mock"

    def execute(self, plan):
        if plan.target == "error":
            raise RuntimeError("Tool execution failed")
        return ExecutionResult(
            success=True,
            tool=self.name,
            output={"result": "ok"},
            error=None
        )


def test_execution_engine():
    registry = ToolRegistry()
    registry.register(MockTool())

    engine = ExecutionEngine(registry)

    # 1. Success execution
    plan = ExecutionPlan(
        tool="mock",
        action="run",
        target="success",
        payload={}
    )
    res = engine.execute(plan)
    assert res.success is True
    assert res.tool == "mock"
    assert res.output == {"result": "ok"}
    assert res.error is None

    # 2. Unknown tool
    unknown_plan = ExecutionPlan(
        tool="nonexistent",
        action="run",
        target="test"
    )
    res_unknown = engine.execute(unknown_plan)
    assert res_unknown.success is False
    assert "not found" in res_unknown.error

    # 3. Exception in tool
    err_plan = ExecutionPlan(
        tool="mock",
        action="run",
        target="error"
    )
    res_err = engine.execute(err_plan)
    assert res_err.success is False
    assert "Tool execution failed" in res_err.error


if __name__ == "__main__":
    test_execution_engine()
    print("test_execution_engine: PASS")

