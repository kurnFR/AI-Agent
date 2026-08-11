from __future__ import annotations

from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.execution.task_lifecycle import TaskLifecycle
from app.execution.task_result import TaskResult
from app.execution.workflow import Workflow
from app.execution.workflow_lifecycle import WorkflowLifecycle
from app.execution.workflow_result import WorkflowResult
from app.schemas.task_plan import TaskPlan


class WorkflowRunner:

    def __init__(self, engine: ExecutionEngine):

        self.engine = engine
        self.task_lifecycle = TaskLifecycle()
        self.workflow_lifecycle = WorkflowLifecycle()

    def execute(
        self,
        workflow: Workflow,
        plans: list[TaskPlan]
    ) -> WorkflowResult:

        if len(workflow.tasks) != len(plans):
            raise ValueError(
                "Number of workflow tasks must match number of task plans."
            )

        self.workflow_lifecycle.start(workflow)

        results: list[TaskResult] = []

        try:

            for task, plan in zip(workflow.tasks, plans):

                self.task_lifecycle.start(task)

                try:

                    execution_result: ExecutionResult = (
                        self.engine.execute(plan)
                    )

                    if execution_result.success:
                        self.task_lifecycle.complete(task)
                    else:
                        self.task_lifecycle.fail(task)

                except Exception:

                    if task.status == TaskLifecycle.RUNNING:
                        self.task_lifecycle.fail(task)

                    raise

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

                if not execution_result.success:

                    self.workflow_lifecycle.fail(workflow)

                    return WorkflowResult(
                        workflow_id=workflow.id,
                        success=False,
                        results=results,
                        error=execution_result.error
                    )

            self.workflow_lifecycle.complete(workflow)

            return WorkflowResult(
                workflow_id=workflow.id,
                success=True,
                results=results,
                error=None
            )

        except Exception:

            if workflow.status == WorkflowLifecycle.RUNNING:
                self.workflow_lifecycle.fail(workflow)

            raise