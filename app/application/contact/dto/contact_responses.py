"""
Contact Response DTOs.

Architecture Freeze v4.0

Contains all outgoing application response contracts
for Contact aggregate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ContactResponseDTO:
    """
    Standard Contact response DTO.
    """

    id: str

    company_id: str

    first_name: str

    last_name: str

    email: str

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None

    is_active: bool = True