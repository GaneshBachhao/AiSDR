"""
Company Request DTOs.

Architecture Freeze v5.0
Contains incoming application request contracts for the Company aggregate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CreateCompanyRequestDTO:
    """Request DTO for creating a company."""

    name: str
    website: str | None = None
    industry: str | None = None
    company_size: str | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None


@dataclass
class UpdateCompanyRequestDTO:
    """Request DTO for updating a company."""

    name: str | None = None
    website: str | None = None
    industry: str | None = None
    company_size: str | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
