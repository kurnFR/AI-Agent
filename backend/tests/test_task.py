from app.execution.task import Task


def test_task_model():
    task = Task(
        id="task-001",
        description="Show current directory"
    )

    assert task.id == "task-001"
    assert task.description == "Show current directory"
    assert task.status == "pending"
    assert task.metadata == {}
    assert task.depends_on == []
    assert task.created_at is not None

    dependent_task = Task(
        id="task-002",
        description="List files",
        depends_on=["task-001"]
    )

    assert dependent_task.id == "task-002"
    assert dependent_task.description == "List files"
    assert dependent_task.status == "pending"
    assert dependent_task.metadata == {}
    assert dependent_task.depends_on == ["task-001"]
    assert dependent_task.created_at is not None

    multiple_dependencies = Task(
        id="task-003",
        description="Process results",
        depends_on=["task-001", "task-002"]
    )

    assert multiple_dependencies.depends_on == [
        "task-001",
        "task-002"
    ]


if __name__ == "__main__":
    test_task_model()
    print("test_task: PASS")