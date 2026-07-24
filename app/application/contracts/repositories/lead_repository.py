from abc import ABC, abstractmethod

from app.domain.lead.entities.lead import Lead
from app.domain.lead.value_objects.lead_id import LeadId


class LeadRepository(ABC):
    """
    Lead persistence contract.
    """

    @abstractmethod
    async def add(self, lead: Lead) -> None:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        lead_id: LeadId
    ) -> Lead | None:
        pass

    @abstractmethod
    async def update(
        self,
        lead: Lead
    ) -> None:
        pass