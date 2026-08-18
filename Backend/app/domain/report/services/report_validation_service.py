from ..aggregate.report import Report
from ..enums.report_status import ReportStatus
from ..exceptions.report_exception import ReportException


class ReportValidationService:
    """
    Domain service responsible for report validation.
    """

    def validate_can_submit_for_review(
        self,
        report: Report,
    ) -> None:
        """
        Validate report before review.
        """

        if not report.has_sections():
            raise ReportException("A report must contain at least one section.")

        incomplete = [section for section in report.sections if not section.is_completed]

        if incomplete:
            raise ReportException("All report sections must be completed before review.")

    def validate_can_approve(
        self,
        report: Report,
    ) -> None:

        if report.status != ReportStatus.IN_REVIEW:
            raise ReportException("Only reports under review can be approved.")

    def validate_can_publish(
        self,
        report: Report,
    ) -> None:

        if report.status != ReportStatus.APPROVED:
            raise ReportException("Only approved reports can be published.")
