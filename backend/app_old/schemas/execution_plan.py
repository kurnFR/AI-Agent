from pydantic import BaseModel


class ExecutionPlan(BaseModel):

    tool: str

    action: str

    arguments: dict

    reason: str | None = None
