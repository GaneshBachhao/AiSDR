"""
Contact Request DTOs.

Architecture Freeze v5.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CreateContactRequestDTO:
    """Incoming request data for creating a Contact."""

    company_id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    job_title: str | None = None
    linkedin_url: str | None = None


@dataclass(slots=True)
class UpdateContactRequestDTO:
    """Incoming request data for updating a Contact."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    job_title: str | None = None
    linkedin_url: str | None = None
