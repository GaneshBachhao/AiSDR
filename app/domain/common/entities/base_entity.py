from __future__ import annotations

from datetime import UTC, datetime
from typing import Generic, TypeVar

from app.domain.shared.base.entity import Entity


TId = TypeVar("TId")


class BaseEntity(Entity[TId], Generic[TId]):
    """
    Base entity with identity and audit timestamps.
    """

    def __init__(
        self,
        entity_id: TId,
    ) -> None:
        super().__init__(entity_id)

        now = datetime.now(UTC)

        self._created_at = now
        self._updated_at = now

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def touch(self) -> None:
        """
        Update modification timestamp.
        """
        self._updated_at = datetime.now(UTC)