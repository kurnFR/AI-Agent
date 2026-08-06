import os

from app.tools.base.tool import BaseTool


class FileSystemTool(BaseTool):

    name = "filesystem"

    def execute(self, plan):

        if plan.action == "list":

            return os.listdir(plan.path)

        if plan.action == "read":

            with open(plan.path, "r") as f:
                return f.read()

        raise Exception(
            f"Unknown filesystem action '{plan.action}'."
        )