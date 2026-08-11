"""
Discovery response DTOs.

Architecture Freeze v5.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DiscoveryResponseDTO:
    """Standard Discovery response."""

    id: str
    lead_id: str
    problem_statement: str | None
    current_solution: str | None
    business_impact: str | None
    success_criteria: str | None
    status: str
    created_at: str
    updated_at: str


# Backward-compatible response DTO names retained for existing imports.
CreateDiscoveryResponseDTO = DiscoveryResponseDTO


@dataclass(slots=True)
class DiscoveryListResponseDTO:
    """Optional envelope for future paginated responses."""

    items: list[DiscoveryResponseDTO]
    total: int


@dataclass(slots=True)
class DeleteDiscoveryResponseDTO:
    """Response after deleting a discovery."""

    id: str
    deleted: bool
