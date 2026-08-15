"""
Application port for company identity verification.

This is the contract that fixes the parent/subsidiary and unrelated-domain
contamination defect (e.g. a candidate named "Lathangi Motors Private
Limited" must never be resolved to "tatamotors.com" on the strength of the
generic shared word "motors"). Implemented in Phase 2; the port is defined
now so CompanyCandidate consumers can be written against a stable contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, HttpUrl

from app.domain.company_research.entities.candidate import CompanyCandidate


class IdentityVerificationResult(BaseModel):
    """Outcome of verifying a candidate's identity and official website.

    ``verified_website`` is populated only when there is strong evidence the
    candidate actually owns/operates that domain. Absence of strong evidence
    must resolve to ``verified_website=None`` and ``confidence="LOW"`` rather
    than falling back to an unverified guess.
    """

    verified_website: HttpUrl | None = None
    confidence: str = Field(pattern="^(HIGH|MEDIUM|LOW)$")
    parent_company: str | None = None
    reason: str


class IdentityVerificationPort(ABC):
    """Application port for verifying a company candidate's official identity."""

    @abstractmethod
    async def verify(
        self,
        candidate: CompanyCandidate,
    ) -> IdentityVerificationResult:
        """Verify the candidate's identity and, where possible, official website.

        Must never assume a domain is correct merely because it appeared in
        discovery search results.
        """
        raise NotImplementedError
