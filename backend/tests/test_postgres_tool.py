from sqlalchemy import create_engine
from app.schemas.task_plan import TaskPlan
from app.tools.postgres.tool import PostgresTool


def test_postgres_tool():
    # Use in-memory SQLite engine to test PostgresTool execution
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
        conn.exec_driver_sql("INSERT INTO users (id, name) VALUES (1, 'Alice');")

    tool = PostgresTool(engine=engine)

    # 1. Query rows
    plan = TaskPlan(
        tool="postgres",
        action="execute",
        target="SELECT * FROM users;",
        payload={},
        reason="Query test"
    )
    result = tool.execute(plan)
    assert result.success is True
    assert result.tool == "postgres"
    assert len(result.output) == 1
    assert result.output[0]["name"] == "Alice"

    # 2. Insert row
    insert_plan = TaskPlan(
        tool="postgres",
        action="execute",
        target="INSERT INTO users (id, name) VALUES (2, 'Bob');",
        payload={},
        reason="Insert test"
    )
    result_insert = tool.execute(insert_plan)
    assert result_insert.success is True
    assert "rows_affected" in result_insert.output
    assert result_insert.output["rows_affected"] == 1

    # 3. Invalid query
    err_plan = TaskPlan(
        tool="postgres",
        action="execute",
        target="SELECT * FROM nonexistent_table;",
        payload={},
        reason="Error test"
    )
    result_err = tool.execute(err_plan)
    assert result_err.success is False
    assert result_err.error is not None


if __name__ == "__main__":
    test_postgres_tool()
    print("test_postgres_tool: PASS")