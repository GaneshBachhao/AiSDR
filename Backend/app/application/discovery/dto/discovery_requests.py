"""Discovery request DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CreateDiscoveryRequestDTO:
    """Request to create a discovery session."""

    lead_id: str
    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None


@dataclass(slots=True)
class UpdateDiscoveryRequestDTO:
    """Request to update a discovery session."""

    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None
    status: str | None = None


@dataclass(slots=True)
class GetDiscoveryRequestDTO:
    """Request to retrieve a discovery."""

    discovery_id: str


@dataclass(slots=True)
class ListDiscoveryRequestDTO:
    """Request to list discoveries."""

    skip: int = 0
    limit: int = 100


@dataclass(slots=True)
class SearchDiscoveryRequestDTO:
    """Request to search discoveries."""

    search_text: str
    skip: int = 0
    limit: int = 100


@dataclass(slots=True)
class DeleteDiscoveryRequestDTO:
    """Request to delete a discovery."""

    discovery_id: str
