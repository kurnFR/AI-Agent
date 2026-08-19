from typing import Any, Optional
from sqlalchemy import text, create_engine

import os
from app.config import DATABASE_URL
from app.database.factory import manager
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool


class PostgresTool(BaseTool):

    name = "postgres"

    def __init__(self, database_url: Optional[str] = None, engine: Optional[Any] = None):

        if engine is not None:
            self.engine = engine
        elif database_url:
            self.engine = create_engine(database_url, pool_pre_ping=True)
        else:
            try:
                self.engine = manager.engine("postgres")
            except Exception:
                self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    def execute(self, plan) -> ExecutionResult:

        sql = ""
        if isinstance(plan.payload, dict) and "sql" in plan.payload:
            sql = str(plan.payload["sql"]).strip()

        if not sql and plan.target and plan.target.strip().lower() != "default":
            sql = plan.target.strip()

        if not sql:
            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error="No SQL query provided in target or payload."
            )

        try:

            with self.engine.begin() as conn:

                rows = conn.execute(
                    text(sql)
                )

                if rows.returns_rows:

                    result = [
                        dict(row._mapping)
                        for row in rows
                    ]

                else:

                    result = {
                        "rows_affected": rows.rowcount
                    }

            return ExecutionResult(
                success=True,
                tool=self.name,
                output=result,
                error=None
            )

        except Exception as ex:

            return ExecutionResult(
                success=False,
                tool=self.name,
                output=None,
                error=str(ex)
            )