
from app.execution.task import Task


class TaskLifecycle:

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    def start(self, task: Task) -> Task:

        if task.status != self.PENDING:
            raise ValueError(
                f"Cannot start task '{task.id}' from status '{task.status}'."
            )

        task.status = self.RUNNING

        return task

    def complete(self, task: Task) -> Task:

        if task.status != self.RUNNING:
            raise ValueError(
                f"Cannot complete task '{task.id}' from status '{task.status}'."
            )

        task.status = self.COMPLETED

        return task

    def fail(self, task: Task) -> Task:

        if task.status != self.RUNNING:
            raise ValueError(
                f"Cannot fail task '{task.id}' from status '{task.status}'."
            )

        task.status = self.FAILED

        return task