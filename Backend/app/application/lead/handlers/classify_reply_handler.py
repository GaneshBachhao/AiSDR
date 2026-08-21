"""
Classify Reply application handler (EPIC-10.1/10.3).

Classifies an operator-supplied reply text into one of six categories and
applies the mapped Lead.status/score change plus stops any currently-Active
Sequence for that Lead -- except OUT_OF_OFFICE, an auto-reply rather than a
real reply from the person, which changes nothing.

The port abstracts the AI call away (same shape as
``IdentityVerificationPort``/``SearchCompaniesHandler``) -- this handler
never touches ``AIExecutionService`` directly.
"""

from __future__ import annotations

from app.application.ai.ports.ai_budget_port import AIBudgetPort
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.lead.dto.reply_classification_responses import (
    ReplyClassificationResponseDTO,
)
from app.application.lead.lead_commands import ClassifyReplyCommand
from app.application.lead.ports.reply_classification_port import ReplyClassificationPort
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.enums.reply_classification import ReplyClassification
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.sequence.enums.sequence_status import SequenceStatus

# Judgment-call mapping (not spec'd anywhere) -- see the EPIC-10.1/10.3 plan
# for the reasoning behind each choice, most notably why OUT_OF_OFFICE is the
# one classification that changes nothing.
_STATUS_BY_CLASSIFICATION: dict[ReplyClassification, LeadStatus | None] = {
    ReplyClassification.INTERESTED: LeadStatus.QUALIFIED,
    ReplyClassification.NOT_NOW: LeadStatus.CONTACTED,
    ReplyClassification.OBJECTION: LeadStatus.CONTACTED,
    ReplyClassification.UNSUBSCRIBE: LeadStatus.DISQUALIFIED,
    ReplyClassification.WRONG_PERSON: LeadStatus.DISQUALIFIED,
    ReplyClassification.OUT_OF_OFFICE: None,
}

_SCORE_DELTA_BY_CLASSIFICATION: dict[ReplyClassification, int] = {
    ReplyClassification.INTERESTED: 20,
    ReplyClassification.NOT_NOW: -5,
}


class ClassifyReplyHandler:
    """Classify a reply and apply it to the Lead and any Active Sequences."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        budget_port: AIBudgetPort,
        reply_classification_port: ReplyClassificationPort,
        ai_provider_name: str = "gemini",
    ) -> None:
        self._unit_of_work = unit_of_work
        self._budget_port = budget_port
        self._reply_classification_port = reply_classification_port
        self._ai_provider_name = ai_provider_name

    async def handle(self, command: ClassifyReplyCommand) -> ReplyClassificationResponseDTO:
        lead_id = LeadId(command.lead_id)

        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(lead_id)
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

        await self._budget_port.ensure_batch_fits(self._ai_provider_name, 1)
        result = await self._reply_classification_port.classify(command.reply_text)

        async with self._unit_of_work:
            lead = await self._unit_of_work.lead_repository.get_by_id(lead_id)
            if lead is None:
                raise NotFoundException(
                    message="Lead not found.",
                    details={"lead_id": command.lead_id},
                )

            new_status = _STATUS_BY_CLASSIFICATION[result.classification]
            if new_status is not None:
                lead.update_status(new_status)

            score_delta = _SCORE_DELTA_BY_CLASSIFICATION.get(result.classification)
            if score_delta is not None:
                new_value = max(0, min(100, lead.score.value + score_delta))
                lead.update_score(LeadScore(new_value))

            await self._unit_of_work.lead_repository.update(lead)

            stopped_sequence_ids: list[str] = []
            if result.classification != ReplyClassification.OUT_OF_OFFICE:
                sequences = await self._unit_of_work.sequence_repository.list_by_lead(lead_id)
                for sequence in sequences:
                    if sequence.status != SequenceStatus.ACTIVE:
                        continue
                    sequence.record_reply()
                    await self._unit_of_work.sequence_repository.update(sequence)
                    stopped_sequence_ids.append(str(sequence.id))

            await self._unit_of_work.commit()

        return ReplyClassificationResponseDTO(
            classification=result.classification.value,
            confidence=result.confidence,
            lead_status=lead.status.value,
            lead_score=lead.score.value,
            sequences_stopped=stopped_sequence_ids,
        )
