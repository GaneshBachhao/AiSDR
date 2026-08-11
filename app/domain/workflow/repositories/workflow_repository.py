from abc import ABC, abstractmethod
from typing import Optional, List

from ..aggregate.workflow import Workflow
from ..value_objects.workflow_id import WorkflowId


class WorkflowRepository(ABC):
    """
    Repository abstraction for Workflow aggregate.

    Infrastructure layer provides the implementation.
    """


    @abstractmethod
    def save(
        self,
        workflow: Workflow
    ) -> None:
        """
        Persist workflow aggregate.
        """

        pass



    @abstractmethod
    def get_by_id(
        self,
        workflow_id: WorkflowId
    ) -> Optional[Workflow]:
        """
        Retrieve workflow by identifier.
        """

        pass



    @abstractmethod
    def get_all(self) -> List[Workflow]:
        """
        Retrieve all workflows.
        """

        pass



    @abstractmethod
    def remove(
        self,
        workflow: Workflow
    ) -> None:
        """
        Remove workflow.
        """

        pass