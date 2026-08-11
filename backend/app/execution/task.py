from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    description: str

    status: str = "pending"

    metadata: dict = Field(default_factory=dict)

    depends_on: list[str] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )