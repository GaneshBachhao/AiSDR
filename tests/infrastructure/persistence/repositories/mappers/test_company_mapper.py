"""
Tests for Company SQLAlchemy mapper.
"""

from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import uuid4

from app.domain.company.entities.company import Company
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry
from app.infrastructure.persistence.mappers.company_mapper import (
    CompanyMapper,
)
from app.infrastructure.persistence.models.company_model import (
    CompanyModel,
)


def create_company() -> Company:
    """
    Create a sample Company entity.
    """

    company = Company(
        id=CompanyId(uuid4()),
        name="OpenAI",
        website="https://openai.com",
        industry=Industry("Information Technology"),
        company_size=CompanySize("Large"),
        country="USA",
        state="California",
        city="San Francisco",
        is_active=True,
    )

    company._created_at = datetime.now(UTC)
    company._updated_at = datetime.now(UTC)

    return company


def create_model() -> CompanyModel:
    """
    Create a sample CompanyModel.
    """

    return CompanyModel(
        id=uuid4(),
        name="OpenAI",
        website="https://openai.com",
        industry="Information Technology",
        company_size="Large",
        country="USA",
        state="California",
        city="San Francisco",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


# ==========================================================
# to_domain
# ==========================================================


def test_to_domain_maps_all_fields() -> None:
    """
    Model should convert to domain entity.
    """

    model = create_model()

    company = CompanyMapper.to_domain(model)

    assert company.id.value == model.id
    assert company.name == model.name
    assert company.website == model.website
    assert company.industry.value == model.industry
    assert company.company_size.value == model.company_size
    assert company.country == model.country
    assert company.state == model.state
    assert company.city == model.city
    assert company.is_active == model.is_active
    assert company.created_at == model.created_at
    assert company.updated_at == model.updated_at


def test_to_domain_handles_optional_none_fields() -> None:
    """
    Optional values should remain None.
    """

    model = create_model()

    model.website = None
    model.industry = None
    model.company_size = None
    model.country = None
    model.state = None
    model.city = None

    company = CompanyMapper.to_domain(model)

    assert company.website is None
    assert company.industry is None
    assert company.company_size is None
    assert company.country is None
    assert company.state is None
    assert company.city is None


# ==========================================================
# to_model
# ==========================================================


def test_to_model_maps_all_fields() -> None:
    """
    Domain entity should convert to SQLAlchemy model.
    """

    company = create_company()

    model = CompanyMapper.to_model(company)

    assert model.id == company.id.value
    assert model.name == company.name
    assert model.website == company.website
    assert model.industry == company.industry.value
    assert model.company_size == company.company_size.value
    assert model.country == company.country
    assert model.state == company.state
    assert model.city == company.city
    assert model.is_active == company.is_active


def test_to_model_handles_optional_none_fields() -> None:
    """
    Optional None values should remain None.
    """

    company = create_company()

    company.website = None
    company.industry = None
    company.company_size = None
    company.country = None
    company.state = None
    company.city = None

    model = CompanyMapper.to_model(company)

    assert model.website is None
    assert model.industry is None
    assert model.company_size is None
    assert model.country is None
    assert model.state is None
    assert model.city is None


# ==========================================================
# update_model
# ==========================================================


def test_update_model_updates_existing_model() -> None:
    """
    Existing model should be updated.
    """

    model = create_model()

    company = create_company()

    company.name = "Microsoft"
    company.website = "https://microsoft.com"
    company.country = "India"
    company.state = "Maharashtra"
    company.city = "Pune"
    company.is_active = False

    updated = CompanyMapper.update_model(
        model,
        company,
    )

    assert updated is model
    assert model.name == "Microsoft"
    assert model.website == "https://microsoft.com"
    assert model.country == "India"
    assert model.state == "Maharashtra"
    assert model.city == "Pune"
    assert model.is_active is False


def test_update_model_handles_optional_none_fields() -> None:
    """
    update_model should correctly update optional None values.
    """

    model = create_model()

    company = create_company()

    company.website = None
    company.industry = None
    company.company_size = None
    company.country = None
    company.state = None
    company.city = None

    CompanyMapper.update_model(
        model,
        company,
    )

    assert model.website is None
    assert model.industry is None
    assert model.company_size is None
    assert model.country is None
    assert model.state is None
    assert model.city is None