from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.execution.task_result import TaskResult
from app.execution.workflow import Workflow
from app.schemas.task_plan import TaskPlan


class WorkflowRunner:

    def __init__(self, engine: ExecutionEngine):

        self.engine = engine

    def execute(
        self,
        workflow: Workflow,
        plans: list[TaskPlan]
    ) -> list[TaskResult]:

        if len(workflow.tasks) != len(plans):

            raise ValueError(
                "Number of workflow tasks must match number of task plans."
            )

        results = []

        for task, plan in zip(workflow.tasks, plans):

            execution_result: ExecutionResult = self.engine.execute(plan)

            result = TaskResult(
                task_id=task.id,
                success=execution_result.success,
                output=execution_result.output,
                error=execution_result.error,
                metadata={
                    "tool": execution_result.tool,
                    "action": plan.action
                }
            )

            results.append(result)

        return results
