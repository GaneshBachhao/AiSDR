from datetime import datetime

from ..value_objects.workflow_id import WorkflowId


class WorkflowCreated:
    """
    Raised when a new workflow is created.
    """

    def __init__(
        self,
        workflow_id: WorkflowId
    ):
        self.workflow_id = workflow_id
        self.occurred_at = datetime.utcnow()