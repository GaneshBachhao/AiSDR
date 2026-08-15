import pytest
from pydantic import ValidationError

from app.application.company_research.ports.company_discovery_port import CompanyDiscoveryPort
from app.application.company_research.ports.contact_discovery_port import ContactDiscoveryPort
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationPort,
    IdentityVerificationResult,
)
from app.application.company_research.dto.company_research_request import (
    CompanyResearchRequest,
)
from app.application.company_research.dto.company_research_response import DiscoveredContact
from app.domain.company_research.entities.candidate import CompanyCandidate


class FakeCompanyDiscoveryAdapter(CompanyDiscoveryPort):
    async def discover(self, request: CompanyResearchRequest) -> list[CompanyCandidate]:
        return [
            CompanyCandidate(
                company_name="Acme Manufacturing",
                website="https://acme.example",
                title="Acme Manufacturing",
                content="",
                source_url="https://acme.example",
            )
        ]


class FakeIdentityVerificationAdapter(IdentityVerificationPort):
    async def verify(self, candidate: CompanyCandidate) -> IdentityVerificationResult:
        return IdentityVerificationResult(
            verified_website=None,
            confidence="LOW",
            parent_company=None,
            reason="official_website_not_verified",
        )


def test_company_discovery_port_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        CompanyDiscoveryPort()  # type: ignore[abstract]


def test_identity_verification_port_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        IdentityVerificationPort()  # type: ignore[abstract]


@pytest.mark.asyncio
async def test_fake_discovery_adapter_satisfies_port_contract():
    adapter: CompanyDiscoveryPort = FakeCompanyDiscoveryAdapter()
    request = CompanyResearchRequest(geography="India")
    candidates = await adapter.discover(request)
    assert candidates[0].company_name == "Acme Manufacturing"


@pytest.mark.asyncio
async def test_fake_identity_adapter_never_silently_defaults_to_high_confidence():
    adapter: IdentityVerificationPort = FakeIdentityVerificationAdapter()
    candidate = CompanyCandidate(
        company_name="Lathangi Motors Private Limited",
        website="https://tatamotors.com",
        title="Lathangi Motors",
        content="",
        source_url="https://tatamotors.com",
    )
    result = await adapter.verify(candidate)
    assert result.verified_website is None
    assert result.confidence == "LOW"


def test_identity_verification_result_rejects_unknown_confidence_value():
    with pytest.raises(ValidationError):
        IdentityVerificationResult(confidence="MAYBE", reason="x")


class FakeContactDiscoveryAdapter(ContactDiscoveryPort):
    async def discover(self, candidate, website, target_role):
        return [DiscoveredContact(name="Jane Doe", role_title=target_role)]


def test_contact_discovery_port_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        ContactDiscoveryPort()  # type: ignore[abstract]


@pytest.mark.asyncio
async def test_fake_contact_discovery_adapter_satisfies_port_contract():
    adapter: ContactDiscoveryPort = FakeContactDiscoveryAdapter()
    candidate = CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        title="Acme Manufacturing",
        content="",
        source_url="https://acme.example",
    )
    contacts = await adapter.discover(candidate, "https://acme.example", "COO / Operations Leader")
    assert contacts[0].name == "Jane Doe"
    assert contacts[0].role_title == "COO / Operations Leader"
