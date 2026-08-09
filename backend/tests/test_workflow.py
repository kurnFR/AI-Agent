from app.execution.task import Task
from app.execution.workflow import Workflow


task1 = Task(
    id="task-001",
    description="Show current directory"
)

task2 = Task(
    id="task-002",
    description="List files"
)

workflow = Workflow(
    id="workflow-001",
    name="Filesystem inspection",
    tasks=[task1, task2]
)

assert workflow.id == "workflow-001"
assert workflow.name == "Filesystem inspection"
assert workflow.status == "pending"

assert len(workflow.tasks) == 2

assert workflow.tasks[0].id == "task-001"
assert workflow.tasks[0].description == "Show current directory"

assert workflow.tasks[1].id == "task-002"
assert workflow.tasks[1].description == "List files"

assert workflow.created_at is not None


print("=" * 60)
print("WORKFLOW TEST")
print("=" * 60)
print("WORKFLOW:")
print(workflow)
print()
print("TASK COUNT:", len(workflow.tasks))
print("=" * 60)
print("WORKFLOW TEST PASSED")
