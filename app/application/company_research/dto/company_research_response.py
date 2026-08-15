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
    ``persisted_company_id`` is populated.
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
    discovery_metadata: list[DiscoverySourceMetadata] = Field(default_factory=list)
    qualification_score: int = Field(ge=0, le=100)
    priority_tier: str
    recommended_outreach_angle: str
    suggested_first_message: str
    sources: list[EvidenceItem] = Field(default_factory=list)
    confidence_level: str
    source: str = "public_web_research"
    persisted_company_id: str | None = None
