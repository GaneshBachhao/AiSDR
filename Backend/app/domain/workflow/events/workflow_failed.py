from datetime import datetime

from ..value_objects.workflow_id import WorkflowId


class WorkflowFailed:
    """
    Raised when workflow execution fails.
    """

    def __init__(self, workflow_id: WorkflowId, reason: str):
        self.workflow_id = workflow_id
        self.reason = reason
        self.occurred_at = datetime.utcnow()
