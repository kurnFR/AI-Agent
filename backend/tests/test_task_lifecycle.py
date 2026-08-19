
from app.execution.task import Task
from app.execution.task_lifecycle import TaskLifecycle


def test_task_lifecycle():
    lifecycle = TaskLifecycle()

    task = Task(
        id="task-001",
        description="Test task"
    )

    assert task.status == "pending"

    result = lifecycle.start(task)
    assert result is task
    assert task.status == "running"

    result = lifecycle.complete(task)
    assert result is task
    assert task.status == "completed"

    failed_task = Task(
        id="task-002",
        description="Failed task"
    )

    lifecycle.start(failed_task)
    result = lifecycle.fail(failed_task)
    assert result is failed_task
    assert failed_task.status == "failed"

    invalid_task = Task(
        id="task-003",
        description="Invalid transition"
    )

    try:
        lifecycle.complete(invalid_task)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    completed_task = Task(
        id="task-004",
        description="Completed task"
    )

    lifecycle.start(completed_task)
    lifecycle.complete(completed_task)

    try:
        lifecycle.start(completed_task)
        assert False, "Expected ValueError"
    except ValueError:
        pass


if __name__ == "__main__":
    test_task_lifecycle()
    print("test_task_lifecycle: PASS")