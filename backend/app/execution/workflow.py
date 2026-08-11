from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from app.execution.task import Task


class Workflow(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    tasks: list[Task] = Field(default_factory=list)

    status: str = "pending"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def validate_dependencies(self) -> None:

        task_ids = {task.id for task in self.tasks}

        if len(task_ids) != len(self.tasks):
            raise ValueError(
                "Workflow contains duplicate task IDs."
            )

        for task in self.tasks:

            if task.id in task.depends_on:
                raise ValueError(
                    f"Task '{task.id}' cannot depend on itself."
                )

            for dependency_id in task.depends_on:

                if dependency_id not in task_ids:
                    raise ValueError(
                        f"Task '{task.id}' depends on unknown "
                        f"task '{dependency_id}'."
                    )

        self._validate_no_cycles()

    def _validate_no_cycles(self) -> None:

        task_map = {
            task.id: task
            for task in self.tasks
        }

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task_id: str) -> None:

            if task_id in visiting:
                raise ValueError(
                    f"Circular dependency detected involving "
                    f"task '{task_id}'."
                )

            if task_id in visited:
                return

            visiting.add(task_id)

            task = task_map[task_id]

            for dependency_id in task.depends_on:
                visit(dependency_id)

            visiting.remove(task_id)
            visited.add(task_id)

        for task in self.tasks:
            visit(task.id)