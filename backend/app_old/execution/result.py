from pydantic import BaseModel


class ExecutionResult(BaseModel):
    success: bool
    tool: str
    output: object = None
    error: str | None = None