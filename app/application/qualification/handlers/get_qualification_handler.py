"""Get Qualification application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.qualification.dto.qualification_response import GetQualificationResponseDTO
from app.application.qualification.qualification_mapper import QualificationMapper
from app.application.qualification.qualification_queries import GetQualificationQuery
from app.domain.qualification.identifiers.qualification_id import QualificationId


class GetQualificationHandler:
    """Retrieve a Qualification by identifier."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, query: GetQualificationQuery) -> GetQualificationResponseDTO:
        try:
            qualification_id = QualificationId(query.qualification_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid qualification id.",
                details={"qualification_id": query.qualification_id},
            ) from exc

        async with self._unit_of_work:
            qualification = await self._unit_of_work.qualification_repository.get_by_id(
                qualification_id,
            )

            if qualification is None:
                raise NotFoundException(
                    message="Qualification not found.",
                    details={"qualification_id": query.qualification_id},
                )

        return QualificationMapper.to_get_response(qualification)
