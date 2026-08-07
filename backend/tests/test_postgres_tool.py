from app.schemas.task_plan import TaskPlan
from app.tools.postgres.tool import PostgresTool


tool = PostgresTool()

plan = TaskPlan(
    tool="postgres",
    action="execute",
    target="SELECT 1 AS ok;",
    payload={},
    reason="Connectivity test"
)

result = tool.execute(plan)

print(result)