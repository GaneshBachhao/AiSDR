# app/domain/lead/repositories/lead_repository.py

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId


class LeadRepository(ABC):
    """
    Repository contract for the Lead aggregate.

    This contract belongs to the Domain layer.

    Repository implementations are provided by the
    Infrastructure layer.
    """

    @abstractmethod
    async def save(
        self,
        lead: Lead,
    ) -> Lead:
        """
        Persist a lead.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        lead_id: LeadId,
    ) -> Lead | None:
        """
        Retrieve a lead by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(
        self,
        email: str,
    ) -> Lead | None:
        """
        Retrieve a lead by email address.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        lead_id: LeadId,
    ) -> bool:
        """
        Determine whether a lead exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        lead: Lead,
    ) -> None:
        """
        Remove a lead.
        """
        raise NotImplementedError