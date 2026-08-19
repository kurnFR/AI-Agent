from app.execution.task import Task
from app.execution.workflow import Workflow


def test_workflow():
    task1 = Task(
        id="task-001",
        description="Show current directory"
    )

    task2 = Task(
        id="task-002",
        description="List files",
        depends_on=["task-001"]
    )

    workflow = Workflow(
        id="workflow-001",
        name="Filesystem inspection",
        tasks=[task1, task2]
    )

    workflow.validate_dependencies()

    assert workflow.id == "workflow-001"
    assert workflow.name == "Filesystem inspection"
    assert workflow.status == "pending"

    assert len(workflow.tasks) == 2
    assert workflow.tasks[0].id == "task-001"
    assert workflow.tasks[0].description == "Show current directory"
    assert workflow.tasks[0].depends_on == []

    assert workflow.tasks[1].id == "task-002"
    assert workflow.tasks[1].description == "List files"
    assert workflow.tasks[1].depends_on == ["task-001"]

    assert workflow.created_at is not None

    # UNKNOWN DEPENDENCY
    unknown_dependency_task = Task(
        id="task-003",
        description="Invalid dependency",
        depends_on=["task-999"]
    )

    unknown_dependency_workflow = Workflow(
        id="workflow-002",
        name="Unknown dependency test",
        tasks=[unknown_dependency_task]
    )

    try:
        unknown_dependency_workflow.validate_dependencies()
        assert False, "Expected ValueError for unknown dependency"
    except ValueError as exc:
        assert "unknown task" in str(exc)

    # SELF DEPENDENCY
    self_dependency_task = Task(
        id="task-004",
        description="Self dependency",
        depends_on=["task-004"]
    )

    self_dependency_workflow = Workflow(
        id="workflow-003",
        name="Self dependency test",
        tasks=[self_dependency_task]
    )

    try:
        self_dependency_workflow.validate_dependencies()
        assert False, "Expected ValueError for self dependency"
    except ValueError as exc:
        assert "cannot depend on itself" in str(exc)

    # CIRCULAR DEPENDENCY
    cycle_task1 = Task(
        id="task-005",
        description="Cycle task 1",
        depends_on=["task-007"]
    )

    cycle_task2 = Task(
        id="task-006",
        description="Cycle task 2",
        depends_on=["task-005"]
    )

    cycle_task3 = Task(
        id="task-007",
        description="Cycle task 3",
        depends_on=["task-006"]
    )

    cycle_workflow = Workflow(
        id="workflow-004",
        name="Circular dependency test",
        tasks=[
            cycle_task1,
            cycle_task2,
            cycle_task3
        ]
    )

    try:
        cycle_workflow.validate_dependencies()
        assert False, "Expected ValueError for circular dependency"
    except ValueError as exc:
        assert "Circular dependency detected" in str(exc)


if __name__ == "__main__":
    test_workflow()
    print("test_workflow: PASS")