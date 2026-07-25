"""
Assessment ORM model.
"""

from __future__ import annotations

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
from app.infrastructure.persistence.models.discovery_model import DiscoveryModel


class AssessmentModel(BaseModel):
    """
    Represents an AI assessment generated from a discovery.
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

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
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

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    discovery: Mapped[DiscoveryModel] = relationship(
        back_populates="assessment",
        lazy="joined",
    )

    recommendation: Mapped["RecommendationModel | None"] = relationship(
        "RecommendationModel",
        back_populates="assessment",
        uselist=False,
        cascade="all, delete-orphan",
    )