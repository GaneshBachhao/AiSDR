from abc import ABC, abstractmethod

from ..aggregate.workflow import Workflow
from ..value_objects.workflow_id import WorkflowId


class WorkflowRepository(ABC):
    """
    Repository abstraction for Workflow aggregate.

    Infrastructure layer provides the implementation.
    """

    @abstractmethod
    def save(self, workflow: Workflow) -> None:
        """
        Persist workflow aggregate.
        """

        pass

    @abstractmethod
    def get_by_id(self, workflow_id: WorkflowId) -> Workflow | None:
        """
        Retrieve workflow by identifier.
        """

        pass

    @abstractmethod
    def get_all(self) -> list[Workflow]:
        """
        Retrieve all workflows.
        """

        pass

    @abstractmethod
    def remove(self, workflow: Workflow) -> None:
        """
        Remove workflow.
        """

        pass
