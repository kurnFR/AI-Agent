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
