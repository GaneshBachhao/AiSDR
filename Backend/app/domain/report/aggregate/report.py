from datetime import UTC, datetime
from uuid import uuid4

from app.domain.shared.base import AggregateRoot

from ..entities.report_section import ReportSection
from ..entities.report_version import ReportVersion
from ..enums.report_status import ReportStatus
from ..events.report_created import ReportCreated
from ..events.report_published import ReportPublished
from ..exceptions.invalid_report_state import InvalidReportState
from ..exceptions.report_exception import ReportException
from ..value_objects.report_id import ReportId
from ..value_objects.report_name import ReportName


class Report(AggregateRoot[ReportId]):
    """
    Aggregate Root representing a business report.
    """

    def __init__(
        self,
        name: ReportName,
        report_id: ReportId | None = None,
    ):
        report_id = report_id or ReportId(uuid4())

        super().__init__(report_id)

        self._name = name

        self._status = ReportStatus.DRAFT

        self._sections: list[ReportSection] = []
        self._versions: list[ReportVersion] = []

        self._published_at: datetime | None = None

        self.add_domain_event(ReportCreated(self.id))

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def name(self) -> ReportName:
        return self._name

    @property
    def status(self) -> ReportStatus:
        return self._status

    @property
    def sections(self) -> list[ReportSection]:
        return list(self._sections)

    @property
    def versions(self) -> list[ReportVersion]:
        return list(self._versions)

    @property
    def published_at(self) -> datetime | None:
        return self._published_at

    # --------------------------------------------------
    # Section Management
    # --------------------------------------------------

    def add_section(
        self,
        section: ReportSection,
    ) -> None:

        if self._status != ReportStatus.DRAFT:
            raise InvalidReportState("Sections can only be added while the report is in DRAFT.")

        self._sections.append(section)
        self.touch()

    # --------------------------------------------------
    # Version Management
    # --------------------------------------------------

    def add_version(
        self,
        version: ReportVersion,
    ) -> None:

        self._versions.append(version)
        self.touch()

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def submit_for_review(self) -> None:

        if not self._sections:
            raise ReportException("A report must contain at least one section.")

        if self._status != ReportStatus.DRAFT:
            raise InvalidReportState("Only draft reports can be submitted for review.")

        self._status = ReportStatus.IN_REVIEW
        self.touch()

    def approve(self) -> None:

        if self._status != ReportStatus.IN_REVIEW:
            raise InvalidReportState("Only reports under review can be approved.")

        self._status = ReportStatus.APPROVED
        self.touch()

    def publish(self) -> None:

        if self._status != ReportStatus.APPROVED:
            raise InvalidReportState("Only approved reports can be published.")

        self._status = ReportStatus.PUBLISHED
        self._published_at = datetime.now(UTC)

        self.touch()

        self.add_domain_event(ReportPublished(self.id))

    def archive(self) -> None:

        if self._status != ReportStatus.PUBLISHED:
            raise InvalidReportState("Only published reports can be archived.")

        self._status = ReportStatus.ARCHIVED
        self.touch()

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    def has_sections(self) -> bool:
        return len(self._sections) > 0

    def is_published(self) -> bool:
        return self._status == ReportStatus.PUBLISHED
