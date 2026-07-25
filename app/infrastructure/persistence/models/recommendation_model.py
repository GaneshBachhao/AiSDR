"""
Recommendation ORM model.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

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

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    assessment: Mapped[AssessmentModel] = relationship(
        back_populates="recommendation",
        lazy="joined",
    )