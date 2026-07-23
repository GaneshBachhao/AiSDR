from __future__ import annotations

from app.application.common.handler.base_handler import (
    BaseHandler,
)
from app.application.common.handler.handler_context import (
    HandlerContext,
)
from app.application.common.handler.handler_result import (
    HandlerResult,
)
from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)
from app.application.recommendation.dto.recommendation_dto import (
    RecommendationDTO,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.application.recommendation.validators.generate_recommendation_validator import (
    GenerateRecommendationValidator,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)
from app.domain.recommendation.repositories.recommendation_repository import (
    RecommendationRepository,
)


class GenerateRecommendationHandler(
    BaseHandler[
        GenerateRecommendationCommand,
        RecommendationDTO,
    ]
):
    """
    Generates AI recommendations from an Assessment.
    """

    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        recommendation_repository: RecommendationRepository,
        validator: GenerateRecommendationValidator | None = None,
    ) -> None:

        self._assessment_repository = (
            assessment_repository
        )

        self._recommendation_repository = (
            recommendation_repository
        )

        self._validator = (
            validator
            if validator is not None
            else GenerateRecommendationValidator()
        )

    async def handle(
        self,
        request: GenerateRecommendationCommand,
        context: HandlerContext,
    ) -> HandlerResult[RecommendationDTO]:
        """
        Generate Recommendation.
        """

        validation = self._validator.validate(
            request,
        )

        if validation.has_errors():

            return HandlerResult.failure(
                message="Recommendation validation failed.",
                errors=validation.error_messages(),
                metadata=context.to_dict(),
            )

        assessment_id = (
            RecommendationMapper.command_to_assessment_id(
                request,
            )
        )

        assessment = (
            await self._assessment_repository.get_by_id(
                assessment_id,
            )
        )

        if assessment is None:

            return HandlerResult.failure(
                message="Assessment not found.",
                errors=["Assessment does not exist."],
                metadata=context.to_dict(),
            )

        existing = (
            await self._recommendation_repository.get_by_assessment(
                assessment.id,
            )
        )

        if existing is not None:

            dto = RecommendationMapper.domain_to_dto(
                existing,
            )

            return HandlerResult.ok(
                data=dto,
                message="Recommendation already exists.",
                metadata=context.to_dict(),
            )

        recommendation = Recommendation(
            assessment_id=assessment.id,
        )

        saved = (
            await self._recommendation_repository.save(
                recommendation,
            )
        )

        dto = RecommendationMapper.domain_to_dto(
            saved,
        )

        return HandlerResult.ok(
            data=dto,
            message="Recommendation generated successfully.",
            metadata=context.to_dict(),
        )