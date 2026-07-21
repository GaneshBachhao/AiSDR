from datetime import UTC, datetime
from typing import Optional
from uuid import uuid4

from domain.shared.base import Entity

from ..exceptions.report_exception import ReportException
from ..value_objects.version_id import VersionId
from ..value_objects.version_number import VersionNumber


class ReportVersion(Entity[VersionId]):
    """
    Entity representing a report version.
    """

    def __init__(
        self,
        version_number: VersionNumber,
        change_summary: str,
        version_id: Optional[VersionId] = None,
    ):
        version_id = version_id or VersionId(uuid4())

        super().__init__(version_id)

        self._version_number = version_number
        self._change_summary = change_summary.strip()

        self._published = False

        self._created_at = datetime.now(UTC)
        self._published_at: Optional[datetime] = None

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def version_number(self) -> VersionNumber:
        return self._version_number

    @property
    def change_summary(self) -> str:
        return self._change_summary

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_published(self) -> bool:
        return self._published

    @property
    def published_at(self) -> Optional[datetime]:
        return self._published_at

    # --------------------------------------------------
    # Behavior
    # --------------------------------------------------

    def publish(self) -> None:

        if self._published:
            raise ReportException(
                "Version has already been published."
            )

        self._published = True
        self._published_at = datetime.now(UTC)