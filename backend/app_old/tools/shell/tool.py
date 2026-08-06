import subprocess

from app.security.command_validator import CommandValidator
from app.tools.base.tool import BaseTool


class ShellTool(BaseTool):

    name = "shell"

    def __init__(self):

        self.validator = CommandValidator()

    def execute(self, plan):

        command = plan.command

        valid = self.validator.validate(command)

        if isinstance(valid, dict):

            if not valid["success"]:
                raise Exception(valid["error"])

        elif valid is False:

            raise Exception("Command not allowed.")

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