import contextlib
import io

from app.schemas.task_plan import TaskPlan
from app.tools.base.tool import BaseTool


class PythonTool(BaseTool):

    name = "python"

    def execute(self, plan: TaskPlan):

        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):

            exec(plan.code, {})

        return buffer.getvalue()
