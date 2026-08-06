import subprocess

from app.schemas.task_plan import TaskPlan
from app.security.command_validator import CommandValidator
from app.tools.base.tool import BaseTool


class ShellTool(BaseTool):

    name = "shell"

    def __init__(self):

        self.validator = CommandValidator()

    def execute(self, plan: TaskPlan):

        command = plan.command

        if not self.validator.validate(command):
            raise Exception("Command is not allowed.")

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
