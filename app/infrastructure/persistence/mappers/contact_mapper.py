"""
Contact persistence mapper.

Maps between the Contact domain aggregate and SQLAlchemy ContactModel.
"""

from __future__ import annotations

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.entities.contact import Contact
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.contact.value_objects.email import Email
from app.infrastructure.persistence.models.contact_model import ContactModel


class ContactMapper:
    """Map Contact domain entities and persistence models."""

    @staticmethod
    def to_domain(model: ContactModel) -> Contact:
        """Convert a SQLAlchemy model into a Contact aggregate."""
        contact = Contact(
            id=ContactId(model.id),
            first_name=model.first_name,
            last_name=model.last_name,
            email=Email(model.email),
            phone=model.phone,
            job_title=model.job_title,
            linkedin_url=model.linkedin_url,
            company_id=CompanyId(model.company_id),
            is_active=model.is_active,
        )
        contact.created_at = model.created_at
        contact.updated_at = model.updated_at
        return contact

    @staticmethod
    def to_model(entity: Contact) -> ContactModel:
        """Convert a Contact aggregate into a SQLAlchemy model."""
        return ContactModel(
            id=entity.id.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email.value,
            phone=entity.phone,
            job_title=entity.job_title,
            linkedin_url=entity.linkedin_url,
            company_id=(
                entity.company_id.value
                if entity.company_id is not None
                else None
            ),
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(
        model: ContactModel,
        entity: Contact,
    ) -> ContactModel:
        """Update an existing SQLAlchemy model from a Contact aggregate."""
        model.first_name = entity.first_name
        model.last_name = entity.last_name
        model.email = entity.email.value
        model.phone = entity.phone
        model.job_title = entity.job_title
        model.linkedin_url = entity.linkedin_url
        model.company_id = (
            entity.company_id.value
            if entity.company_id is not None
            else None
        )
        model.is_active = entity.is_active
        model.updated_at = entity.updated_at
        return model
