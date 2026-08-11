from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.recommendation.commands.add_roadmap_phase import (
    AddRoadmapPhaseCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.add_roadmap_phase_validator import (
    AddRoadmapPhaseValidator,
)
from app.domain.recommendation.entities.roadmap_phase import (
    RoadmapPhase,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class AddRoadmapPhaseHandler:
    """
    Handles adding roadmap phases to a recommendation.
    """

    def __init__(
        self,
        repository: RecommendationRepository,
        validator: AddRoadmapPhaseValidator,
        mapper: RecommendationMapper,
    ) -> None:

        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddRoadmapPhaseCommand,
    ) -> RecommendationDTO:

        validation = self._validator.validate(
            command,
        )

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        recommendation = await self._repository.get_by_id(
            RecommendationId(
                command.recommendation_id,
            ),
        )

        if recommendation is None:
            raise ValueError(
                "Recommendation not found."
            )

        phase = RoadmapPhase(
            phase_name=command.name,
            sequence=command.sequence,
            description=command.description,
            estimated_duration="Not specified",
        )

        recommendation.add_roadmap_phase(
            phase,
        )

        recommendation = await self._repository.save(
            recommendation,
        )

        return self._mapper.domain_to_dto(
            recommendation,
        )