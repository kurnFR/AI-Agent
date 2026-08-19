import os
from pathlib import Path
from typing import Optional

from app.config import WORKSPACE_ROOT
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool


class FileSystemTool(BaseTool):

    name = "filesystem"

    def __init__(self, workspace_root: Optional[str] = None):

        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT).resolve()

    def _resolve_path(self, raw_path: str) -> Path:

        p = Path(raw_path)
        if not p.is_absolute():
            return (self.workspace_root / p).resolve()
        return p.resolve()

    def execute(self, plan) -> ExecutionResult:

        raw_path = ""
        if isinstance(plan.payload, dict) and "path" in plan.payload:
            raw_path = str(plan.payload["path"]).strip()

        if not raw_path and plan.target:
            raw_path = plan.target.strip()

        if not raw_path:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="No path supplied in target or payload."
            )

        path = self._resolve_path(raw_path)
        action = plan.action.lower() if plan.action else "list"

        try:
            if action in ("list", "ls"):

                if not path.exists():
                    return ExecutionResult(
                        success=False,
                        tool=self.name,
                        output=None,
                        error=f"{path} not found."
                    )

                if not path.is_dir():
                    return ExecutionResult(
                        success=False,
                        tool=self.name,
                        output=None,
                        error=f"{path} is not a directory."
                    )

                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=sorted(p.name for p in path.iterdir()),
                    error=None
                )

            elif action in ("read", "cat"):

                if not path.exists():
                    return ExecutionResult(
                        success=False,
                        tool=self.name,
                        output=None,
                        error=f"{path} not found."
                    )

                if not path.is_file():
                    return ExecutionResult(
                        success=False,
                        tool=self.name,
                        output=None,
                        error=f"{path} is not a file."
                    )

                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=path.read_text(encoding="utf-8", errors="replace"),
                    error=None
                )

            elif action in ("write", "create"):

                content = ""
                if isinstance(plan.payload, dict):
                    content = plan.payload.get("content", "")

                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=f"Successfully wrote {len(content)} bytes to {path}.",
                    error=None
                )

            elif action in ("mkdir", "make_dir"):

                path.mkdir(parents=True, exist_ok=True)
                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=f"Directory created: {path}",
                    error=None
                )

            elif action in ("delete", "remove", "rm"):

                if not path.exists():
                    return ExecutionResult(
                        success=False,
                        tool=self.name,
                        output=None,
                        error=f"{path} not found."
                    )

                if path.is_file() or path.is_symlink():
                    path.unlink()
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)

                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=f"Removed {path}",
                    error=None
                )

            elif action in ("exists", "check"):

                return ExecutionResult(
                    success=True,
                    tool=self.name,
                    output=path.exists(),
                    error=None
                )

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=f"Unknown action '{plan.action}'."
            )

        except Exception as ex:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=str(ex)
            )