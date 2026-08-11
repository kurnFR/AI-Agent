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
            error="Fake execution failed"
        )


class FakeRegistry:

    def __init__(self):

        self.tools = {
            "fake": FakeTool(),
            "fake-failing": FakeFailingTool()
        }

    def get(self, name):

        return self.tools.get(name)


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
    name="Test workflow",
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


engine = ExecutionEngine(FakeRegistry())

runner = WorkflowRunner(engine)


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
assert workflow_result.results[0].error is None
assert workflow_result.results[0].metadata["tool"] == "fake"
assert workflow_result.results[0].metadata["action"] == "execute"

assert task1.status == "completed"


assert workflow_result.results[1].task_id == "task-002"
assert workflow_result.results[1].success is True
assert workflow_result.results[1].output == "executed: second"
assert workflow_result.results[1].error is None
assert workflow_result.results[1].metadata["tool"] == "fake"
assert workflow_result.results[1].metadata["action"] == "execute"

assert task2.status == "completed"

assert workflow.status == "completed"


failed_task = Task(
    id="task-003",
    description="Failing task"
)

failed_workflow = Workflow(
    id="workflow-002",
    name="Failing workflow",
    tasks=[failed_task]
)

failed_plan = TaskPlan(
    tool="fake-failing",
    action="execute",
    target="failure"
)


failed_result = runner.execute(
    failed_workflow,
    [failed_plan]
)


assert failed_result.workflow_id == "workflow-002"
assert failed_result.success is False
assert failed_result.error == "Fake execution failed"

assert len(failed_result.results) == 1

assert failed_result.results[0].task_id == "task-003"
assert failed_result.results[0].success is False
assert failed_result.results[0].output is None
assert failed_result.results[0].error == "Fake execution failed"
assert failed_result.results[0].metadata["tool"] == "fake-failing"
assert failed_result.results[0].metadata["action"] == "execute"

assert failed_workflow.status == "failed"
assert failed_task.status == "failed"


print("=" * 60)
print("WORKFLOW RUNNER TEST")
print("=" * 60)

print()
print("SUCCESS WORKFLOW RESULT:")
print(workflow_result)

print()
print("SUCCESS WORKFLOW STATUS:", workflow.status)

print()
print("FAILED WORKFLOW RESULT:")
print(failed_result)

print()
print("FAILED WORKFLOW STATUS:", failed_workflow.status)

print()
print("TASK 001 STATUS:", task1.status)
print("TASK 002 STATUS:", task2.status)
print("TASK 003 STATUS:", failed_task.status)

print("=" * 60)
print("WORKFLOW RUNNER TEST PASSED")