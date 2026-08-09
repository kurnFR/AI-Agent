from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class TaskResult(BaseModel):

    task_id: str

    success: bool

    output: Any = None

    error: str | None = None

    metadata: dict = Field(default_factory=dict)

    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
