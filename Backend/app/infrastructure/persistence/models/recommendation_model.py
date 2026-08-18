"""
Recommendation ORM model.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.assessment_model import AssessmentModel
from app.infrastructure.persistence.models.base_model import BaseModel


class RecommendationModel(BaseModel):
    """
    Represents an AI recommendation generated from an assessment.
    """

    __tablename__ = "recommendations"

    assessment_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(
            "assessments.id",
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

    solutions: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="[]",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Draft",
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    assessment: Mapped[AssessmentModel] = relationship(
        back_populates="recommendation",
        lazy="joined",
    )
