"""
Company Response DTOs.

Architecture Freeze v5.0
Contains outgoing application response contracts for the Company aggregate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompanyResponseDTO:
    """Standard Company response DTO."""

    id: str
    name: str
    website: str | None = None
    industry: str | None = None
    company_size: str | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    is_active: bool = True
