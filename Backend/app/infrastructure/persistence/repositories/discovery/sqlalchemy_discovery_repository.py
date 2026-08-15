"""
SQLAlchemy Discovery repository.

Architecture Freeze v5.0
"""

from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.discovery_repository import DiscoveryRepository
from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.lead.identifiers.lead_id import LeadId
from app.infrastructure.persistence.mappers.discovery_mapper import DiscoveryMapper
from app.infrastructure.persistence.models.discovery_model import DiscoveryModel


class SqlAlchemyDiscoveryRepository(DiscoveryRepository):
    """SQLAlchemy implementation of the Discovery repository contract."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.mapper = DiscoveryMapper()

    async def get_by_id(self, entity_id: DiscoveryId) -> Discovery | None:
        result = await self._session.execute(
            select(DiscoveryModel).where(DiscoveryModel.id == entity_id.value)
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def add(self, entity: Discovery) -> None:
        self._session.add(self.mapper.to_model(entity))

    async def update(self, entity: Discovery) -> None:
        model = await self._session.get(DiscoveryModel, entity.id.value)
        if model is None:
            raise ValueError(f"Discovery not found: {entity.id.value}")

        model.lead_id = entity.lead_id.value
        model.summary = entity.problem_statement
        model.current_process = entity.current_solution
        model.challenges = entity.business_impact
        model.goals = entity.success_criteria
        model.status = entity.status.value
        model.updated_at = entity.updated_at
        await self._session.flush()

    async def delete(self, entity_id: DiscoveryId) -> None:
        model = await self._session.get(DiscoveryModel, entity_id.value)
        if model is not None:
            await self._session.delete(model)

    async def exists(self, entity_id: DiscoveryId) -> bool:
        result = await self._session.execute(
            select(DiscoveryModel.id).where(DiscoveryModel.id == entity_id.value)
        )
        return result.scalar_one_or_none() is not None

    async def get_by_lead(self, lead_id: LeadId) -> Discovery | None:
        result = await self._session.execute(
            select(DiscoveryModel).where(DiscoveryModel.lead_id == lead_id.value)
        )
        model = result.scalar_one_or_none()
        return None if model is None else self.mapper.to_domain(model)

    async def list(self, skip: int = 0, limit: int = 100) -> list[Discovery]:
        result = await self._session.execute(
            select(DiscoveryModel)
            .order_by(DiscoveryModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]

    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Discovery]:
        pattern = f"%{search_text.strip()}%"
        result = await self._session.execute(
            select(DiscoveryModel)
            .where(
                or_(
                    DiscoveryModel.summary.ilike(pattern),
                    DiscoveryModel.current_process.ilike(pattern),
                    DiscoveryModel.challenges.ilike(pattern),
                    DiscoveryModel.goals.ilike(pattern),
                )
            )
            .order_by(DiscoveryModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [self.mapper.to_domain(model) for model in result.scalars().all()]
