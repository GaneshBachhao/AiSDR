"""Lead repository contract."""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId


class LeadRepository(Repository[Lead, LeadId]):
    """Repository contract for Lead aggregates."""

    @abstractmethod
    async def list(
        self,
        company_id: CompanyId | None = None,
        contact_id: ContactId | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        """List Leads with optional Company/Contact filters."""
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        search_text: str,
        company_id: CompanyId | None = None,
        contact_id: ContactId | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Lead]:
        """Search Leads with optional relationship filters."""
        raise NotImplementedError
