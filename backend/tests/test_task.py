from app.execution.task import Task


task = Task(
    id="task-001",
    description="Show current directory"
)

assert task.id == "task-001"
assert task.description == "Show current directory"
assert task.status == "pending"
assert task.metadata == {}
assert task.created_at is not None

print("=" * 60)
print("TASK MODEL TEST")
print("=" * 60)
print(task)
print("=" * 60)
print("TASK TEST PASSED")
