from datetime import UTC, datetime

from ..value_objects.report_id import ReportId
from ..value_objects.section_id import SectionId


class SectionCompleted:
    """
    Raised when a report section is completed.
    """

    def __init__(
        self,
        report_id: ReportId,
        section_id: SectionId,
    ):
        self.report_id = report_id
        self.section_id = section_id
        self.occurred_at = datetime.now(UTC)
