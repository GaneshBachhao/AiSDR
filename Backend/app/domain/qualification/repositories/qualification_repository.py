"""
Qualification repository contract.
"""

from __future__ import annotations

from abc import abstractmethod

from app.domain.qualification.entities.qualification import (
    Qualification,
)
from app.domain.qualification.identifiers.qualification_id import (
    QualificationId,
)
from app.domain.shared.repositories.repository import (
    Repository,
)


class QualificationRepository(
    Repository[
        Qualification,
        QualificationId,
    ],
):
    """
    Repository contract for Qualification aggregate.
    """

    @abstractmethod
    async def add(
        self,
        qualification: Qualification,
    ) -> None:
        """
        Add a qualification.
        """

    @abstractmethod
    async def update(
        self,
        qualification: Qualification,
    ) -> None:
        """
        Update a qualification.
        """

    @abstractmethod
    async def delete(
        self,
        qualification: Qualification,
    ) -> None:
        """
        Delete a qualification.
        """

    @abstractmethod
    async def get_by_id(
        self,
        qualification_id: QualificationId,
    ) -> Qualification | None:
        """
        Retrieve a qualification by identifier.
        """

    @abstractmethod
    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Qualification]:
        """
        List qualifications.
        """