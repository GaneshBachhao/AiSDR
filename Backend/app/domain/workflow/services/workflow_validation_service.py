from ..aggregate.workflow import Workflow
from ..enums.workflow_status import WorkflowStatus
from ..exceptions.workflow_exception import WorkflowException


class WorkflowValidationService:
    """
    Domain service responsible for workflow validation.
    """

    def validate_can_prepare(self, workflow: Workflow) -> None:
        """
        Validate workflow preparation.
        """

        if not workflow.has_steps():
            raise WorkflowException("Workflow requires at least one step")

    def validate_can_start(self, workflow: Workflow) -> None:
        """
        Validate workflow execution start.
        """

        if workflow.status != WorkflowStatus.READY:
            raise WorkflowException("Workflow is not ready for execution")

    def validate_completion(self, workflow: Workflow) -> None:
        """
        Validate workflow completion.
        """

        incomplete_steps = [step for step in workflow.steps if not step.is_completed]

        if incomplete_steps:
            raise WorkflowException("All steps must be completed before workflow completion")
