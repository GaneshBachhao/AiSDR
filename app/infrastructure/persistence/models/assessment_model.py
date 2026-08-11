"""
Assessment persistence model.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.models.base_model import BaseModel


class AssessmentModel(BaseModel):
    """
    Assessment persistence model.
    """

    __tablename__ = "assessments"

    discovery_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "discoveries.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    maturity_level: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    readiness_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    opportunities: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    risks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # -----------------------------------------------------------------
    # Relationships
    # -----------------------------------------------------------------

    discovery = relationship(
        "DiscoveryModel",
        back_populates="assessment",
        lazy="joined",
    )

    recommendation = relationship(
        "RecommendationModel",
        back_populates="assessment",
        uselist=False,
        cascade="all, delete-orphan",
    )