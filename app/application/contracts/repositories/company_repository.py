"""
Company repository contract.

Architecture Freeze v5.0
Defines the application-facing persistence contract for Company.
"""
from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.company.entities.company import Company
from app.domain.company.identifiers.company_id import CompanyId


class CompanyRepository(Repository[Company, CompanyId]):
    """Repository contract for Company aggregates."""

    @abstractmethod
    async def find_by_name(self, name: str) -> Company | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[Company]:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        search_text: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Company]:
        raise NotImplementedError
