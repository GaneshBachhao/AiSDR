"""
SQLAlchemy model for AI requests.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.database import Base


class AIRequestModel(Base):
    """
    Persistence model representing an AI request.
    """

    __tablename__ = "ai_requests"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    max_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # AI Response
    # -------------------------------------------------------------------------

    response_content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    response_finish_reason: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    response_prompt_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    response_completion_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    response_total_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    response_created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Failure
    # -------------------------------------------------------------------------

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Execution Lifecycle
    # -------------------------------------------------------------------------

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
