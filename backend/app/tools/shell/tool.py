import shlex
import subprocess

from app.config import EXECUTION_TIMEOUT
from app.execution.result import ExecutionResult
from app.security.command_validator import CommandValidator
from app.tools.base.tool import BaseTool


class ShellTool(BaseTool):

    name = "shell"

    def __init__(self):

        self.validator = CommandValidator()

    def execute(self, plan) -> ExecutionResult:

        command = ""
        if isinstance(plan.payload, dict) and "command" in plan.payload:
            command = str(plan.payload["command"]).strip()

        if not command and plan.target:
            command = plan.target.strip()

        if not command:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="No command provided."
            )

        valid = self.validator.validate(command)

        if not valid:

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=f"Command is blocked or unsafe: {command}"
            )

        try:
            tokens = shlex.split(command)
            result = subprocess.run(
                tokens,
                shell=False,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
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
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=f"Command timed out after {EXECUTION_TIMEOUT}s."
            )
        except Exception as ex:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=str(ex)
            )