from __future__ import annotations

import pytest

from app.domain.company.entities.company import Company
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry


def test_company_strips_whitespace_from_text_fields() -> None:
    company = Company(name="  Acme  ", website="  https://acme.example  ", country="  India  ")

    assert company.name == "Acme"
    assert company.website == "https://acme.example"
    assert company.country == "India"


def test_company_rejects_an_empty_name() -> None:
    with pytest.raises(ValueError):
        Company(name="   ")


def test_company_rejects_a_negative_employee_count() -> None:
    with pytest.raises(ValueError):
        Company(name="Acme", employee_count=-1)


def test_company_defaults_to_active() -> None:
    company = Company(name="Acme")

    assert company.is_active is True


def test_update_name_strips_and_touches() -> None:
    company = Company(name="Acme")
    updated_before = company.updated_at

    company.update_name("  New Name  ")

    assert company.name == "New Name"
    assert company.updated_at >= updated_before


def test_update_name_rejects_empty() -> None:
    company = Company(name="Acme")

    with pytest.raises(ValueError):
        company.update_name("   ")


def test_rename_is_an_alias_for_update_name() -> None:
    company = Company(name="Acme")

    company.rename("Renamed")

    assert company.name == "Renamed"


def test_update_website_clears_to_none_on_blank_input() -> None:
    company = Company(name="Acme", website="https://acme.example")

    company.update_website("")

    assert company.website is None


def test_update_industry_and_company_size() -> None:
    company = Company(name="Acme")

    company.update_industry(Industry.INFORMATION_TECHNOLOGY)
    company.update_company_size(CompanySize.SMALL)

    assert company.industry is Industry.INFORMATION_TECHNOLOGY
    assert company.company_size is CompanySize.SMALL


def test_update_employee_count_rejects_negative() -> None:
    company = Company(name="Acme", employee_count=10)

    with pytest.raises(ValueError):
        company.update_employee_count(-5)


def test_update_location_only_changes_provided_fields() -> None:
    company = Company(name="Acme", country="India", state="Karnataka", city="Bengaluru")

    company.update_location(city="Mumbai")

    assert company.country == "India"
    assert company.state == "Karnataka"
    assert company.city == "Mumbai"


def test_activate_and_deactivate() -> None:
    company = Company(name="Acme")

    company.deactivate()
    assert company.is_active is False

    company.activate()
    assert company.is_active is True
