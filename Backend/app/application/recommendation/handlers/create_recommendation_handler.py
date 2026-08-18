"""Create Recommendation application handler.

Note on this module's history: a separate ``GenerateRecommendationHandler``
previously existed alongside this one, with its own command/validator, but
was never wired into any router or DI dependency and called a repository
method (``get_by_assessment``) that doesn't exist on the real, concrete
``RecommendationRepository`` -- it could never have run successfully. This
handler is the only one actually reachable via ``POST /recommendations``,
so the AI-generation work belongs here; the orphaned handler/command/
validator were deleted rather than left as a second, misleading "real"
implementation. See docs/product_backlog.md for the full finding.
"""

from __future__ import annotations

import json
import logging
import re

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.recommendation.commands.create_recommendation import CreateRecommendationCommand
from app.application.recommendation.dto.recommendation_dto import RecommendationDTO
from app.application.recommendation.mappers.recommendation_mapper import RecommendationMapper
from app.application.recommendation.validators.create_recommendation_validator import (
    CreateRecommendationValidator,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.infrastructure.ai.composition import default_model_for_provider
from app.infrastructure.configuration.solution_catalog import load_solution_catalog

logger = logging.getLogger(__name__)

_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)

_VALID_SOLUTION_TYPES = (
    "AI Agent",
    "Copilot",
    "Automation",
    "Analytics",
    "Chatbot",
    "Knowledge Assistant",
    "Document Intelligence",
    "Predictive AI",
    "Custom",
)
_VALID_PRIORITIES = ("Low", "Medium", "High", "Critical")


class CreateRecommendationHandler:
    """Create a Recommendation aggregate, AI-generating its Solutions from
    the linked Assessment, and persist it.

    Idempotent: re-running for the same assessment returns the existing
    Recommendation rather than creating a duplicate.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        ai_execution_service: AIExecutionService,
        ai_provider_name: str = "gemini",
    ) -> None:
        self._unit_of_work = unit_of_work
        self._ai_execution_service = ai_execution_service
        self._ai_provider_name = ai_provider_name

    async def handle(self, command: CreateRecommendationCommand) -> RecommendationDTO:
        validation = CreateRecommendationValidator().validate(command)
        if not validation.success:
            raise ValueError(validation.errors)

        assessment_id = AssessmentId(command.assessment_id)

        async with self._unit_of_work:
            existing = await self._unit_of_work.recommendation_repository.get_by_assessment_id(assessment_id)
            if existing is not None:
                return RecommendationMapper.domain_to_dto(existing)

            assessment = await self._unit_of_work.assessment_repository.get_by_id(assessment_id)
            if assessment is None:
                raise NotFoundException(
                    message="Assessment not found.",
                    details={"assessment_id": str(command.assessment_id)},
                )

        # AI call happens outside the DB transaction -- no need to hold a
        # session open for the duration of an external network call.
        solutions = await self._generate_solutions(assessment)

        recommendation = Recommendation(
            assessment_id=assessment_id,
            executive_summary=(f"{len(solutions)} solution(s) generated from assessment findings."),
        )
        for solution in solutions:
            recommendation.add_solution(solution)

        async with self._unit_of_work:
            await self._unit_of_work.recommendation_repository.add(recommendation)
            await self._unit_of_work.commit()

        return RecommendationMapper.domain_to_dto(recommendation)

    async def _generate_solutions(self, assessment) -> list[Solution]:
        if not self._has_meaningful_content(assessment):
            raise ValueError(
                "Assessment has no summary/analysis to generate recommendations from. "
                "Populate summary, strengths, weaknesses, opportunities, or risks first."
            )

        assessment_context = self._assessment_context(assessment)
        catalog = load_solution_catalog()
        prompt = self._build_prompt(assessment_context, catalog)

        request = AIRequest(
            provider=ProviderName(self._ai_provider_name),
            model=ModelName(default_model_for_provider(self._ai_provider_name)),
            prompt=Prompt(prompt),
            temperature=Temperature(0.2),
            max_tokens=MaxTokens(1500),
        )
        response = await self._ai_execution_service.execute(request)

        return self._parse_solutions(response.content)

    @staticmethod
    def _has_meaningful_content(assessment) -> bool:
        """Whether the assessment has any human-entered analysis to generate
        from. ``maturity_level`` deliberately excluded -- it defaults to
        ``INITIAL`` even on a completely empty assessment, so it alone must
        never be treated as "content"."""
        return any(
            [
                assessment.summary,
                assessment.strengths,
                assessment.weaknesses,
                assessment.opportunities_summary,
                assessment.risks,
            ]
        )

    @staticmethod
    def _assessment_context(assessment) -> str:
        parts = [
            f"Maturity level: {assessment.maturity_level.value}" if assessment.maturity_level else None,
            f"Summary: {assessment.summary}" if assessment.summary else None,
            f"Strengths: {assessment.strengths}" if assessment.strengths else None,
            f"Weaknesses: {assessment.weaknesses}" if assessment.weaknesses else None,
            f"Opportunities: {assessment.opportunities_summary}"
            if assessment.opportunities_summary
            else None,
            f"Risks: {assessment.risks}" if assessment.risks else None,
        ]
        return "\n".join(p for p in parts if p)

    @staticmethod
    def _build_prompt(assessment_context: str, catalog: list) -> str:
        catalog_json = json.dumps(
            [
                {
                    "id": entry.id,
                    "sector": entry.sector,
                    "pain_point": entry.pain_point,
                    "title": entry.title,
                    "description": entry.description,
                    "is_existing_offering": entry.is_existing_offering,
                }
                for entry in catalog
            ]
        )
        return f"""You are generating technology solution recommendations for a
business assessment. Follow this order strictly:
1. Identify the company's pain points from the assessment below.
2. Map each pain point to a matching entry in the AI Solution Catalog.
3. If no catalog entry fits a pain point, propose a generic, sector-appropriate
   AI solution instead -- but you must set "is_existing_offering" to false for it.
4. Never claim a generic idea is an existing offering, and never omit a real
   catalog match in favor of inventing something generic.

Return 1 to 4 solutions as a strict JSON array, no markdown fences, no prose
before or after. Each item must have exactly these fields:
{{"title": string, "description": string, "solution_type": one of {list(_VALID_SOLUTION_TYPES)},
"priority": one of {list(_VALID_PRIORITIES)}, "is_existing_offering": boolean}}

Assessment:
{assessment_context}

AI Solution Catalog:
{catalog_json}
"""

    @classmethod
    def _parse_solutions(cls, raw_content: str) -> list[Solution]:
        cleaned = _JSON_FENCE.sub("", raw_content.strip()).strip()
        try:
            items = json.loads(cleaned)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"AI response was not valid JSON: {exc}") from exc

        if not isinstance(items, list) or not items:
            raise ValueError("AI response did not contain any solutions.")

        solutions: list[Solution] = []
        for item in items:
            try:
                solutions.append(
                    Solution(
                        title=str(item["title"]).strip(),
                        description=str(item["description"]).strip(),
                        solution_type=item["solution_type"],
                        priority=item.get("priority", "Medium"),
                        is_existing_offering=bool(item.get("is_existing_offering", False)),
                    )
                )
            except (KeyError, ValueError) as exc:
                logger.warning("Skipping unparseable AI solution entry %r: %s", item, exc)

        if not solutions:
            raise ValueError("No valid solutions could be parsed from the AI response.")

        return solutions
