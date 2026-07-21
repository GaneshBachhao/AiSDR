from domain.shared.base import DomainEvent

from ..value_objects.workflow_id import WorkflowId


class WorkflowCompleted(DomainEvent):
    """
    Raised when workflow execution completes.
    """

    def __init__(self, workflow_id: WorkflowId):
        super().__init__()
        self.workflow_id = workflow_id