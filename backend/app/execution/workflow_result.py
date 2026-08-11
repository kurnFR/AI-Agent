from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.execution.task_result import TaskResult


class WorkflowResult(BaseModel):

    workflow_id: str

    success: bool

    results: list[TaskResult] = Field(default_factory=list)

    error: str | None = None

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
