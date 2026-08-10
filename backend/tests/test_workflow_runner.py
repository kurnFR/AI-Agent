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


class FakeRegistry:

    def __init__(self):

        self.tool = FakeTool()

    def get(self, name):

        if name == self.tool.name:
            return self.tool

        return None


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

results = runner.execute(
    workflow,
    [plan1, plan2]
)


assert len(results) == 2

assert results[0].task_id == "task-001"
assert results[0].success is True
assert results[0].output == "executed: first"
assert results[0].error is None
assert results[0].metadata["tool"] == "fake"
assert results[0].metadata["action"] == "execute"


assert results[1].task_id == "task-002"
assert results[1].success is True
assert results[1].output == "executed: second"
assert results[1].error is None


print("=" * 60)
print("WORKFLOW RUNNER TEST")
print("=" * 60)

for result in results:
    print(result)

print("=" * 60)
print("WORKFLOW RUNNER TEST PASSED")
