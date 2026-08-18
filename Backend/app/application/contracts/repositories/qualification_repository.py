"""
Qualification repository contract.

Architecture Freeze v5.0
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)
from app.domain.qualification.entities.qualification import (
    Qualification,
)
from app.domain.qualification.identifiers.qualification_id import (
    QualificationId,
)


class QualificationRepository(
    Repository[Qualification, QualificationId],
):
    """
    Application-layer repository contract for Qualification.
    """

    @abstractmethod
    async def get_by_lead_id(
        self,
        lead_id: LeadId,
    ) -> Qualification | None:
        """
        Retrieve the qualification associated with a lead.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_assessment_id(
        self,
        assessment_id: AssessmentId,
    ) -> Qualification | None:
        """
        Retrieve the qualification associated with an assessment.
        """
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Qualification]:
        """
        Retrieve qualifications using pagination.
        """
        raise NotImplementedError
