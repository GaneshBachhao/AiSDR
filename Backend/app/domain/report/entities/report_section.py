from datetime import UTC, datetime
from uuid import uuid4

from app.domain.shared.base import Entity

from ..enums.section_status import SectionStatus
from ..exceptions.report_section_exception import ReportSectionException
from ..value_objects.report_name import ReportName
from ..value_objects.section_id import SectionId


class ReportSection(Entity[SectionId]):
    """
    Entity representing a report section.
    """

    def __init__(
        self,
        title: ReportName,
        display_order: int,
        section_id: SectionId | None = None,
    ):
        if display_order < 1:
            raise ReportSectionException("Display order must be greater than zero.")

        section_id = section_id or SectionId(uuid4())

        super().__init__(section_id)

        self._title = title
        self._display_order = display_order

        self._content = ""

        self._status = SectionStatus.DRAFT

        self._created_at = datetime.now(UTC)
        self._updated_at = self._created_at

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def title(self) -> ReportName:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def display_order(self) -> int:
        return self._display_order

    @property
    def status(self) -> SectionStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_completed(self) -> bool:
        return self._status == SectionStatus.COMPLETED

    @property
    def is_locked(self) -> bool:
        return self._status == SectionStatus.LOCKED

    # --------------------------------------------------
    # Behavior
    # --------------------------------------------------

    def update_content(
        self,
        content: str,
    ) -> None:

        if self._status == SectionStatus.LOCKED:
            raise ReportSectionException("Locked sections cannot be modified.")

        self._content = content.strip()
        self._touch()

    def complete(self) -> None:

        if not self._content:
            raise ReportSectionException("Section content cannot be empty.")

        self._status = SectionStatus.COMPLETED
        self._touch()

    def lock(self) -> None:

        if self._status != SectionStatus.COMPLETED:
            raise ReportSectionException("Only completed sections can be locked.")

        self._status = SectionStatus.LOCKED
        self._touch()

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _touch(self) -> None:
        self._updated_at = datetime.now(UTC)
