from app.domain.shared.base import DomainEvent

from ..value_objects.workflow_id import WorkflowId


class WorkflowStarted(DomainEvent):
    """
    Raised when workflow execution starts.
    """

    def __init__(self, workflow_id: WorkflowId):
        super().__init__()
        self.workflow_id = workflow_id