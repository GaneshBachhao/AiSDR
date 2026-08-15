from ..aggregate.report import Report
from ..entities.report_version import ReportVersion
from ..exceptions.report_exception import ReportException
from .report_validation_service import ReportValidationService


class ReportPublicationService:
    """
    Coordinates report publication workflow.
    """

    def __init__(
        self,
        validation_service: ReportValidationService,
    ):
        self._validation_service = validation_service

    def submit_for_review(
        self,
        report: Report,
    ) -> None:

        self._validation_service.validate_can_submit_for_review(
            report
        )

        report.submit_for_review()

    def approve(
        self,
        report: Report,
    ) -> None:

        self._validation_service.validate_can_approve(
            report
        )

        report.approve()

    def publish(
        self,
        report: Report,
        version: ReportVersion,
    ) -> None:

        self._validation_service.validate_can_publish(
            report
        )

        version.publish()

        report.publish()

    def create_version(
        self,
        report: Report,
        version: ReportVersion,
    ) -> None:

        report.add_version(version)

    def archive(
        self,
        report: Report,
    ) -> None:

        if not report.is_published():
            raise ReportException(
                "Only published reports can be archived."
            )

        report.archive()