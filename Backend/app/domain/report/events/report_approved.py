from datetime import UTC, datetime

from ..value_objects.report_id import ReportId


class ReportApproved:
    """
    Raised when a report is approved.
    """

    def __init__(self, report_id: ReportId):
        self.report_id = report_id
        self.occurred_at = datetime.now(UTC)