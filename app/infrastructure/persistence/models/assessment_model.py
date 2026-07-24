"""
Assessment ORM model.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database.base import (
    Base,
    EntityMixin,
)


class AssessmentModel(Base, EntityMixin):
    """
    Stores AI assessment results for a Lead.
    """

    __tablename__ = "assessments"

    lead_id: Mapped[str] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    maturity_level: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        String(4000),
        nullable=False,
    )

    strengths: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    weaknesses: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    opportunities: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    risks: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    metadata: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    lead: Mapped["LeadModel"] = relationship(
        "LeadModel",
        lazy="joined",
    )