from app.execution.workflow import Workflow
from app.execution.workflow_lifecycle import WorkflowLifecycle


def test_workflow_lifecycle():
    lifecycle = WorkflowLifecycle()

    workflow = Workflow(
        id="workflow-001",
        name="Test workflow"
    )

    assert workflow.status == "pending"

    result = lifecycle.start(workflow)
    assert result is workflow
    assert workflow.status == "running"

    result = lifecycle.complete(workflow)
    assert result is workflow
    assert workflow.status == "completed"

    failed_workflow = Workflow(
        id="workflow-002",
        name="Failed workflow"
    )

    lifecycle.start(failed_workflow)
    result = lifecycle.fail(failed_workflow)
    assert result is failed_workflow
    assert failed_workflow.status == "failed"

    invalid_workflow = Workflow(
        id="workflow-003",
        name="Invalid workflow"
    )

    try:
        lifecycle.complete(invalid_workflow)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    completed_workflow = Workflow(
        id="workflow-004",
        name="Completed workflow"
    )

    lifecycle.start(completed_workflow)
    lifecycle.complete(completed_workflow)

    try:
        lifecycle.start(completed_workflow)
        assert False, "Expected ValueError"
    except ValueError:
        pass


if __name__ == "__main__":
    test_workflow_lifecycle()
    print("test_workflow_lifecycle: PASS")

