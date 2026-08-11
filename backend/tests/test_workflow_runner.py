from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.execution.task import Task
from app.execution.workflow import Workflow
from app.execution.workflow_runner import WorkflowRunner
from app.schemas.task_plan import TaskPlan


class FakeTool:

    name = "fake"

    def execute(self, plan):

        return ExecutionResult(
            success=True,
            tool=self.name,
            output=f"executed: {plan.target}",
            error=None
        )


class FakeFailingTool:

    name = "fake-failing"

    def execute(self, plan):

        return ExecutionResult(
            success=False,
            tool=self.name,
            output=None,
            error=f"Execution failed: {plan.target}"
        )


class FakeRegistry:

    def __init__(self):

        self.tools = {
            "fake": FakeTool(),
            "fake-failing": FakeFailingTool()
        }

    def get(self, name):

        return self.tools.get(name)


engine = ExecutionEngine(FakeRegistry())
runner = WorkflowRunner(engine)


# ==========================================================
# 1. SUCCESSFUL WORKFLOW
# ==========================================================

task1 = Task(
    id="task-001",
    description="First task"
)

task2 = Task(
    id="task-002",
    description="Second task"
)

workflow = Workflow(
    id="workflow-001",
    name="Successful workflow",
    tasks=[task1, task2]
)

plan1 = TaskPlan(
    tool="fake",
    action="execute",
    target="first"
)

plan2 = TaskPlan(
    tool="fake",
    action="execute",
    target="second"
)

workflow_result = runner.execute(
    workflow,
    [plan1, plan2]
)

assert workflow_result.workflow_id == "workflow-001"
assert workflow_result.success is True
assert workflow_result.error is None

assert len(workflow_result.results) == 2

assert workflow_result.results[0].task_id == "task-001"
assert workflow_result.results[0].success is True
assert workflow_result.results[0].output == "executed: first"

assert workflow_result.results[1].task_id == "task-002"
assert workflow_result.results[1].success is True
assert workflow_result.results[1].output == "executed: second"

assert task1.status == "completed"
assert task2.status == "completed"
assert workflow.status == "completed"


# ==========================================================
# 2. INDEPENDENT TASK FAILURE
# ==========================================================

failed_task = Task(
    id="task-003",
    description="Failing task"
)

successful_task = Task(
    id="task-004",
    description="Task after failure"
)

partial_workflow = Workflow(
    id="workflow-002",
    name="Partial failure workflow",
    tasks=[
        failed_task,
        successful_task
    ]
)

failed_plan = TaskPlan(
    tool="fake-failing",
    action="execute",
    target="failure"
)

successful_plan = TaskPlan(
    tool="fake",
    action="execute",
    target="after-failure"
)

partial_result = runner.execute(
    partial_workflow,
    [
        failed_plan,
        successful_plan
    ]
)

assert partial_result.workflow_id == "workflow-002"

# The workflow contains a failure.
assert partial_result.success is False

# The failure should be reported.
assert partial_result.results[0].task_id == "task-003"
assert partial_result.results[0].success is False
assert partial_result.results[0].error == "Execution failed: failure"

assert failed_task.status == "failed"

# Independent task must still execute.
assert partial_result.results[1].task_id == "task-004"
assert partial_result.results[1].success is True
assert partial_result.results[1].output == "executed: after-failure"

assert successful_task.status == "completed"

# Workflow ultimately contains a failure.
assert partial_workflow.status == "failed"


# ==========================================================
# 3. TASK / PLAN COUNT MISMATCH
# ==========================================================

mismatch_task = Task(
    id="task-005",
    description="Mismatch task"
)

mismatch_workflow = Workflow(
    id="workflow-003",
    name="Mismatch workflow",
    tasks=[mismatch_task]
)

try:

    runner.execute(
        mismatch_workflow,
        []
    )

    raise AssertionError(
        "Expected ValueError for task/plan count mismatch"
    )

except ValueError as exc:

    assert str(exc) == (
        "Number of workflow tasks must match number of task plans."
    )


# ==========================================================
# 4. EMPTY WORKFLOW
# ==========================================================

empty_workflow = Workflow(
    id="workflow-004",
    name="Empty workflow",
    tasks=[]
)

try:

    runner.execute(
        empty_workflow,
        []
    )

    raise AssertionError(
        "Expected ValueError for empty workflow"
    )

except ValueError as exc:

    assert str(exc) == "Workflow must contain at least one task."


# ==========================================================
# OUTPUT
# ==========================================================

print("=" * 60)
print("WORKFLOW RUNNER EDGE CASE TEST")
print("=" * 60)

print()
print("SUCCESSFUL WORKFLOW:")
print(workflow_result)

print()
print("PARTIAL FAILURE WORKFLOW:")
print(partial_result)

print()
print("SUCCESS WORKFLOW STATUS:", workflow.status)
print("PARTIAL WORKFLOW STATUS:", partial_workflow.status)

print()
print("TASK 001 STATUS:", task1.status)
print("TASK 002 STATUS:", task2.status)
print("TASK 003 STATUS:", failed_task.status)
print("TASK 004 STATUS:", successful_task.status)

print()
print("=" * 60)
print("WORKFLOW RUNNER EDGE CASE TEST PASSED")
print("=" * 60)