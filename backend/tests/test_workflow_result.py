from app.execution.task_result import TaskResult
from app.execution.workflow_result import WorkflowResult


success_task = TaskResult(
    task_id="task-001",
    success=True,
    output="hello"
)

failed_task = TaskResult(
    task_id="task-002",
    success=False,
    error="Something went wrong"
)


success_result = WorkflowResult(
    workflow_id="workflow-001",
    success=True,
    results=[success_task]
)

assert success_result.workflow_id == "workflow-001"
assert success_result.success is True
assert len(success_result.results) == 1
assert success_result.results[0].task_id == "task-001"
assert success_result.results[0].success is True
assert success_result.error is None
assert success_result.completed_at is not None


failed_result = WorkflowResult(
    workflow_id="workflow-002",
    success=False,
    results=[failed_task],
    error="Workflow execution failed"
)

assert failed_result.workflow_id == "workflow-002"
assert failed_result.success is False
assert len(failed_result.results) == 1
assert failed_result.results[0].task_id == "task-002"
assert failed_result.results[0].success is False
assert failed_result.results[0].error == "Something went wrong"
assert failed_result.error == "Workflow execution failed"
assert failed_result.completed_at is not None


empty_result_1 = WorkflowResult(
    workflow_id="workflow-003",
    success=True
)

empty_result_2 = WorkflowResult(
    workflow_id="workflow-004",
    success=True
)

empty_result_1.results.append(success_task)

assert len(empty_result_1.results) == 1
assert len(empty_result_2.results) == 0



print("=" * 60)
print("WORKFLOW RESULT TEST")
print("=" * 60)

print("SUCCESS RESULT:")
print(success_result)

print()

print("FAILED RESULT:")
print(failed_result)

print("=" * 60)
print("WORKFLOW RESULT TEST PASSED")
