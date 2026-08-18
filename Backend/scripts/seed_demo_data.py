"""
Seed representative demo data across the whole Company -> Contact -> Lead
-> Discovery -> Assessment -> Qualification -> Recommendation pipeline,
without calling Gemini or Tavily.

The dev database otherwise only accumulates whatever a developer happened
to create by hand while testing one feature at a time -- sparse, single
records with no variety of status/lifecycle stage. This script builds a
handful of complete, realistic-looking demo chains that intentionally
stop at *different* pipeline stages (a bare new Lead, a Lead mid-Discovery,
a fully Qualified prospect with no Recommendation yet, a Recommendation
sitting in Draft, another already Under Review) so every list/detail
screen and every status badge has something real to show, and so the
Submit/Approve actions on a Recommendation have a live Draft/Under-Review
record to exercise instead of needing a real AI-generated one.

Every entity is constructed directly via the domain layer and persisted
through the same UnitOfWork/repository path the application itself uses --
exactly like Backend/scripts/create_user.py does for User. No HTTP calls,
no AI/search provider calls.

Usage (from Backend/, with the venv active):

    python -m scripts.seed_demo_data

Idempotent per company: each demo chain is looked up by its Company name
first (CompanyRepository.find_by_name) and skipped entirely if it already
exists, so re-running this script is always safe and never creates
duplicates or silently overwrites data a developer may have since edited
by hand through the app.

Two known, deliberate omissions -- not bugs in this script, but two
pre-existing gaps in how Assessment/Recommendation persist today (see
app/infrastructure/persistence/mappers/assessment_mapper.py and
recommendation_mapper.py): Assessment's per-dimension score breakdown and
its Finding/Evidence/Opportunity entities have no backing columns at all,
and Recommendation's roadmap_phases has none either -- whatever is set on
those fields is silently dropped on save. Building them here would produce
seed data that looks richer in this script than it ever appears in the
app, so this script only sets the fields that actually round-trip.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.enums.assessment_status import AssessmentStatus
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.value_objects.assessment_score import AssessmentScore
from app.domain.company.entities.company import Company
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry
from app.domain.contact.entities.contact import Contact
from app.domain.contact.value_objects.email import Email
from app.domain.discovery.entities.discovery import Discovery
from app.domain.discovery.enums.discovery_status import DiscoveryStatus
from app.domain.lead.entities.lead import Lead
from app.domain.lead.enums.lead_source import LeadSource
from app.domain.lead.enums.lead_status import LeadStatus
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.qualification.entities.qualification import Qualification
from app.domain.qualification.enums.qualification_status import QualificationStatus
from app.domain.qualification.value_objects.qualification_score import QualificationScore
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.implementation_priority import ImplementationPriority
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus
from app.domain.recommendation.enums.solution_type import SolutionType
from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.session import get_session_manager
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


async def _seed_meridian(uow: SqlAlchemyUnitOfWork) -> bool:
    """Full pipeline through a Draft Recommendation -- try "Submit for Review"."""
    if await uow.company_repository.find_by_name("Meridian Logistics Group"):
        return False

    company = Company(
        name="Meridian Logistics Group",
        website="https://meridianlogisticsgroup.example",
        industry=Industry.LOGISTICS,
        company_size=CompanySize.MEDIUM,
        employee_count=180,
        country="US",
        state="TX",
        city="Dallas",
    )
    await uow.company_repository.add(company)

    contact = Contact(
        first_name="Priya",
        last_name="Nandakumar",
        email=Email("priya.nandakumar@meridianlogisticsgroup.example"),
        phone="+1-214-555-0142",
        job_title="VP of Operations",
        company_id=company.id,
    )
    await uow.contact_repository.add(contact)

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id,
        source=LeadSource.REFERRAL,
        status=LeadStatus.QUALIFIED,
        score=LeadScore(82),
        notes="Warm referral from an existing Pamacore client in the same 3PL network.",
    )
    await uow.lead_repository.add(lead)

    discovery = Discovery(
        lead_id=lead.id,
        problem_statement=(
            "Dispatch coordinators manually re-key shipment data between the TMS "
            "and the customer-facing tracking portal, several times a day per lane."
        ),
        current_solution="A shared spreadsheet plus manual email updates to customers.",
        business_impact=(
            "Estimated 12-15 hours/week of coordinator time lost to re-keying, "
            "and repeated customer complaints about stale tracking status."
        ),
        success_criteria="Tracking status updates automatically within 5 minutes of a TMS event.",
        status=DiscoveryStatus.COMPLETED,
    )
    await uow.discovery_repository.add(discovery)

    assessment = Assessment(
        discovery_id=discovery.id,
        status=AssessmentStatus.COMPLETED,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        score=AssessmentScore(overall_score=74.0),
        maturity_level=MaturityLevel.DEVELOPING,
        summary="Solid data foundation (both systems have APIs); the gap is process, not tooling.",
        strengths="Existing TMS and tracking portal both expose usable APIs.",
        weaknesses="No integration layer; all cross-system updates are manual today.",
        opportunities_summary="Automation could eliminate the re-keying step almost entirely.",
        risks="Coordinator team has limited technical bandwidth to support a rollout.",
    )
    await uow.assessment_repository.add(assessment)

    qualification = Qualification(lead_id=lead.id, assessment_id=assessment.id)
    qualification.update_score(QualificationScore(81.0))
    qualification.update_status(QualificationStatus.QUALIFIED)
    qualification.update_recommendation(
        "Strong automation fit: clear process gap, existing API surface on both systems, "
        "engaged economic buyer (VP Operations)."
    )
    await uow.qualification_repository.add(qualification)

    recommendation = Recommendation(
        assessment_id=assessment.id,
        status=RecommendationStatus.DRAFT,
        executive_summary="2 solution(s) proposed to close the TMS-to-portal data gap.",
    )
    recommendation.add_solution(
        Solution(
            title="TMS-to-Portal Sync Automation",
            description="Event-driven sync that pushes TMS shipment updates to the customer portal.",
            solution_type=SolutionType.AUTOMATION,
            priority=ImplementationPriority.CRITICAL,
            is_existing_offering=True,
        )
    )
    recommendation.add_solution(
        Solution(
            title="Dispatch Coordinator Copilot",
            description="A copilot that drafts customer status updates from TMS events for review.",
            solution_type=SolutionType.COPILOT,
            priority=ImplementationPriority.MEDIUM,
            is_existing_offering=False,
        )
    )
    await uow.recommendation_repository.add(recommendation)

    return True


async def _seed_brightline(uow: SqlAlchemyUnitOfWork) -> bool:
    """Full pipeline through a Recommendation already Under Review -- try "Approve"."""
    if await uow.company_repository.find_by_name("Brightline Financial Services"):
        return False

    company = Company(
        name="Brightline Financial Services",
        website="https://brightlinefinancial.example",
        industry=Industry.FINANCIAL_SERVICES,
        company_size=CompanySize.MEDIUM,
        employee_count=220,
        country="US",
        state="IL",
        city="Chicago",
    )
    await uow.company_repository.add(company)

    contact = Contact(
        first_name="Marcus",
        last_name="Webb",
        email=Email("marcus.webb@brightlinefinancial.example"),
        phone="+1-312-555-0198",
        job_title="Director of Finance Operations",
        company_id=company.id,
    )
    await uow.contact_repository.add(contact)

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id,
        source=LeadSource.WEBSITE,
        status=LeadStatus.QUALIFIED,
        score=LeadScore(75),
        notes="Inbound from the AI readiness assessment landing page.",
    )
    await uow.lead_repository.add(lead)

    discovery = Discovery(
        lead_id=lead.id,
        problem_statement="Monthly close requires manually reconciling 6 source systems into one report.",
        current_solution="A finance analyst spends roughly a week each month building it manually.",
        business_impact="Close is consistently 3-4 business days later than the target date.",
        success_criteria="Reconciliation report generated automatically within 1 business day of close.",
        status=DiscoveryStatus.COMPLETED,
    )
    await uow.discovery_repository.add(discovery)

    assessment = Assessment(
        discovery_id=discovery.id,
        status=AssessmentStatus.COMPLETED,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        score=AssessmentScore(overall_score=68.0),
        maturity_level=MaturityLevel.INITIAL,
        summary="High manual-effort, well-bounded reporting problem -- a strong first automation candidate.",
        strengths="All 6 source systems already export structured data (CSV/API), nothing paper-based.",
        weaknesses="No prior automation experience on the finance team; will need change management.",
        opportunities_summary="A single automated pipeline would recover most of the lost week.",
        risks="Finance data is sensitive -- any solution needs a clear audit trail.",
    )
    await uow.assessment_repository.add(assessment)

    qualification = Qualification(lead_id=lead.id, assessment_id=assessment.id)
    qualification.update_score(QualificationScore(76.0))
    qualification.update_status(QualificationStatus.QUALIFIED)
    qualification.update_recommendation(
        "Well-scoped, high-effort-savings automation opportunity with a clearly engaged buyer."
    )
    await uow.qualification_repository.add(qualification)

    recommendation = Recommendation(
        assessment_id=assessment.id,
        status=RecommendationStatus.DRAFT,
        executive_summary="1 solution proposed to automate month-end reconciliation.",
    )
    recommendation.add_solution(
        Solution(
            title="Automated Financial Reconciliation Pipeline",
            description="Automates the monthly 6-system reconciliation into a single audited report.",
            solution_type=SolutionType.AUTOMATION,
            priority=ImplementationPriority.HIGH,
            is_existing_offering=True,
        )
    )
    # submit_for_review() requires at least one solution, matching the real
    # application-layer guard in SubmitRecommendationHandler -- calling the
    # same domain method here (not a script-only shortcut) keeps this
    # seed data reachable through the exact same invariant the API enforces.
    recommendation.submit_for_review()
    await uow.recommendation_repository.add(recommendation)

    return True


async def _seed_coastal(uow: SqlAlchemyUnitOfWork) -> bool:
    """Stops at Qualification -- no Recommendation yet, a realistic "still being worked" stage."""
    if await uow.company_repository.find_by_name("Coastal Retail Group"):
        return False

    company = Company(
        name="Coastal Retail Group",
        website="https://coastalretailgroup.example",
        industry=Industry.RETAIL,
        company_size=CompanySize.SMALL,
        employee_count=45,
        country="US",
        state="FL",
        city="Tampa",
    )
    await uow.company_repository.add(company)

    contact = Contact(
        first_name="Dana",
        last_name="Ferreira",
        email=Email("dana.ferreira@coastalretailgroup.example"),
        job_title="Store Operations Manager",
        company_id=company.id,
    )
    await uow.contact_repository.add(contact)

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id,
        source=LeadSource.EVENT,
        status=LeadStatus.CONTACTED,
        score=LeadScore(48),
        notes="Met at a regional retail operations conference; interested but budget not yet confirmed.",
    )
    await uow.lead_repository.add(lead)

    discovery = Discovery(
        lead_id=lead.id,
        problem_statement="Inventory counts drift out of sync across 4 store locations.",
        current_solution="Weekly manual stock counts phoned in to a central spreadsheet.",
        business_impact="Frequent stockouts on fast-moving items; unclear if this justifies AI tooling yet.",
        status=DiscoveryStatus.COMPLETED,
    )
    await uow.discovery_repository.add(discovery)

    assessment = Assessment(
        discovery_id=discovery.id,
        status=AssessmentStatus.COMPLETED,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        score=AssessmentScore(overall_score=41.0),
        maturity_level=MaturityLevel.INITIAL,
        summary="Real pain point, but scale and budget don't clearly support a custom build yet.",
        weaknesses="No existing systems to integrate with -- would need a POS/inventory platform first.",
        risks="Company size may be below the threshold where a bespoke solution pencils out.",
    )
    await uow.assessment_repository.add(assessment)

    qualification = Qualification(lead_id=lead.id, assessment_id=assessment.id)
    qualification.update_score(QualificationScore(38.0))
    qualification.update_status(QualificationStatus.NEEDS_NURTURING)
    qualification.update_recommendation(
        "Revisit once they've adopted a modern POS/inventory platform -- not enough system "
        "foundation to recommend a solution yet."
    )
    await uow.qualification_repository.add(qualification)

    return True


async def _seed_fenwick(uow: SqlAlchemyUnitOfWork) -> bool:
    """Stops mid-Discovery -- top-of-funnel, no Assessment started yet."""
    if await uow.company_repository.find_by_name("Fenwick Manufacturing Co."):
        return False

    company = Company(
        name="Fenwick Manufacturing Co.",
        website="https://fenwickmanufacturing.example",
        industry=Industry.MANUFACTURING,
        company_size=CompanySize.LARGE,
        employee_count=640,
        country="US",
        state="OH",
        city="Akron",
    )
    await uow.company_repository.add(company)

    contact = Contact(
        first_name="Robert",
        last_name="Ozawa",
        email=Email("robert.ozawa@fenwickmanufacturing.example"),
        phone="+1-330-555-0173",
        job_title="Plant Systems Manager",
        company_id=company.id,
    )
    await uow.contact_repository.add(contact)

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id,
        source=LeadSource.LINKEDIN,
        status=LeadStatus.CONTACTED,
        score=LeadScore(55),
        notes="Responded to outreach about predictive maintenance; first discovery call scheduled.",
    )
    await uow.lead_repository.add(lead)

    discovery = Discovery(
        lead_id=lead.id,
        problem_statement="Unplanned line downtime from equipment failures the team can't predict.",
        current_solution="Reactive maintenance -- repairs happen after a failure, not before.",
        status=DiscoveryStatus.IN_PROGRESS,
    )
    await uow.discovery_repository.add(discovery)

    return True


async def _seed_northgate(uow: SqlAlchemyUnitOfWork) -> bool:
    """A bare new Lead -- freshest possible top-of-funnel record, nothing else started."""
    if await uow.company_repository.find_by_name("Northgate Consulting Partners"):
        return False

    company = Company(
        name="Northgate Consulting Partners",
        website="https://northgateconsulting.example",
        industry=Industry.INFORMATION_TECHNOLOGY,
        company_size=CompanySize.SMALL,
        employee_count=30,
        country="US",
        state="WA",
        city="Seattle",
    )
    await uow.company_repository.add(company)

    contact = Contact(
        first_name="Elena",
        last_name="Kowalski",
        email=Email("elena.kowalski@northgateconsulting.example"),
        job_title="Managing Partner",
        company_id=company.id,
    )
    await uow.contact_repository.add(contact)

    lead = Lead(
        company_id=company.id,
        contact_id=contact.id,
        source=LeadSource.OTHER,
        status=LeadStatus.NEW,
        score=LeadScore(20),
        notes="Just added; not yet worked.",
    )
    await uow.lead_repository.add(lead)

    return True


async def main() -> None:
    settings = DatabaseSettings()
    manager = get_session_manager(settings)
    session = manager.create_session()

    seeders = [
        ("Meridian Logistics Group", _seed_meridian),
        ("Brightline Financial Services", _seed_brightline),
        ("Coastal Retail Group", _seed_coastal),
        ("Fenwick Manufacturing Co.", _seed_fenwick),
        ("Northgate Consulting Partners", _seed_northgate),
    ]

    try:
        for label, seed in seeders:
            uow = SqlAlchemyUnitOfWork(session=session)
            async with uow:
                created = await seed(uow)
                if created:
                    await uow.commit()
                    print(f"Seeded: {label}")
                else:
                    print(f"Already exists, skipped: {label}")
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
