from pathlib import Path

from app.execution.result import ExecutionResult


class FileSystemTool:

    name = "filesystem"

    def execute(self, plan):

        path = Path(plan.target)

        if plan.action == "list":

            if not path.exists():
                return ExecutionResult(
                    success=False,
                    tool=self.name,
                    output=None,
                    error=f"{path} not found."
                )

            return ExecutionResult(
                success=True,
                tool=self.name,
                output=sorted(
                    p.name for p in path.iterdir()
                ),
                error=None
            )

        if plan.action == "read":

            if not path.exists():
                return ExecutionResult(
                    success=False,
                    tool=self.name,
                    output=None,
                    error=f"{path} not found."
                )

            return ExecutionResult(
                success=True,
                tool=self.name,
                output=path.read_text(),
                error=None
            )

        return ExecutionResult(
            success=False,
            tool=self.name,
            output=None,
            error=f"Unknown action '{plan.action}'."
        )