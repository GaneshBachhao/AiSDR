"""
Company persistence mapper.

Domain <-> ORM conversion always unwraps strongly typed IDs to UUIDs
when constructing ORM models.
"""
from __future__ import annotations

from app.domain.company.entities.company import Company
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry
from app.infrastructure.persistence.models.company_model import CompanyModel


class CompanyMapper:
    """Maps Company domain entities and ORM models."""

    @staticmethod
    def to_domain(model: CompanyModel) -> Company:
        company = Company(
            id=CompanyId(model.id),
            name=model.name,
            website=model.website,
            industry=Industry(model.industry) if model.industry else None,
            company_size=(
                CompanySize(model.company_size)
                if model.company_size
                else None
            ),
            employee_count=model.employee_count,
            country=model.country,
            state=model.state,
            city=model.city,
            is_active=model.is_active,
        )
        company.created_at = model.created_at
        company.updated_at = model.updated_at
        return company

    @staticmethod
    def to_model(entity: Company) -> CompanyModel:
        return CompanyModel(
            id=entity.id.value,
            name=entity.name,
            website=entity.website,
            industry=entity.industry.value if entity.industry else None,
            company_size=(
                entity.company_size.value
                if entity.company_size
                else None
            ),
            employee_count=entity.employee_count,
            country=entity.country,
            state=entity.state,
            city=entity.city,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(
        model: CompanyModel,
        entity: Company,
    ) -> CompanyModel:
        model.name = entity.name
        model.website = entity.website
        model.industry = (
            entity.industry.value
            if entity.industry
            else None
        )
        model.company_size = (
            entity.company_size.value
            if entity.company_size
            else None
        )
        model.employee_count = entity.employee_count
        model.country = entity.country
        model.state = entity.state
        model.city = entity.city
        model.is_active = entity.is_active
        return model
