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
# 1. SUCCESSFUL WORKFLOW WITH DEPENDENCY
# ==========================================================

task1 = Task(
    id="task-001",
    description="First task"
)

task2 = Task(
    id="task-002",
    description="Second task",
    depends_on=["task-001"]
)

workflow = Workflow(
    id="workflow-001",
    name="Successful dependent workflow",
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

assert workflow_result.results[1].task_id == "task-002"
assert workflow_result.results[1].success is True

assert task1.status == "completed"
assert task2.status == "completed"
assert workflow.status == "completed"


# ==========================================================
# 2. FAILED TASK + DEPENDENT TASK SKIPPED
# ==========================================================

failed_task = Task(
    id="task-003",
    description="Failing task"
)

dependent_task = Task(
    id="task-004",
    description="Depends on failed task",
    depends_on=["task-003"]
)

independent_task = Task(
    id="task-005",
    description="Independent after failure"
)

partial_workflow = Workflow(
    id="workflow-002",
    name="Partial failure workflow",
    tasks=[
        failed_task,
        dependent_task,
        independent_task
    ]
)

failed_plan = TaskPlan(
    tool="fake-failing",
    action="execute",
    target="failure"
)

dependent_plan = TaskPlan(
    tool="fake",
    action="execute",
    target="should-not-run"
)

independent_plan = TaskPlan(
    tool="fake",
    action="execute",
    target="independent"
)

partial_result = runner.execute(
    partial_workflow,
    [
        failed_plan,
        dependent_plan,
        independent_plan
    ]
)

assert partial_result.workflow_id == "workflow-002"
assert partial_result.success is False
assert partial_result.error == (
    "One or more tasks failed or were skipped."
)

assert len(partial_result.results) == 3


# Failed task
assert partial_result.results[0].task_id == "task-003"
assert partial_result.results[0].success is False
assert partial_result.results[0].error == "Execution failed: failure"

assert failed_task.status == "failed"


# Dependent task skipped
assert partial_result.results[1].task_id == "task-004"
assert partial_result.results[1].success is False
assert partial_result.results[1].output is None
assert "task-003" in partial_result.results[1].error
assert partial_result.results[1].metadata["status"] == "skipped"

# It never started
assert dependent_task.status == "pending"


# Independent task continues
assert partial_result.results[2].task_id == "task-005"
assert partial_result.results[2].success is True
assert partial_result.results[2].output == "executed: independent"

assert independent_task.status == "completed"

assert partial_workflow.status == "failed"


# ==========================================================
# 3. MULTIPLE DEPENDENCIES
# ==========================================================

task6 = Task(
    id="task-006",
    description="Dependency A"
)

task7 = Task(
    id="task-007",
    description="Dependency B"
)

task8 = Task(
    id="task-008",
    description="Depends on A and B",
    depends_on=["task-006", "task-007"]
)

multi_workflow = Workflow(
    id="workflow-003",
    name="Multiple dependency workflow",
    tasks=[task6, task7, task8]
)

multi_result = runner.execute(
    multi_workflow,
    [
        TaskPlan(
            tool="fake",
            action="execute",
            target="dependency-a"
        ),
        TaskPlan(
            tool="fake",
            action="execute",
            target="dependency-b"
        ),
        TaskPlan(
            tool="fake",
            action="execute",
            target="dependent"
        )
    ]
)

assert multi_result.success is True
assert len(multi_result.results) == 3

assert task6.status == "completed"
assert task7.status == "completed"
assert task8.status == "completed"


# ==========================================================
# 4. UNKNOWN DEPENDENCY
# ==========================================================

invalid_task = Task(
    id="task-009",
    description="Invalid dependency",
    depends_on=["does-not-exist"]
)

invalid_workflow = Workflow(
    id="workflow-004",
    name="Invalid dependency workflow",
    tasks=[invalid_task]
)

try:

    runner.execute(
        invalid_workflow,
        [
            TaskPlan(
                tool="fake",
                action="execute",
                target="invalid"
            )
        ]
    )

    raise AssertionError("Expected ValueError")

except ValueError as exc:

    assert "unknown task" in str(exc)


assert invalid_workflow.status == "pending"


# ==========================================================
# 5. SELF DEPENDENCY
# ==========================================================

self_task = Task(
    id="task-010",
    description="Self dependency",
    depends_on=["task-010"]
)

self_workflow = Workflow(
    id="workflow-005",
    name="Self dependency workflow",
    tasks=[self_task]
)

try:

    runner.execute(
        self_workflow,
        [
            TaskPlan(
                tool="fake",
                action="execute",
                target="self"
            )
        ]
    )

    raise AssertionError("Expected ValueError")

except ValueError as exc:

    assert "cannot depend on itself" in str(exc)


assert self_workflow.status == "pending"


# ==========================================================
# 6. CIRCULAR DEPENDENCY
# ==========================================================

cycle_task_a = Task(
    id="task-011",
    description="Cycle A",
    depends_on=["task-012"]
)

cycle_task_b = Task(
    id="task-012",
    description="Cycle B",
    depends_on=["task-011"]
)

cycle_workflow = Workflow(
    id="workflow-006",
    name="Circular dependency workflow",
    tasks=[
        cycle_task_a,
        cycle_task_b
    ]
)

try:

    runner.execute(
        cycle_workflow,
        [
            TaskPlan(
                tool="fake",
                action="execute",
                target="cycle-a"
            ),
            TaskPlan(
                tool="fake",
                action="execute",
                target="cycle-b"
            )
        ]
    )

    raise AssertionError("Expected ValueError")

except ValueError as exc:

    assert "Circular dependency detected" in str(exc)


assert cycle_workflow.status == "pending"


# ==========================================================
# 7. EMPTY WORKFLOW
# ==========================================================

empty_workflow = Workflow(
    id="workflow-007",
    name="Empty workflow",
    tasks=[]
)

try:

    runner.execute(
        empty_workflow,
        []
    )

    raise AssertionError("Expected ValueError")

except ValueError as exc:

    assert "at least one task" in str(exc)


assert empty_workflow.status == "pending"


# ==========================================================
# TEST OUTPUT
# ==========================================================

print("=" * 60)
print("WORKFLOW RUNNER DEPENDENCY TEST")
print("=" * 60)

print()
print("SUCCESSFUL WORKFLOW:")
print(workflow_result)

print()
print("PARTIAL FAILURE WORKFLOW:")
print(partial_result)

print()
print("MULTIPLE DEPENDENCY WORKFLOW:")
print(multi_result)

print()
print("TASK STATUS:")
print("TASK 001:", task1.status)
print("TASK 002:", task2.status)
print("TASK 003:", failed_task.status)
print("TASK 004:", dependent_task.status)
print("TASK 005:", independent_task.status)
print("TASK 006:", task6.status)
print("TASK 007:", task7.status)
print("TASK 008:", task8.status)

print()
print("WORKFLOW STATUS:")
print("WORKFLOW 001:", workflow.status)
print("WORKFLOW 002:", partial_workflow.status)
print("WORKFLOW 003:", multi_workflow.status)
print("WORKFLOW 004:", invalid_workflow.status)
print("WORKFLOW 005:", self_workflow.status)
print("WORKFLOW 006:", cycle_workflow.status)
print("WORKFLOW 007:", empty_workflow.status)

print()
print("WORKFLOW RUNNER DEPENDENCY TEST PASSED")
print("=" * 60)