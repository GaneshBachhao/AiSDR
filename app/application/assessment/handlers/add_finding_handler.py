from __future__ import annotations

from app.application.assessment.commands.add_finding import (
    AddFindingCommand,
)
from app.application.assessment.dto.finding_dto import (
    FindingDTO,
)
from app.application.assessment.mappers.finding_mapper import (
    FindingMapper,
)
from app.application.assessment.validators.add_finding_validator import (
    AddFindingValidator,
)
from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.domain.assessment.entities.finding import (
    Finding,
)
from app.domain.assessment.enums.finding_type import (
    FindingType,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository,
)


class AddFindingHandler:
    """
    Handles AddFindingCommand.
    """

    def __init__(
        self,
        repository: AssessmentRepository,
        validator: AddFindingValidator,
        mapper: FindingMapper,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: AddFindingCommand,
    ) -> FindingDTO:
        """
        Add a finding to an assessment.
        """

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValidationException(
                validation.errors,
            )

        assessment = await self._repository.get_by_id(
            AssessmentId(
                command.assessment_id,
            ),
        )

        if assessment is None:
            raise ValueError(
                "Assessment not found."
            )

        finding = Finding(
            title=command.title,
            description=command.description,
            finding_type=FindingType[
                command.finding_type.upper()
            ],
            severity=command.severity,
            recommendation_hint=command.recommendation_hint,
        )

        assessment.add_finding(
            finding,
        )

        await self._repository.save(
            assessment,
        )

        return self._mapper.to_dto(
            finding,
        )