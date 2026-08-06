from pathlib import Path

from app.schemas.task_plan import TaskPlan
from app.tools.base.tool import BaseTool


class FileSystemTool(BaseTool):

    name = "filesystem"

    def execute(self, plan: TaskPlan):

        action = plan.action
        path = Path(plan.path)

        if action == "list":

            return sorted(
                x.name
                for x in path.iterdir()
            )

        if action == "read":

            return path.read_text()

        raise Exception(f"Unknown filesystem action '{action}'.")
