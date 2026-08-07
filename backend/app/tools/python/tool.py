import subprocess
import tempfile
from pathlib import Path

from app.execution.result import ExecutionResult


class PythonTool:

    name = "python"

    def execute(self, plan):

        code = plan.payload.get("code", "")

        if not code.strip():

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="No Python code supplied."
            )

        with tempfile.TemporaryDirectory() as tmpdir:

            script = Path(tmpdir) / "script.py"

            script.write_text(code)

            result = subprocess.run(
                ["python3", str(script)],
                capture_output=True,
                text=True
            )

        return ExecutionResult(
            success=result.returncode == 0,
            tool=self.name,
            output=result.stdout,
            error=None if result.returncode == 0 else result.stderr
        )