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
                output=None,
                error=f"Tool '{plan.tool}' not found."
            )

        try:

            return tool.execute(plan)

        except Exception as ex:

            return ExecutionResult(
                success=False,
                tool=plan.tool,
                output=None,
                error=str(ex)
            )