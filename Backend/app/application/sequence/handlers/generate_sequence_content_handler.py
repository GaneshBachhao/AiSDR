"""
Generate Sequence Content application handler (EPIC-09.2).

The first prose-generation, application-layer AI call site outside
CreateRecommendationHandler (EPIC-04) -- deliberately mirrors that
handler's shape (AIExecutionService injected directly, provider name from
composition, a "refuse to generate from nothing" gate before ever calling
AI) rather than inventing new AI-calling conventions.
"""

from __future__ import annotations

from app.application.ai.ports.ai_budget_port import AIBudgetPort
from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_commands import GenerateSequenceContentCommand
from app.application.sequence.sequence_mapper import SequenceMapper
from app.application.sequence.services.touch_content_prompt_builder import (
    LeadEvidenceContext,
    build_touch_prompt,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.lead.entities.lead import Lead
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.identifiers.sequence_id import SequenceId
from app.infrastructure.ai.composition import default_model_for_provider


class GenerateSequenceContentHandler:
    """AI-generate content for every touch in a Sequence, grounded in the
    Lead's real evidence -- each touch takes a different angle (opener /
    proof point(s) / breakup) based purely on its position.

    Requires the Sequence to still be Draft -- regenerating content on an
    already-active/completed/stopped sequence would be confusing, and
    matches Sequence.start()'s own Draft-only gate in spirit.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        ai_execution_service: AIExecutionService,
        budget_port: AIBudgetPort,
        ai_provider_name: str = "gemini",
    ) -> None:
        self._unit_of_work = unit_of_work
        self._ai_execution_service = ai_execution_service
        self._budget_port = budget_port
        self._ai_provider_name = ai_provider_name

    async def handle(self, command: GenerateSequenceContentCommand) -> SequenceResponseDTO:
        sequence_id = SequenceId(command.sequence_id)

        async with self._unit_of_work:
            sequence = await self._unit_of_work.sequence_repository.get_by_id(sequence_id)
            if sequence is None:
                raise NotFoundException(
                    message="Sequence not found.",
                    details={"sequence_id": command.sequence_id},
                )

            if sequence.status != SequenceStatus.DRAFT:
                raise ConflictException(
                    message="Sequence must be in Draft status to generate content.",
                    details={"sequence_id": command.sequence_id, "status": sequence.status.value},
                )

            lead = await self._unit_of_work.lead_repository.get_by_id(sequence.lead_id)
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": str(sequence.lead_id)},
                )

            evidence = await self._gather_evidence(lead)

        if not evidence.has_meaningful_content():
            raise ValidationException(
                message=(
                    "This Lead has no captured evidence (notes, signals, or a "
                    "Discovery/Assessment/Recommendation) to ground touch content "
                    "in. Add real evidence before generating content."
                ),
                details={"lead_id": str(sequence.lead_id)},
            )

        # One pre-flight batch check for the whole run, same pattern as
        # SearchCompaniesHandler -- fail once, clearly, before spending
        # any of the len(touches) calls this will make.
        await self._budget_port.ensure_batch_fits(self._ai_provider_name, len(sequence.touches))

        # AI calls happen outside the DB transaction -- no need to hold a
        # session open across N external network calls.
        await self._generate_all_touches(sequence, evidence)

        async with self._unit_of_work:
            await self._unit_of_work.sequence_repository.update(sequence)
            await self._unit_of_work.commit()

        return SequenceMapper.to_response(sequence)

    async def _gather_evidence(self, lead: Lead) -> LeadEvidenceContext:
        discovery = await self._unit_of_work.discovery_repository.get_by_lead(lead.id)
        assessment = await self._unit_of_work.assessment_repository.get_by_lead_id(lead.id)
        recommendation = None
        if assessment is not None:
            recommendation = await self._unit_of_work.recommendation_repository.get_by_assessment_id(
                assessment.id,
            )

        return LeadEvidenceContext(
            notes=lead.notes,
            evidence_signals=lead.evidence_signals,
            discovery_problem_statement=discovery.problem_statement if discovery else None,
            discovery_business_impact=discovery.business_impact if discovery else None,
            assessment_summary=assessment.summary if assessment else None,
            recommendation_executive_summary=(recommendation.executive_summary if recommendation else None),
        )

    async def _generate_all_touches(self, sequence: Sequence, evidence: LeadEvidenceContext) -> None:
        total = len(sequence.touches)
        prior_touches: list[tuple[str, str]] = []
        model_name = default_model_for_provider(self._ai_provider_name)

        for index, touch in enumerate(sequence.touches):
            prompt, angle = build_touch_prompt(index, total, touch.channel, evidence, prior_touches)

            response = await self._ai_execution_service.execute(
                AIRequest(
                    provider=ProviderName(self._ai_provider_name),
                    model=ModelName(model_name),
                    prompt=Prompt(prompt),
                    temperature=Temperature(0.7),
                    max_tokens=MaxTokens(400),
                )
            )

            content = response.content.strip()
            sequence.set_touch_content(index, content)
            prior_touches.append((angle, content))
