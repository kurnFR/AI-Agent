from typing import Any
from typing import Optional

from pydantic import BaseModel


class TaskPlan(BaseModel):

    tool: str

    action: Optional[str] = None

    command: Optional[str] = None

    path: Optional[str] = None

    query: Optional[str] = None

    code: Optional[str] = None

    arguments: dict[str, Any] = {}
