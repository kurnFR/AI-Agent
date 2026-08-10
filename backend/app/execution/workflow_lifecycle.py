from app.execution.workflow import Workflow


class WorkflowLifecycle:

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

    def start(self, workflow: Workflow) -> Workflow:

        if workflow.status != self.PENDING:
            raise ValueError(
                f"Cannot start workflow '{workflow.id}' "
                f"from status '{workflow.status}'."
            )

        workflow.status = self.RUNNING

        return workflow

    def complete(self, workflow: Workflow) -> Workflow:

        if workflow.status != self.RUNNING:
            raise ValueError(
                f"Cannot complete workflow '{workflow.id}' "
                f"from status '{workflow.status}'."
            )

        workflow.status = self.COMPLETED

        return workflow

    def fail(self, workflow: Workflow) -> Workflow:

        if workflow.status != self.RUNNING:
            raise ValueError(
                f"Cannot fail workflow '{workflow.id}' "
                f"from status '{workflow.status}'."
            )

        workflow.status = self.FAILED

        return workflow
