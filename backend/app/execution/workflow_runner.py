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

        if not workflow.tasks:
            raise ValueError(
                "Workflow must contain at least one task."
            )

        workflow.validate_dependencies()

        self.workflow_lifecycle.start(workflow)
        results: list[TaskResult] = []

        # Maps task_id -> TaskResult.
        #
        # This is used to determine whether dependencies completed
        # successfully before allowing a dependent task to execute.
        task_results: dict[str, TaskResult] = {}

        has_failure = False

        try:

            for task, plan in zip(workflow.tasks, plans):

                # ======================================================
                # CHECK TASK DEPENDENCIES
                # ======================================================

                failed_dependencies = [
                    dependency_id
                    for dependency_id in task.depends_on
                    if (
                        dependency_id not in task_results
                        or not task_results[dependency_id].success
                    )
                ]

                if failed_dependencies:

                    has_failure = True

                    dependency_message = (
                        "Task skipped because dependency task(s) "
                        "failed or were skipped: "
                        + ", ".join(failed_dependencies)
                        + "."
                    )

                    skipped_result = TaskResult(
                        task_id=task.id,
                        success=False,
                        output=None,
                        error=dependency_message,
                        metadata={
                            "status": "skipped",
                            "dependencies": list(task.depends_on),
                            "failed_dependencies": failed_dependencies,
                            "tool": plan.tool,
                            "action": plan.action,
                        },
                    )

                    results.append(skipped_result)
                    task_results[task.id] = skipped_result

                    # The task never started.
                    #
                    # Therefore its Task.status intentionally remains
                    # "pending".
                    continue

                # ======================================================
                # START TASK
                # ======================================================

                self.task_lifecycle.start(task)

                try:

                    execution_result: ExecutionResult = (
                        self.engine.execute(plan)
                    )

                except Exception:

                    if task.status == TaskLifecycle.RUNNING:
                        self.task_lifecycle.fail(task)

                    raise

                # ======================================================
                # UPDATE TASK LIFECYCLE
                # ======================================================

                if execution_result.success:

                    self.task_lifecycle.complete(task)

                else:

                    self.task_lifecycle.fail(task)
                    has_failure = True

                # ======================================================
                # BUILD TASK RESULT
                # ======================================================

                task_result = TaskResult(
                    task_id=task.id,
                    success=execution_result.success,
                    output=execution_result.output,
                    error=execution_result.error,
                    metadata={
                        "status": (
                            "completed"
                            if execution_result.success
                            else "failed"
                        ),
                        "tool": execution_result.tool,
                        "action": plan.action,
                    },
                )

                results.append(task_result)
                task_results[task.id] = task_result

            # ==========================================================
            # FINISH WORKFLOW
            # ==========================================================

            if has_failure:

                self.workflow_lifecycle.fail(workflow)

                return WorkflowResult(
                    workflow_id=workflow.id,
                    success=False,
                    results=results,
                    error="One or more tasks failed or were skipped.",
                )

            self.workflow_lifecycle.complete(workflow)

            return WorkflowResult(
                workflow_id=workflow.id,
                success=True,
                results=results,
                error=None,
            )

        except Exception:

            if workflow.status == WorkflowLifecycle.RUNNING:
                self.workflow_lifecycle.fail(workflow)

            raise