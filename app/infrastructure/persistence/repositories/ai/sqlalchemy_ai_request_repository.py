"""
SQLAlchemy implementation of AIRequestRepository.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.repositories.ai_request_repository import (
    AIRequestRepository,
)
from app.domain.ai.value_objects.ai_request_id import AIRequestId

from app.infrastructure.persistence.mappers.ai_request_mapper import (
    AIRequestMapper,
)
from app.infrastructure.persistence.models.ai_request_model import (
    AIRequestModel,
)


class SQLAlchemyAIRequestRepository(
    AIRequestRepository,
):
    """
    SQLAlchemy implementation of AIRequestRepository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def save(
        self,
        request: AIRequest,
    ) -> AIRequest:

        model = AIRequestMapper.to_model(
            request,
        )

        await self._session.merge(
            model,
        )

        return request

    async def get_by_id(
        self,
        request_id: AIRequestId,
    ) -> AIRequest | None:

        statement = select(
            AIRequestModel,
        ).where(
            AIRequestModel.id == str(
                request_id,
            ),
        )

        result = await self._session.execute(
            statement,
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return AIRequestMapper.to_domain(
            model,
        )

    async def exists(
        self,
        request_id: AIRequestId,
    ) -> bool:

        statement = select(
            AIRequestModel.id,
        ).where(
            AIRequestModel.id == str(
                request_id,
            ),
        )

        result = await self._session.execute(
            statement,
        )

        return result.scalar_one_or_none() is not None

    async def delete(
        self,
        request: AIRequest,
    ) -> None:

        statement = select(
            AIRequestModel,
        ).where(
            AIRequestModel.id == str(
                request.id,
            ),
        )

        result = await self._session.execute(
            statement,
        )

        model = result.scalar_one_or_none()

        if model is not None:
            await self._session.delete(
                model,
            )