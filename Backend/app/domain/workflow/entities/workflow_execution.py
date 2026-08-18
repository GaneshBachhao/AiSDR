from datetime import datetime
from uuid import uuid4

from ..enums.execution_status import ExecutionStatus
from ..exceptions.workflow_exception import WorkflowException
from ..value_objects.execution_id import ExecutionId


class WorkflowExecution:
    """
    Entity representing a workflow execution instance.

    Tracks runtime execution lifecycle.
    """

    def __init__(
        self,
        execution_id: ExecutionId | None = None,
    ):
        self._id = execution_id or ExecutionId(uuid4())

        self._status = ExecutionStatus.CREATED

        self._started_at: datetime | None = None
        self._completed_at: datetime | None = None

        self._failure_reason: str | None = None

    # ----------------------------
    # Properties
    # ----------------------------

    @property
    def id(self) -> ExecutionId:
        return self._id

    @property
    def status(self) -> ExecutionStatus:
        return self._status

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    @property
    def failure_reason(self) -> str | None:
        return self._failure_reason

    # ----------------------------
    # Lifecycle
    # ----------------------------

    def start(self) -> None:
        """
        Start execution.
        """

        if self._status != ExecutionStatus.CREATED:
            raise WorkflowException("Only created executions can start")

        self._status = ExecutionStatus.RUNNING
        self._started_at = datetime.utcnow()

    def complete(self) -> None:
        """
        Complete execution.
        """

        if self._status != ExecutionStatus.RUNNING:
            raise WorkflowException("Only running executions can complete")

        self._status = ExecutionStatus.COMPLETED
        self._completed_at = datetime.utcnow()

    def fail(self, reason: str) -> None:
        """
        Fail execution.
        """

        if self._status != ExecutionStatus.RUNNING:
            raise WorkflowException("Only running executions can fail")

        if not reason:
            raise WorkflowException("Failure reason is required")

        self._status = ExecutionStatus.FAILED
        self._failure_reason = reason

    def cancel(self) -> None:
        """
        Cancel execution.
        """

        if self._status == ExecutionStatus.COMPLETED:
            raise WorkflowException("Completed execution cannot be cancelled")

        self._status = ExecutionStatus.CANCELLED
