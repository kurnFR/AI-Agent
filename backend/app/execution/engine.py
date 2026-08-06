from app.execution.result import ExecutionResult


class ExecutionEngine:

    def __init__(self, registry):

        self.registry = registry

    def execute(self, plan):

        tool = self.registry.get(plan.tool)

        if tool is None:

            return ExecutionResult(
                success=False,
                tool=plan.tool,
                error=f"Tool '{plan.tool}' not found."
            )

        try:

            output = tool.execute(plan)

            return ExecutionResult(
                success=True,
                tool=plan.tool,
                output=output
            )

        except Exception as ex:

            return ExecutionResult(
                success=False,
                tool=plan.tool,
                error=str(ex)
            )
