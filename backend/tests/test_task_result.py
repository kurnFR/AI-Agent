from app.execution.task_result import TaskResult


def test_task_result():
    success_result = TaskResult(
        task_id="task-001",
        success=True,
        output="hello world"
    )

    assert success_result.task_id == "task-001"
    assert success_result.success is True
    assert success_result.output == "hello world"
    assert success_result.error is None
    assert success_result.metadata == {}
    assert success_result.completed_at is not None

    failed_result = TaskResult(
        task_id="task-002",
        success=False,
        error="Something went wrong"
    )

    assert failed_result.task_id == "task-002"
    assert failed_result.success is False
    assert failed_result.output is None
    assert failed_result.error == "Something went wrong"


if __name__ == "__main__":
    test_task_result()
    print("test_task_result: PASS")

