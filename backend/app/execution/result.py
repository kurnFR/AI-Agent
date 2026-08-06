from typing import Any
from typing import Optional

from pydantic import BaseModel


class ExecutionResult(BaseModel):

    success: bool

    tool: str

    output: Optional[Any] = None

    error: Optional[str] = None
