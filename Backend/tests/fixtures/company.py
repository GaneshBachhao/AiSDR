"""
Company fixtures.
"""

from __future__ import annotations

import pytest

from app.domain.company.entities.company import Company


@pytest.fixture
def company() -> Company:
    return Company(
        name="Microsoft",
        website="https://microsoft.com",
    )


@pytest.fixture
def company_list() -> list[Company]:
    return [
        Company(name="Microsoft"),
        Company(name="Google"),
        Company(name="Amazon"),
    ]
