"""
Discovery application mapper.

Architecture Freeze v5.0
"""

from __future__ import annotations

from app.application.discovery.discovery_commands import (
    CreateDiscoveryCommand,
    DeleteDiscoveryCommand,
    UpdateDiscoveryCommand,
)
from app.application.discovery.discovery_queries import (
    GetDiscoveryQuery,
    ListDiscoveryQuery,
    SearchDiscoveryQuery,
)
from app.application.discovery.dto.discovery_requests import (
    CreateDiscoveryRequestDTO,
    DeleteDiscoveryRequestDTO,
    GetDiscoveryRequestDTO,
    ListDiscoveryRequestDTO,
    SearchDiscoveryRequestDTO,
    UpdateDiscoveryRequestDTO,
)
from app.application.discovery.dto.discovery_responses import DiscoveryResponseDTO
from app.domain.discovery.entities.discovery import Discovery


class DiscoveryMapper:
    """Map Discovery API/application contracts to the domain and back."""

    @staticmethod
    def to_create_command(request: CreateDiscoveryRequestDTO) -> CreateDiscoveryCommand:
        return CreateDiscoveryCommand(
            lead_id=request.lead_id,
            problem_statement=request.problem_statement,
            current_solution=request.current_solution,
            business_impact=request.business_impact,
            success_criteria=request.success_criteria,
        )

    @staticmethod
    def to_update_command(
        discovery_id: str,
        request: UpdateDiscoveryRequestDTO,
    ) -> UpdateDiscoveryCommand:
        return UpdateDiscoveryCommand(
            discovery_id=discovery_id,
            problem_statement=request.problem_statement,
            current_solution=request.current_solution,
            business_impact=request.business_impact,
            success_criteria=request.success_criteria,
            status=request.status,
        )

    @staticmethod
    def to_delete_command(
        discovery_id: str | DeleteDiscoveryRequestDTO,
    ) -> DeleteDiscoveryCommand:
        if isinstance(discovery_id, DeleteDiscoveryRequestDTO):
            discovery_id = discovery_id.discovery_id
        return DeleteDiscoveryCommand(discovery_id=discovery_id)

    @staticmethod
    def to_get_query(request: GetDiscoveryRequestDTO) -> GetDiscoveryQuery:
        return GetDiscoveryQuery(discovery_id=request.discovery_id)

    @staticmethod
    def to_list_query(request: ListDiscoveryRequestDTO) -> ListDiscoveryQuery:
        return ListDiscoveryQuery(skip=request.skip, limit=request.limit)

    @staticmethod
    def to_search_query(request: SearchDiscoveryRequestDTO) -> SearchDiscoveryQuery:
        return SearchDiscoveryQuery(
            search_text=request.search_text,
            skip=request.skip,
            limit=request.limit,
        )

    @staticmethod
    def to_response_dto(discovery: Discovery) -> DiscoveryResponseDTO:
        return DiscoveryResponseDTO(
            id=str(discovery.id.value),
            lead_id=str(discovery.lead_id.value),
            problem_statement=discovery.problem_statement,
            current_solution=discovery.current_solution,
            business_impact=discovery.business_impact,
            success_criteria=discovery.success_criteria,
            status=discovery.status.value,
            created_at=discovery.created_at.isoformat(),
            updated_at=discovery.updated_at.isoformat(),
        )

    @staticmethod
    def to_response_list(discoveries: list[Discovery]) -> list[DiscoveryResponseDTO]:
        return [DiscoveryMapper.to_response_dto(item) for item in discoveries]
