"""
SQLAlchemy implementation of ContactRepository.
"""

from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.contact_repository import ContactRepository
from app.domain.contact.entities.contact import Contact
from app.domain.contact.identifiers.contact_id import ContactId
from app.infrastructure.persistence.mappers.contact_mapper import ContactMapper
from app.infrastructure.persistence.models.contact_model import ContactModel
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyContactRepository(
    SqlAlchemyRepository[
        Contact,
        ContactModel,
        ContactId,
    ],
    ContactRepository,
):
    """SQLAlchemy implementation of ContactRepository."""

    model_type = ContactModel

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            mapper=ContactMapper(),
        )

    async def find_by_email(
        self,
        email: str,
    ) -> Contact | None:
        """Retrieve a contact by normalized email."""
        result = await self._session.execute(
            select(ContactModel).where(
                ContactModel.email == email.strip().lower(),
            )
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self.mapper.to_domain(model)

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contact]:
        """Return paginated contacts ordered by name."""
        result = await self._session.execute(
            select(ContactModel)
            .order_by(
                ContactModel.last_name.asc(),
                ContactModel.first_name.asc(),
            )
            .offset(skip)
            .limit(limit)
        )
        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]

    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contact]:
        """Return contacts matching searchable contact fields."""
        query_text = search_text.strip()

        if not query_text:
            return await self.list(
                skip=skip,
                limit=limit,
            )

        pattern = f"%{query_text}%"

        result = await self._session.execute(
            select(ContactModel)
            .where(
                or_(
                    ContactModel.first_name.ilike(pattern),
                    ContactModel.last_name.ilike(pattern),
                    ContactModel.email.ilike(pattern),
                    ContactModel.phone.ilike(pattern),
                    ContactModel.job_title.ilike(pattern),
                    ContactModel.linkedin_url.ilike(pattern),
                )
            )
            .order_by(
                ContactModel.last_name.asc(),
                ContactModel.first_name.asc(),
            )
            .offset(skip)
            .limit(limit)
        )

        return [
            self.mapper.to_domain(model)
            for model in result.scalars().all()
        ]
