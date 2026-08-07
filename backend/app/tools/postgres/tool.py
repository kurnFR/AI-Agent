from sqlalchemy import text

import app.settings
import os

from app.database.factory import manager
from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool


class PostgresTool(BaseTool):

    name = "postgres"

    def __init__(self):

        self.engine = manager.engine("postgres")

    def execute(self, plan):

        sql = plan.target.strip()

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