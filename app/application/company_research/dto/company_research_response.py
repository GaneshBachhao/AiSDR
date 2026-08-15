from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class EvidenceItem(BaseModel):
    """A public source used to support a research observation.

    ``signal_scope`` distinguishes evidence that plausibly refers to the
    named company ("company_specific") from evidence that only discusses
    its industry/sector in general ("industry_general") -- see
    docs/pamacore_aisdr_summary.md §3. Defaults to the conservative value
    so evidence of unknown scope (e.g. constructed without classification)
    is never mistaken for company-specific proof. ``evidence_date`` is when
    the source was published; ``observed_date`` is when Pamacore captured it.
    """

    title: str
    url: HttpUrl
    snippet: str | None = None
    evidence_date: str | None = None
    observed_date: str | None = None
    signal_scope: Literal["company_specific", "industry_general"] = "industry_general"


class DiscoveredContact(BaseModel):
    """A public-web-discovered person at a researched company.

    Best-effort, sourced from a public profile page (e.g. LinkedIn) --
    never fabricated. ``role_title`` is the title observed on the source
    page, which may differ from ``CompanySearchResult.decision_maker_role``
    (the *targeted* role derived from the catalog match). ``email`` is a
    verified address, when one is actually known -- public LinkedIn-profile
    discovery never populates it; the field exists so a future real
    email-enrichment source (EPIC-17) has somewhere to put one without
    another DTO change. ``PromoteCandidateToLeadHandler`` (EPIC-06) requires
    ``email`` to be set before it will create a CRM Contact/Lead -- it never
    guesses one, per this module's never-fabricate discipline.
    """

    name: str
    role_title: str | None = None
    linkedin_url: HttpUrl | None = None
    source_url: HttpUrl | None = None
    email: str | None = None


class DiscoverySourceMetadata(BaseModel):
    """Dynamic metadata captured from a discovery/directory source at run time."""

    source_type: str = "discovery_directory"
    source_title: str
    source_url: HttpUrl
    discovered_record_count: int | None = Field(default=None, ge=0)
    metadata_observed_at: str | None = None


class CompanySearchResult(BaseModel):
    """Research result.

    Not persisted as CRM data by default. Set
    ``CompanyResearchRequest.persist_as_companies`` to also resolve/create a
    real CRM Company record per qualified result -- when that happens,
    ``persisted_company_id`` is populated. The same flag additionally
    attempts a Contact + Lead (``persisted_contact_id``/``persisted_lead_id``)
    once a ``discovered_contacts`` entry has a verified ``email`` -- until a
    real email-enrichment source exists (EPIC-17), that's rare, and
    ``lead_creation_skipped_reason`` explains why no Lead was created rather
    than leaving the gap silent.
    """

    company_name: str
    industry: str | None = None
    industry_match: bool = True
    industry_match_reason: str | None = None
    location: str | None = None
    website: HttpUrl | None = None
    company_size: str | None = None
    employee_count: int | None = Field(default=None, ge=0)
    parent_company: str | None = None
    icp_match: bool = True
    icp_match_reason: str | None = None
    business_description: str | None = None
    opportunity_type: list[str] = Field(default_factory=list)
    evidence_of_need: str
    evidence_classification: str
    business_problem_hypothesis: str
    recommended_solution: list[str] = Field(default_factory=list)
    expected_business_impact: str
    trigger_event: str | None = None
    evidence_date: str | None = None
    decision_maker_role: str | None = None
    decision_maker_name: str | None = None
    public_contact_channel: str | None = None
    discovered_contacts: list[DiscoveredContact] = Field(default_factory=list)
    discovery_metadata: list[DiscoverySourceMetadata] = Field(default_factory=list)
    qualification_score: int = Field(ge=0, le=100)
    priority_tier: str
    recommended_outreach_angle: str
    suggested_first_message: str
    sources: list[EvidenceItem] = Field(default_factory=list)
    confidence_level: str
    source: str = "public_web_research"
    persisted_company_id: str | None = None
    persisted_contact_id: str | None = None
    persisted_lead_id: str | None = None
    lead_creation_skipped_reason: str | None = None


class CandidateResearchFailure(BaseModel):
    """A candidate whose research pipeline step raised unexpectedly.

    Deliberately distinct from a candidate simply not appearing in
    ``CompanyResearchBatchResult.results`` -- that still happens whenever a
    candidate is checked and legitimately doesn't qualify (wrong industry,
    unverifiable identity, ...), which is not an error. This DTO exists only
    for the other case: an identity-verification or evidence-gathering call
    raised (a network error, a provider outage, ...) before the candidate
    could be checked at all. Carries the original candidate's discovery
    fields so it can be retried via ``POST /company-research/retry`` without
    paying for a fresh discovery pass.
    """

    company_name: str
    website: HttpUrl | None = None
    title: str
    content: str
    source_url: str
    discovery_metadata: list[DiscoverySourceMetadata] = Field(default_factory=list)
    failed_step: str
    error_message: str
    is_resumable: bool = True


class CompanyResearchBatchResult(BaseModel):
    """Envelope response for ``POST /company-research/search``.

    Splits genuinely-qualified results from candidates whose research
    pipeline crashed before a qualification decision could even be made --
    see ``CandidateResearchFailure``. A candidate that was checked and
    simply didn't qualify appears in neither list, same as before this
    envelope existed.
    """

    results: list[CompanySearchResult] = Field(default_factory=list)
    failures: list[CandidateResearchFailure] = Field(default_factory=list)
