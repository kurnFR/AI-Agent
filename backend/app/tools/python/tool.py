import subprocess
import tempfile
from pathlib import Path

from app.config import EXECUTION_TIMEOUT
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool


class PythonTool(BaseTool):

    name = "python"

    def execute(self, plan) -> ExecutionResult:

        code = ""
        if isinstance(plan.payload, dict) and "code" in plan.payload:
            code = str(plan.payload["code"]).strip()

        if not code and plan.target:
            code = plan.target.strip()

        if not code:

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="No Python code supplied."
            )

        try:
            with tempfile.TemporaryDirectory() as tmpdir:

                script = Path(tmpdir) / "script.py"

                script.write_text(code, encoding="utf-8")

                result = subprocess.run(
                    ["python3", str(script)],
                    capture_output=True,
                    text=True,
                    timeout=EXECUTION_TIMEOUT
                )

            return ExecutionResult(
                success=result.returncode == 0,
                tool=self.name,
                output=result.stdout,
                error=None if result.returncode == 0 else result.stderr
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=f"Python execution timed out after {EXECUTION_TIMEOUT}s."
            )
        except Exception as ex:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=str(ex)
            )