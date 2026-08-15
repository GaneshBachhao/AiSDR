from datetime import datetime

from ..value_objects.workflow_id import WorkflowId
from ..value_objects.step_id import StepId


class WorkflowStepCompleted:
    """
    Raised when an individual workflow step completes.
    """

    def __init__(
        self,
        workflow_id: WorkflowId,
        step_id: StepId
    ):
        self.workflow_id = workflow_id
        self.step_id = step_id
        self.occurred_at = datetime.utcnow()