"""
Assessment repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.discovery.identifiers.discovery_id import (
    DiscoveryId,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class AssessmentRepository(
    Repository[
        Assessment,
        AssessmentId,
    ],
):
    """
    Contract for Assessment persistence.

    Generic CRUD operations are inherited from Repository.
    """

    @abstractmethod
    async def get_by_lead_id(
        self,
        lead_id: LeadId,
    ) -> Assessment | None:
        """
        Returns the assessment associated with a lead.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_discovery(
        self,
        discovery_id: DiscoveryId,
    ) -> Assessment | None:
        """
        Returns the assessment associated with a discovery, if any.
        """
        raise NotImplementedError
