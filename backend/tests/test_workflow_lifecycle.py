from app.execution.workflow import Workflow
from app.execution.workflow_lifecycle import WorkflowLifecycle


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
    raise AssertionError("Expected ValueError")
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
    raise AssertionError("Expected ValueError")
except ValueError:
    pass


print("=" * 60)
print("WORKFLOW LIFECYCLE TEST")
print("=" * 60)

print("WORKFLOW 001:", workflow.status)
print("WORKFLOW 002:", failed_workflow.status)
print("WORKFLOW 004:", completed_workflow.status)

print("=" * 60)
print("WORKFLOW LIFECYCLE TEST PASSED")
