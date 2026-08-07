from pydantic import BaseModel


class TaskPlan(BaseModel):

    tool: str

    action: str

    target: str = ""

    payload: dict = {}

    reason: str = ""