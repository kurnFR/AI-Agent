import subprocess

from app.execution.result import ExecutionResult
from app.security.command_validator import CommandValidator


class ShellTool:

    name = "shell"

    def __init__(self):

        self.validator = CommandValidator()

    def execute(self, plan):

        command = plan.target

        valid = self.validator.validate(command)

        if not valid:

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="Command is blocked."
            )

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return ExecutionResult(
            success=result.returncode == 0,
            tool=self.name,
            output={
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            },
            error=None if result.returncode == 0 else result.stderr
        )