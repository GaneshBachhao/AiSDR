from abc import ABC, abstractmethod
from typing import List, Optional

from ..aggregate.report import Report
from ..value_objects.report_id import ReportId


class ReportRepository(ABC):
    """
    Repository abstraction for the Report aggregate.
    """

    @abstractmethod
    def save(
        self,
        report: Report,
    ) -> None:
        """
        Persist a report aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        report_id: ReportId,
    ) -> Optional[Report]:
        """
        Retrieve a report by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Report]:
        """
        Retrieve all reports.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        report: Report,
    ) -> None:
        """
        Remove a report.
        """
        raise NotImplementedError