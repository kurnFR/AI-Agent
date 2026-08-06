import io
from contextlib import redirect_stdout

from app.tools.base.tool import BaseTool


class PythonTool(BaseTool):

    name = "python"

    def execute(self, plan):

        buffer = io.StringIO()

        with redirect_stdout(buffer):

            exec(plan.command, {})

        return buffer.getvalue()