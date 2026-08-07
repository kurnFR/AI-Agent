from sqlalchemy import create_engine
from sqlalchemy import text

from app.execution.result import ExecutionResult
from app.tools.base.tool import BaseTool


class PostgresTool(BaseTool):

    name = "postgres"

    def __init__(self, connection_string: str):

        self.engine = create_engine(
            connection_string,
            pool_pre_ping=True
        )

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