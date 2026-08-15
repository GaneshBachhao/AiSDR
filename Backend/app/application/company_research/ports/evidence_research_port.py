"""
Application port for gathering public-web evidence about a verified candidate.

This is the third and final external boundary in the research pipeline
(discover -> verify identity -> gather evidence). It only runs for
candidates that have already passed the deterministic gate and identity
verification, keeping expensive deep research downstream of the cheap
checks.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import EvidenceItem
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


class EvidenceResearchPort(ABC):
    """Application port for collecting buying-signal evidence about a company."""

    @abstractmethod
    async def gather(
        self,
        candidate: CompanyCandidate,
        identity: IdentityVerificationResult,
        request: CompanyResearchRequest,
    ) -> list[EvidenceItem]:
        """Return public-web evidence items relevant to the requested services/period."""
        raise NotImplementedError
