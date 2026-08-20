"""
Sequence ORM model.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.base_model import BaseModel
from app.infrastructure.persistence.models.sequence_touch_model import SequenceTouchModel


class SequenceModel(BaseModel):
    """
    Represents a planned multichannel touch cadence for a Lead.
    """

    __tablename__ = "sequences"

    lead_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Draft",
    )

    current_touch_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    stop_reason: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    # selectin, not joined: joined eager-loading against a collection
    # duplicates the parent row once per child row, which then requires
    # callers to remember Result.unique() everywhere. selectin issues a
    # separate `WHERE sequence_id IN (...)` query instead, avoiding that
    # footgun entirely while still eager-loading (required for async --
    # the default lazy="select" would need a lazy load outside the
    # request's greenlet context).
    touches: Mapped[list[SequenceTouchModel]] = relationship(
        order_by="SequenceTouchModel.position",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
