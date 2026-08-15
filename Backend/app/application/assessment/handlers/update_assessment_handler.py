"""
Update Assessment handler.
"""
from __future__ import annotations

from app.application.assessment.assessment_commands import UpdateAssessmentCommand
from app.application.assessment.assessment_mapper import AssessmentMapper
from app.application.assessment.assessment_validator import AssessmentValidator
from app.application.assessment.dto.assessment_response import UpdateAssessmentResponseDTO
from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.assessment.value_objects.assessment_score import AssessmentScore


class UpdateAssessmentHandler:
    """Handle Assessment updates."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: UpdateAssessmentCommand) -> UpdateAssessmentResponseDTO:
        validation = AssessmentValidator.validate_update(command)
        if validation.has_errors():
            raise ValueError(validation.error_messages())

        async with self._unit_of_work:
            assessment = await self._unit_of_work.assessment_repository.get_by_id(
                AssessmentId(command.assessment_id),
            )
            if assessment is None:
                raise NotFoundException(
                    message="Assessment not found.",
                    details={"assessment_id": command.assessment_id},
                )

            if command.summary is not None:
                assessment.summary = command.summary

            if command.maturity_level is not None:
                assessment.update_maturity(_to_maturity_level(command.maturity_level))

            if command.readiness_score is not None:
                assessment.update_score(
                    AssessmentScore(overall_score=command.readiness_score),
                )

            assessment.update_analysis(
                strengths=command.strengths,
                weaknesses=command.weaknesses,
                opportunities=command.opportunities,
                risks=command.risks,
            )

            await self._unit_of_work.assessment_repository.update(assessment)
            await self._unit_of_work.commit()

        return AssessmentMapper.to_update_response(assessment)


def _to_maturity_level(value: str) -> MaturityLevel:
    """Convert canonical and common maturity labels to MaturityLevel."""
    normalized = value.strip()
    if not normalized:
        raise ValueError("Maturity level cannot be empty.")

    try:
        return MaturityLevel(normalized)
    except ValueError:
        key = normalized.upper().replace("-", "_").replace(" ", "_")
        aliases = {
            "BEGINNER": MaturityLevel.INITIAL,
            "EMERGING": MaturityLevel.DEVELOPING,
            "INTERMEDIATE": MaturityLevel.DEFINED,
            "ADVANCED": MaturityLevel.MANAGED,
            "MATURE": MaturityLevel.OPTIMIZED,
        }
        if key in aliases:
            return aliases[key]
        try:
            return MaturityLevel[key]
        except KeyError as exc:
            raise ValueError(f"Invalid maturity level: {value!r}") from exc
