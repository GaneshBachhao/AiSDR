"""
Lead repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.lead.entities.lead import (
    Lead,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class LeadRepository(
    Repository[
        Lead,
        LeadId,
    ],
):
    """
    Contract for Lead persistence.

    Feature-specific queries should be added here.
    Generic CRUD operations are inherited from Repository.
    """

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> Lead | None:
        """
        Returns a lead by email address.
        """
        raise NotImplementedError