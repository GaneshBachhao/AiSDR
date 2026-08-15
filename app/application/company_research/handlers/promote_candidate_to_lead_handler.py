"""
Bridges a qualified, already-promoted-to-Company research result into a real
CRM Contact + Lead -- Track 1 Phase 6 (EPIC-06, "Lead creation bridge").

Only invoked (by ``SearchCompaniesHandler``) after
``PromoteCandidateToCompanyHandler`` has already resolved/created the
Company, and only when ``CompanyResearchRequest.persist_as_companies`` is
set -- same opt-in gate as company promotion, since this is the same
"materialize this research result as CRM data" decision, not a separate one.

Requires a verified ``DiscoveredContact.email`` before creating anything.
Public-web contact discovery (EPIC-05) never populates one -- LinkedIn
search results don't expose emails -- so in practice this is a no-op today.
That's deliberate: this project's contact/identity ports already treat
"no evidence" as a hard stop rather than a guess (see
``ContactDiscoveryPort``/``IdentityVerificationPort``), and ``Contact.email``
is a mandatory, validated CRM field a future send path would read --
guessing one there is a sharper foot-gun than the guesses this system
already refuses to make elsewhere. The bridge itself is real and tested; it
starts producing live Leads once a real email source (EPIC-17) exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.contact.contact_commands import CreateContactCommand
from app.application.contact.handlers.create_contact_handler import CreateContactHandler
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
    DiscoveredContact,
)
from app.application.lead.handlers.create_lead_handler import CreateLeadHandler
from app.application.lead.lead_commands import CreateLeadCommand
from app.domain.company.identifiers.company_id import CompanyId
from app.domain.contact.identifiers.contact_id import ContactId
from app.domain.lead.enums.lead_source import LeadSource


@dataclass(frozen=True, slots=True)
class LeadPromotionOutcome:
    """Result of attempting to promote one research result to Contact+Lead."""

    contact_id: str | None = None
    lead_id: str | None = None
    skipped_reason: str | None = None


class PromoteCandidateToLeadHandler:
    """Resolves or creates the CRM Contact + Lead for one research result."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        create_contact_handler: CreateContactHandler,
        create_lead_handler: CreateLeadHandler,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._create_contact_handler = create_contact_handler
        self._create_lead_handler = create_lead_handler

    async def handle(
        self, result: CompanySearchResult, company_id: str
    ) -> LeadPromotionOutcome:
        contact = next(
            (item for item in result.discovered_contacts if item.email), None
        )
        if contact is None:
            return LeadPromotionOutcome(
                skipped_reason="no_verified_email_found"
            )

        contact_id = await self._resolve_contact(contact, company_id)

        existing_leads = await self._unit_of_work.lead_repository.list(
            company_id=CompanyId(company_id),
            contact_id=ContactId(contact_id),
            limit=1,
        )
        if existing_leads:
            return LeadPromotionOutcome(
                contact_id=contact_id, lead_id=str(existing_leads[0].id.value)
            )

        lead_response = await self._create_lead_handler.handle(
            CreateLeadCommand(
                company_id=company_id,
                contact_id=contact_id,
                source=LeadSource.AI_RESEARCH.value,
                score=result.qualification_score,
                notes=self._build_notes(result),
            )
        )
        return LeadPromotionOutcome(contact_id=contact_id, lead_id=lead_response.id)

    async def _resolve_contact(
        self, contact: DiscoveredContact, company_id: str
    ) -> str:
        existing = await self._unit_of_work.contact_repository.find_by_email(
            contact.email
        )
        if existing is not None:
            return str(existing.id.value)

        first_name, last_name = self._split_name(contact.name)
        try:
            response = await self._create_contact_handler.handle(
                CreateContactCommand(
                    company_id=company_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=contact.email,
                    job_title=contact.role_title,
                    linkedin_url=(
                        str(contact.linkedin_url) if contact.linkedin_url else None
                    ),
                )
            )
            return response.id
        except ConflictException:
            existing = await self._unit_of_work.contact_repository.find_by_email(
                contact.email
            )
            if existing is not None:
                return str(existing.id.value)
            raise

    @staticmethod
    def _split_name(name: str) -> tuple[str, str]:
        parts = name.strip().split()
        if len(parts) >= 2:
            return parts[0], " ".join(parts[1:])
        return parts[0], parts[0]

    @staticmethod
    def _build_notes(result: CompanySearchResult) -> str:
        return (
            f"AI-research-sourced lead (score {result.qualification_score}, "
            f"{result.priority_tier}).\n"
            f"Hypothesis: {result.business_problem_hypothesis}\n"
            f"Evidence: {result.evidence_of_need}\n"
            f"Trigger event: {result.trigger_event or 'none observed'}"
        )
