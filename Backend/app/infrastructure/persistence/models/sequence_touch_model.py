"""
SequenceTouch ORM model.

Owned entirely by SequenceModel -- no independent repository. Touches are
set once when a Sequence is created and never mutated afterward.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base_model import BaseModel


class SequenceTouchModel(BaseModel):
    """
    Represents one planned touch within a Sequence.
    """

    __tablename__ = "sequence_touches"

    sequence_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("sequences.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    wait_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
