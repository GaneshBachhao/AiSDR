"""Update Qualification application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.qualification.dto.qualification_response import UpdateQualificationResponseDTO
from app.application.qualification.qualification_commands import UpdateQualificationCommand
from app.application.qualification.qualification_mapper import QualificationMapper
from app.application.qualification.qualification_validator import QualificationValidator
from app.domain.qualification.identifiers.qualification_id import QualificationId
from app.domain.qualification.value_objects.qualification_score import QualificationScore


class UpdateQualificationHandler:
    """Update an existing Qualification."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: UpdateQualificationCommand) -> UpdateQualificationResponseDTO:
        validation = QualificationValidator.validate_update(command)
        if validation.has_errors():
            raise ValidationException(
                message="Qualification validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        qualification_id = QualificationId(command.qualification_id)

        async with self._unit_of_work:
            qualification = await self._unit_of_work.qualification_repository.get_by_id(
                qualification_id,
            )

            if qualification is None:
                raise NotFoundException(
                    message="Qualification not found.",
                    details={"qualification_id": command.qualification_id},
                )

            if command.status is not None:
                status = QualificationValidator.normalize_status(command.status)
                # Validation already guarantees this is non-null.
                qualification.update_status(status)  # type: ignore[arg-type]

            if command.score is not None:
                qualification.update_score(QualificationScore(command.score))

            if command.recommendation is not None:
                qualification.update_recommendation(command.recommendation)

            await self._unit_of_work.qualification_repository.update(qualification)
            await self._unit_of_work.commit()

        return QualificationMapper.to_update_response(qualification)
