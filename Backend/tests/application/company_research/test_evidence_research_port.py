import pytest

from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import EvidenceItem
from app.application.company_research.ports.evidence_research_port import (
    EvidenceResearchPort,
)
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationResult,
)
from app.domain.company_research.entities.candidate import CompanyCandidate


class FakeEvidenceResearchAdapter(EvidenceResearchPort):
    async def gather(self, candidate, identity, request):
        return [
            EvidenceItem(
                title="Acme is hiring",
                url="https://acme.example/careers",
                snippet="Acme is hiring cloud engineers.",
                evidence_date=None,
            )
        ]


def test_evidence_research_port_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        EvidenceResearchPort()  # type: ignore[abstract]


@pytest.mark.asyncio
async def test_fake_evidence_adapter_satisfies_port_contract():
    adapter: EvidenceResearchPort = FakeEvidenceResearchAdapter()
    candidate = CompanyCandidate(
        company_name="Acme",
        website="https://acme.example",
        title="Acme",
        content="",
        source_url="https://acme.example",
    )
    identity = IdentityVerificationResult(
        verified_website="https://acme.example",
        confidence="HIGH",
        parent_company=None,
        reason="matched",
    )
    request = CompanyResearchRequest(geography="India")
    evidence = await adapter.gather(candidate, identity, request)
    assert evidence[0].title == "Acme is hiring"
