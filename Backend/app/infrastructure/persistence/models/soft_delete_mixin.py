"""
Soft delete persistence mixin.

Provides soft deletion support for persistent entities.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin:
    """
    Adds soft deletion support to a persistent entity.
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def mark_deleted(self) -> None:
        """
        Mark the entity as deleted.
        """

        self.is_deleted = True
        self.deleted_at = datetime.now(
            UTC,
        )

    def restore(self) -> None:
        """
        Restore a soft-deleted entity.
        """

        self.is_deleted = False
        self.deleted_at = None
