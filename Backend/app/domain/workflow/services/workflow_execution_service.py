from ..aggregate.workflow import Workflow
from ..entities.workflow_execution import WorkflowExecution
from ..exceptions.workflow_exception import WorkflowException


class WorkflowExecutionService:
    """
    Coordinates workflow execution lifecycle.
    """

    def __init__(self, validation_service):
        self.validation_service = validation_service

    def prepare(self, workflow: Workflow) -> None:
        """
        Prepare workflow for execution.
        """

        self.validation_service.validate_can_prepare(workflow)

        workflow.prepare()

    def start(self, workflow: Workflow) -> WorkflowExecution:
        """
        Start workflow execution.
        """

        self.validation_service.validate_can_start(workflow)

        workflow.start()

        execution = WorkflowExecution()

        execution.start()

        return execution

    def complete(self, workflow: Workflow, execution: WorkflowExecution) -> None:
        """
        Complete workflow execution.
        """

        self.validation_service.validate_completion(workflow)

        workflow.complete()

        execution.complete()

    def fail(self, workflow: Workflow, execution: WorkflowExecution, reason: str) -> None:
        """
        Handle workflow failure.
        """

        if not reason:
            raise WorkflowException("Failure reason required")

        workflow.fail()

        execution.fail(reason)
