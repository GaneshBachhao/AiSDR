"""
Repository dependency registration.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.repositories.ai.sqlalchemy_ai_request_repository import (
    SQLAlchemyAIRequestRepository,
)


def ai_request_repository(
    session: AsyncSession,
) -> SQLAlchemyAIRequestRepository:
    """
    Create AIRequestRepository.
    """

    return SQLAlchemyAIRequestRepository(
        session,
    )