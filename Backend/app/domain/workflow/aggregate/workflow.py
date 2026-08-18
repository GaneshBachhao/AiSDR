from datetime import UTC, datetime
from uuid import uuid4

from app.domain.shared.base import AggregateRoot

from ..entities.workflow_step import WorkflowStep
from ..enums.workflow_status import WorkflowStatus
from ..events.workflow_completed import WorkflowCompleted
from ..events.workflow_started import WorkflowStarted
from ..exceptions.invalid_workflow_state import InvalidWorkflowState
from ..exceptions.workflow_exception import WorkflowException
from ..value_objects.workflow_id import WorkflowId
from ..value_objects.workflow_name import WorkflowName


class Workflow(AggregateRoot[WorkflowId]):
    """
    Aggregate Root representing an AI consulting workflow.

    Controls:
    - Workflow lifecycle
    - Step execution flow
    - State transitions
    - Domain consistency
    """

    def __init__(
        self,
        name: WorkflowName,
        workflow_id: WorkflowId | None = None,
    ):
        workflow_id = workflow_id or WorkflowId(uuid4())

        super().__init__(workflow_id)

        self._name = name
        self._status = WorkflowStatus.DRAFT

        self._steps: list[WorkflowStep] = []

        self._started_at: datetime | None = None
        self._completed_at: datetime | None = None

    # ----------------------------
    # Properties
    # ----------------------------

    @property
    def name(self) -> WorkflowName:
        return self._name

    @property
    def status(self) -> WorkflowStatus:
        return self._status

    @property
    def steps(self) -> list[WorkflowStep]:
        return list(self._steps)

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    # ----------------------------
    # Step Management
    # ----------------------------

    def add_step(self, step: WorkflowStep) -> None:
        """
        Add a workflow step.

        Business Rule:
        Steps cannot be added after workflow starts.
        """

        if self._status != WorkflowStatus.DRAFT:
            raise InvalidWorkflowState("Cannot add steps after workflow execution begins")

        self._steps.append(step)
        self.touch()

    # ----------------------------
    # Lifecycle Operations
    # ----------------------------

    def prepare(self) -> None:
        """
        Moves workflow from draft to ready.
        """

        if not self._steps:
            raise WorkflowException("Workflow must contain at least one step")

        if self._status != WorkflowStatus.DRAFT:
            raise InvalidWorkflowState("Only draft workflow can be prepared")

        self._status = WorkflowStatus.READY
        self.touch()

    def start(self) -> None:
        """
        Start workflow execution.
        """

        if self._status != WorkflowStatus.READY:
            raise InvalidWorkflowState("Workflow must be ready before starting")

        self._status = WorkflowStatus.RUNNING
        self._started_at = datetime.now(UTC)

        self.touch()
        self.add_domain_event(WorkflowStarted(self.id))

    def complete(self) -> None:
        """
        Complete workflow execution.
        """

        if self._status != WorkflowStatus.RUNNING:
            raise InvalidWorkflowState("Only running workflow can be completed")

        if not all(step.is_completed for step in self._steps):
            raise WorkflowException("All workflow steps must be completed")

        self._status = WorkflowStatus.COMPLETED
        self._completed_at = datetime.now(UTC)

        self.touch()
        self.add_domain_event(WorkflowCompleted(self.id))

    def fail(self) -> None:
        """
        Mark workflow as failed.
        """

        if self._status not in (
            WorkflowStatus.RUNNING,
            WorkflowStatus.READY,
        ):
            raise InvalidWorkflowState("Workflow cannot fail from current state")

        self._status = WorkflowStatus.FAILED
        self.touch()

    def cancel(self) -> None:
        """
        Cancel workflow.
        """

        if self._status == WorkflowStatus.COMPLETED:
            raise InvalidWorkflowState("Completed workflow cannot be cancelled")

        self._status = WorkflowStatus.CANCELLED
        self.touch()

    # ----------------------------
    # Queries
    # ----------------------------

    def is_completed(self) -> bool:
        return self._status == WorkflowStatus.COMPLETED

    def has_steps(self) -> bool:
        return len(self._steps) > 0
