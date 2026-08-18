"""
Contact repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.contact.entities.contact import (
    Contact,
)
from app.domain.contact.identifiers.contact_id import (
    ContactId,
)


class ContactRepository(
    Repository[
        Contact,
        ContactId,
    ],
):
    """
    Repository contract for Contact aggregates.

    Inherits generic CRUD operations from Repository and defines
    Contact-specific query operations.
    """

    @abstractmethod
    async def find_by_email(
        self,
        email: str,
    ) -> Contact | None:
        """
        Retrieve a contact by email.
        """

        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contact]:
        """
        Retrieve contacts using pagination.
        """

        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Contact]:
        """
        Search contacts.
        """

        raise NotImplementedError
