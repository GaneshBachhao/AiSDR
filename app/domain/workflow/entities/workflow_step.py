from datetime import UTC, datetime
from typing import Optional
from uuid import uuid4

from domain.shared.base import Entity

from ..enums.step_status import StepStatus
from ..exceptions.workflow_step_exception import WorkflowStepException
from ..value_objects.step_id import StepId
from ..value_objects.workflow_name import WorkflowName


class WorkflowStep(Entity[StepId]):
    """
    Entity representing a workflow execution step.

    Controlled by Workflow aggregate.
    """

    def __init__(
        self,
        name: WorkflowName,
        step_id: Optional[StepId] = None,
    ):
        step_id = step_id or StepId(uuid4())

        super().__init__(step_id)

        self._name = name

        self._status = StepStatus.PENDING

        self._created_at = datetime.now(UTC)

        self._started_at: Optional[datetime] = None
        self._completed_at: Optional[datetime] = None

        self._error_message: Optional[str] = None

    # ----------------------------
    # Properties
    # ----------------------------

    @property
    def name(self) -> WorkflowName:
        return self._name

    @property
    def status(self) -> StepStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def started_at(self) -> Optional[datetime]:
        return self._started_at

    @property
    def completed_at(self) -> Optional[datetime]:
        return self._completed_at

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message

    @property
    def is_completed(self) -> bool:
        return self._status == StepStatus.COMPLETED

    # ----------------------------
    # Lifecycle
    # ----------------------------

    def mark_ready(self) -> None:
        """
        Move step into executable state.
        """

        if self._status != StepStatus.PENDING:
            raise WorkflowStepException(
                "Only pending steps can become ready"
            )

        self._status = StepStatus.READY

    def start(self) -> None:
        """
        Begin execution.
        """

        if self._status != StepStatus.READY:
            raise WorkflowStepException(
                "Step must be ready before execution"
            )

        self._status = StepStatus.RUNNING
        self._started_at = datetime.now(UTC)

    def complete(self) -> None:
        """
        Mark step completed.
        """

        if self._status != StepStatus.RUNNING:
            raise WorkflowStepException(
                "Only running steps can complete"
            )

        self._status = StepStatus.COMPLETED
        self._completed_at = datetime.now(UTC)

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Mark step failed.
        """

        if self._status not in (
            StepStatus.RUNNING,
            StepStatus.READY,
        ):
            raise WorkflowStepException(
                "Step cannot fail from current state"
            )

        self._status = StepStatus.FAILED
        self._error_message = reason

    def reset(self) -> None:
        """
        Reset failed step for retry.
        """

        if self._status != StepStatus.FAILED:
            raise WorkflowStepException(
                "Only failed steps can be reset"
            )

        self._status = StepStatus.PENDING
        self._error_message = None