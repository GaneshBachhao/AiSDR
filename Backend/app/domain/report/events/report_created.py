from app.domain.shared.base import DomainEvent

from ..value_objects.report_id import ReportId


class ReportCreated(DomainEvent):
    """
    Raised when a report is created.
    """

    def __init__(self, report_id: ReportId):
        super().__init__()
        self.report_id = report_id
