# Pamacore / AiSDR — Opportunity Discovery Architecture & Implementation Plan

> This document replaces an earlier brainstorm draft. The vision and principles in that
> draft are sound and are preserved below (§1–§7). What it got wrong is the starting
> point: it was written without visibility into this codebase and assumed most of the
> downstream pipeline (Company, Contact, Lead, Discovery, Assessment, Recommendation)
> still needed to be built. **It already exists, is persisted, tested, and API-exposed.**
> §8 is a ground-truth correction of that assumption.
>
> The plan was then deliberately widened beyond "finish wiring the pipeline." §9
> onward takes a product/platform view: an AI SDR only matters if discovered
> opportunities turn into booked meetings, the system improves from real outcomes,
> and the humans using it trust what it hands them. Pipeline wiring is necessary
> plumbing; §10–§14 are where the product actually differentiates and where several
> of this session's own incidents (model deprecation, quota exhaustion, a stale env
> var) point directly at gaps worth closing early.

---

## 1. Product Context

Pamacore is not a "company search" system. It is an SMB-focused B2B **opportunity
discovery and qualification platform**. Company search is only the first stage of a
much larger chain:

```text
DOMAIN → COMPANY UNIVERSE → COMPANY → CONTACTS → SIGNALS → LEAD →
DISCOVERY → ASSESSMENT → RECOMMENDATION → OUTREACH
```

Target customers are primarily **SMB / mid-market organizations**, initially across
Manufacturing, Healthcare, Pharma, Biotech, Research, Logistics, Financial Services,
Construction, and Retail — with the architecture required to support adding further
domains (Energy, Telecom, Insurance, Education, Automotive, Professional Services, ...)
**without rewriting or destabilizing existing domains.**

The full journey:

```text
DOMAIN → COMPANY UNIVERSE → COMPANY DISCOVERY → ENTITY RESOLUTION →
COMPANY PROFILE → ICP QUALIFICATION → WEB/BUSINESS SIGNAL RESEARCH →
OPPORTUNITY DETECTION → CONTACT DISCOVERY → LEAD → DISCOVERY →
ASSESSMENT → RECOMMENDATION → OUTREACH → PIPELINE
```

Every later stage must be able to trace its reasoning back to evidence from the
previous stage. Never:

```text
SEARCH → LLM → "Company needs Azure"
```

---

## 2. Target Customer Signal (not employee count alone)

The system should prioritize organizations where measurable business value is
realistic: operational complexity, growth, modernization opportunity, manual
processes, fragmented systems, legacy applications, cloud/AI adoption opportunity,
integration challenges, scaling problems, hiring related to technology, expansion,
new facilities/products/markets, regulatory pressure.

**Employee count alone must never be treated as proof of opportunity.**

---

## 3. The Core Research Principle: Company Facts ≠ Business Signals ≠ Evidence ≠ Hypothesis

> "Company manufactures automotive components" is a **company fact**. It does not mean
> "company needs custom software." "Company is growing" does not mean "company needs
> Azure modernization."

Four things must remain distinct and separately labeled:

| Layer | Example |
|---|---|
| **A. Company facts** | industry, location, employee count, revenue, website, ownership, parent company |
| **B. Business signals** | technology hiring, expansion, new facility, cloud/AI hiring, new ERP, acquisition, new product/market |
| **C. Opportunity evidence** | evidence connecting a signal to a potential technology problem |
| **D. Hypothesis** | what Pamacore believes may be worth investigating — never asserted as fact |

**A general industry article must never upgrade a company to `CONFIRMED_NEED`.**
Recommended strict evidence-strength ladder:

```text
INDUSTRY_SIGNAL → INDIRECT_COMPANY_SIGNAL → COMPANY_SIGNAL →
STRONG_COMPANY_SIGNAL → DIRECT_NEED_SIGNAL → CONFIRMED_NEED
```

`CONFIRMED_NEED` requires **company-specific** evidence: an announcement, job posting,
transformation program, procurement notice, executive statement, or project
announcement from that company — never an industry-level article.

Recommended evidence record shape:

```json
{
  "signal_type": "technology_hiring",
  "signal_scope": "company_specific | industry_general",
  "source_type": "company_job_posting | news_article | directory | industry_report",
  "source_url": "...",
  "source_date": "...",
  "observed_date": "...",
  "evidence_strength": "strong | moderate | weak",
  "evidence_text": "...",
  "confidence": 0.91
}
```

The `signal_scope` field is the key addition over what exists today (see §8): it is
what lets scoring refuse to promote industry-general evidence into a company-level
`CONFIRMED_NEED`.

---

## 4. Cost-Control: An Asymmetric Funnel

Tavily/web research and LLM calls are expensive; directory/registry lookups are cheap.
Never spend expensive research budget on candidates that will never qualify.

```text
CHEAP:  Directory/registry sources → Normalize → Deduplicate → Entity Resolution →
        Basic ICP filtering → Candidate ranking
EXPENSIVE: Web research → Signal extraction → LLM analysis → Contact discovery
```

```text
Millions of directory records → cheap filtering → hundreds/thousands of candidates →
entity resolution → ICP filtering → hundreds of qualified companies →
targeted web research → dozens of strong opportunities → contact research → leads
```

Optimize for **cost per qualified opportunity**, not number of companies discovered.
(§12's Phase 14 extends this principle to actual AI spend tracking, not just design intent.)

---

## 5. Company Universe, Domain, Directory — kept distinct

- **Domain** — a business sector (Manufacturing, Healthcare, ...). A domain is a
  *configuration/context*, not a hardcoded branch in the core engine. Avoid
  `if industry == "manufacturing": ...` in shared code; instead:
  `Core Engine → Domain Profile → Domain Rules`. A Domain Profile carries vocabulary,
  industry classifications, exclusion rules, size rules, ICP rules, opportunity
  vocabulary, evidence rules, scoring weights, research keywords.
- **Company Universe** — the canonical pool of organizations across all domains
  (`Company Universe ├── Manufacturing ├── Healthcare ├── ... └── Future Domains`).
- **Directory** — a *source* organizations are discovered from (D&B, MCA, industry
  association, government registry, trade association). Not the same as a Domain.
- **Company** — the canonical organization (e.g. "Nippon Audiotronix Private
  Limited").
- **Research Source** — evidence discovered during enrichment (company website, job
  posting, press release, news article, annual report).

Multiple directories may refer to the same organization:
`Directory Record → Normalization → Entity Resolution → Canonical Company`. Do not
create duplicate companies merely because they came from different directories.
Canonical identity: legal name, normalized name, website, country, location,
registration identifier, domain, parent company, aliases.

Directory metadata is an **observation**, not immutable truth — retain history
(`employee_count=195 observed=2026-08-11`, then `employee_count=220 observed=2026-10-01`
— both kept), especially for employee count, revenue, classification, address,
ownership.

---

## 6. Qualification, Research Questions, Opportunity Mapping

**Qualification stages:** (1) Basic eligibility — cheap deterministic checks (industry,
country, company type, employee count, exclusions, parent company, duplicate,
website availability); (2) ICP fit; (3) Opportunity potential — only after ICP fit
does expensive research begin; (4) Evidence research.

**Research should answer structured questions, not "tell me everything":**
Company (what/industry/where/size/products/business model), Technology (visible
stack, legacy signs, cloud/AI adoption, tech hiring), Business Change (growing,
expanding, acquiring, launching, entering markets), Operational Pain (manual
processes, fragmented systems, reporting gaps, integration needs, scalability,
compliance burden), Opportunity ("what technology opportunity could reasonably be
investigated based on the evidence" — never "what should Pamacore sell").

**Opportunity mapping must preserve:** `Evidence → Inference → Hypothesis →
Potential Solution`. Example: hiring software engineers + disconnected systems +
multi-location expansion → hypothesis "application/integration modernization" →
candidate solutions (Custom Application Development, Architecture Review, Cloud
Modernization) — never solution-first reasoning.

---

## 7. Contact, Lead, Discovery, Assessment, Recommendation, Outreach — behavioral rules

- **Contact discovery** only after a company passes the qualification threshold — not
  for every discovered company. Role selection depends on the opportunity (AI
  opportunity → CTO/CIO/Head of AI; operational automation → COO/Ops Head;
  application modernization → CTO/CIO/IT Head).
- **Lead creation** is not automatic from a company match:
  `Company → ICP Candidate → Qualified Company → Opportunity Candidate → Contact
  Identified → Lead`. A Lead should carry company, contact, role, opportunity
  hypothesis, evidence, confidence, qualification score, recommended solution,
  outreach angle.
- **Discovery** moves from "we think they may need X" to "let's validate whether they
  actually have problem X" — captures current problem/process/solution, systems,
  pain points, business impact, urgency, stakeholders, constraints, desired outcome,
  success criteria.
- **Assessment** evaluates the validated situation: Current State → Technology
  Maturity → Process Maturity → Data Maturity → AI Readiness → Architecture →
  Business Impact — based on validated Discovery data, not company-research
  assumptions.
- **Recommendation**: Assessment → Problems → Root Causes → Prioritized Opportunities
  → Recommended Solution → Implementation Roadmap. A recommendation must never be
  generated without a defensible evidence → hypothesis → capability chain.
- **Outreach** must use company-specific evidence, never generic filler
  ("I noticed you're growing..."). Shape: Observed Signal → Business Implication →
  Potential Problem → Pamacore Capability → Low-pressure Discovery CTA. Never claim
  "you have a problem" — say "we noticed X, which may create Y, worth exploring
  whether it's relevant."

Every recommendation should follow this order: (1) identify the company's pain
points, (2) map them to the AI Solution Catalog (Appendix A), (3) if no catalog entry
fits, suggest a generic industry-appropriate AI opportunity, (4) clearly label each
recommendation as an existing Pamacore/AgneticAI offering vs. a generic industry
opportunity — never blur the two.

---

## 8. Ground Truth: What Already Exists (as of 2026-08-12)

Confirmed by reading the actual domain/application/infrastructure/presentation
layers, not assumed.

| Bounded context | State | Where |
|---|---|---|
| **company** | Mature. `Company` aggregate, `CompanyProfile`/`CompanySize`/`Industry` value objects, full CQRS (create/update/delete/get/list/search), SQLAlchemy-persisted, API-exposed (`company_router.py`). | `app/domain/company`, `app/application/company`, `app/infrastructure/persistence/repositories/company` |
| **contact** | Present: `Contact` entity, `Email` value object, repository, CQRS handlers, API-exposed. | `app/domain/contact`, `app/infrastructure/persistence/repositories/contact` |
| **lead** | Mature. `Lead` aggregate requires an existing `company_id` **and** `contact_id` (contact details are deliberately not duplicated on Lead). `LeadSource` enum currently has no research/AI-discovery origin value, and nothing updates `LeadStatus`/`LeadScore` from real prospect engagement. `LeadScore`, `LeadStatus`, domain events (`created`/`qualified`/`converted`), persisted, API-exposed. | `app/domain/lead`, `app/infrastructure/persistence/repositories/lead` |
| **discovery** | Mature, and already matches §7's Discovery vision closely: `BusinessGoal`, `PainPoint`, `Stakeholder`, `Technology` value objects, persisted, API-exposed. | `app/domain/discovery` |
| **assessment** | Mature, already matches §7's Assessment vision: `Finding`, `MaturityLevel`, `AssessmentDimension`, `Evidence`, `Opportunity` value objects, `AssessmentService`, persisted, API-exposed. | `app/domain/assessment` |
| **recommendation** | Schema is mature — `Solution` (with `SolutionType`, `TechnologyStack`, `BusinessBenefit`, `ImplementationRisk`, `Dependency`, `ROI`, `CostEstimate`), `RoadmapPhase`, full CQRS command set. **But `GenerateRecommendationHandler` is a stub**: given an `assessment_id` it just creates an *empty* `Recommendation` shell — no AI call, no catalog lookup, no solutions populated. Concrete file: `app/application/recommendation/handlers/generate_recommendation_handler.py`. | `app/domain/recommendation`, `app/application/recommendation` |
| **qualification** | A `Qualification` aggregate exists, but it is a **different concept** than company_research's opportunity-qualification scoring: it ties `lead_id` + `assessment_id` together with a status/score for the *post-Lead, post-Assessment* stage. Do not conflate with `app.domain.company_research.value_objects.qualification_score.QualificationScore`. Names collide; concerns don't. | `app/domain/qualification` |
| **workflow** | A generic `Workflow`/`WorkflowExecution`/`WorkflowStep` execution engine with status tracking and events already exists, unused by company_research today. Ready-made mechanism for orchestrating and observing the multi-stage chain per company. | `app/domain/workflow` |
| **report** | A versioned, sectioned, approvable `Report` aggregate (draft → submitted → approved → published) already exists — the natural home for a generated Proposal document. No need to invent a new document model for Outreach. | `app/domain/report` |
| **ai** | Centralized, multi-provider (Gemini/OpenAI/Azure OpenAI) `AIExecutionService`, switchable via one `.env` value (`AI_PROVIDER`), reusable by any module. Each client already implements `health_check()` — unused today outside its own module (relevant to §12 Phase 13). | `app/infrastructure/ai`, `app/infrastructure/configuration` |
| **company_research** | Rebuilt this session: Tavily-backed discovery, AI-assisted identity verification, industry classification, ICP/size matching, 4-tier evidence classification, qualification scoring, opportunity→service mapping. Returns a response DTO only — **creates no Company, Contact, Lead, Discovery, Assessment, or Recommendation records.** Currently an island upstream of everything in this table. | `app/domain/company_research`, `app/application/company_research`, `app/infrastructure/company_research` |

**Not present anywhere in the codebase today:** Company Universe/directory ingestion
(discovery is 100% live Tavily search per request — the expensive path §4 warns
against), Domain Profile as data/config (hardcoded Python dicts today), entity
resolution into the canonical `Company`, Signal/Evidence with `signal_scope`, contact
auto-discovery, AI Solution Catalog as queryable data, **and nothing at all** for:
multichannel sequencing, reply handling, meeting booking, deliverability/compliance
(no unsubscribe/do-not-contact list exists anywhere), outcome feedback learning, AI
provider health-checks/fallback, AI cost/quota tracking, or a human-in-the-loop
review queue.

---

## 9. Implementation Roadmap — Track 1: Core Pipeline Wiring

Because the downstream lifecycle already exists and is solid, this track is a wiring
project, not a rebuild. Each phase is additive, touches a bounded set of files, and is
independently testable/shippable.

### Phase 0 — Domain Profile foundation (no pipeline behavior change)

Move hardcoded industry/ICP vocab out of Python into data (§5). New
`app/domain/company_research/value_objects/domain_profile.py`; seed profiles for the
9 initial sectors under `app/infrastructure/configuration/domain_profiles/`; modify
`IndustryClassifier`/`IcpMatcher` to accept an injected `DomainProfile`.

### Phase 1 — Evidence Model v2 (`signal_scope`)

Add `signal_scope: "company_specific" | "industry_general"` and `source_date`/
`observed_date` to `EvidenceItem` and `EvidenceSignalExtractor`; require
`confirmed_company_specific_count >= 2` for `CONFIRMED_NEED`, not just `confirmed >= 2`
regardless of scope.

### Phase 2 — Company Universe cheap-discovery tier

New `CompanyDirectoryPort` distinct from the existing web-search `CompanyDiscoveryPort`;
one concrete registry/directory adapter; `SearchCompaniesHandler` tries the cheap port
first, falls back to Tavily only for domains without registry coverage.

### Phase 3 — Entity Resolution: bridge to `app.domain.company`

The single biggest structural gap in Track 1: candidates become real `Company`
aggregates instead of a disposable response DTO. **Decision needed:** opt-in
`persist_as_companies` flag on `CompanyResearchRequest` (recommended) vs. always-on,
to avoid silently breaking the current "research-only" contract.

### Phase 4 — AI Solution Catalog as first-class data

New `SolutionCatalogEntry` value object + seed data from Appendix A; fix
`GenerateRecommendationHandler` to actually call `AIExecutionService` with Assessment
findings + matched catalog entries and populate real `Solution` entries; point
company_research's `OpportunityMapper` at the same catalog instead of its own
disconnected list.

### Phase 5 — Contact Discovery

New `ContactDiscoveryPort` + adapter, invoked only above
`minimum_qualification_score`; role targeting driven by the Phase 4 catalog match.

### Phase 6 — Lead creation bridge

Add a research-originated `LeadSource` value; create `Company` + `Contact` + `Lead`
for qualified candidates via existing command paths, carrying qualification score,
hypothesis, and evidence as Lead metadata.

### Phase 7 — Outreach generation (first build in this track, minimal)

A first, single-touch version reusing `app.domain.report` for the artifact. (Track 2
below replaces this with a real multi-touch engagement engine — treat Phase 7 as a
thin placeholder only if you need something demoable before Track 2 is ready.)

### Phase 8 — Orchestration via the existing Workflow engine

Wrap DISCOVER→...→LEAD as a `Workflow`/`WorkflowStep` execution per candidate,
reusing `app.domain.workflow`. A failed step should leave a resumable/failed
Workflow state instead of `SearchCompaniesHandler._research` silently swallowing the
exception and returning `None`, which is today's behavior.

---

## 10. Track 2 — Engagement & Revenue Layer

**Why this deserves its own track, not a sub-phase of Track 1:** an AI SDR's value is
measured in booked meetings, not discovered companies. Treating "Outreach" as one
last, single-shot phase (as the original draft did) undersells the highest-leverage
part of the whole system. A real AI SDR is a multi-touch, reply-aware conversation
engine, not a "generate one email" function.

### Phase 9 — Multichannel Sequencing Engine

New `app/domain/sequence` bounded context: a `Sequence` aggregate = an ordered list of
touches (email, LinkedIn message, call task) with wait-time rules and branching on
reply/no-reply/bounce. Each touch is generated via `AIExecutionService`, grounded in
the Lead's evidence chain, but *varied* per touch (touch 1: signal-led opener; touch 2:
different proof point/angle; touch 3: breakup message) — single-shot outreach is the
most common weak point in AI SDR tools today; sequencing is what fixes it.

### Phase 10 — Reply Intelligence & Meeting Booking

Inbound reply classification (interested / not now / objection / unsubscribe / OOO /
wrong person) via a new `ReplyClassificationPort` — a distinct AI capability from
outreach generation. On "interested": suggest meeting times (calendar integration) and
draft a scheduling reply. On "objection": draft a grounded response but require human
approval before send (Track 4 Phase 16's review gate). This is also where
`Lead.status`/`LeadScore` should start updating from real prospect behavior instead of
only internal qualification — nothing today does that.

### Phase 11 — Deliverability & Compliance

Non-negotiable before real outbound volume: a persisted unsubscribe/do-not-contact
list checked before every send (doesn't exist anywhere today), suppression on
bounce/complaint, sending-domain warmup, quiet-hours/timezone-aware send windows, and
jurisdiction-aware consent handling — `CompanyResearchRequest.geography` already
identifies the target jurisdiction and can drive which compliance rules apply
(CAN-SPAM/GDPR/TCPA differ by region). This is the track most likely to create real
legal/reputational risk if skipped, and it's far cheaper to build early than to
retrofit after a bad send.

---

## 11. Track 3 — Closed-Loop Learning

### Phase 12 — Outcome Feedback Loop

Every Track 1 decision (accept/reject candidate, score, classify evidence) is
currently one-way, with no mechanism to learn whether it was right. Persist an
`OutcomeEvent` (meeting_booked / won / lost / no_response) against the originating
Lead, and run a periodic (offline, not real-time/online-ML) recalibration pass that
feeds back into:

- `QualificationScorer` weights — which evidence types actually correlated with
  booked meetings, per domain profile
- `IndustryClassifier`/`IcpMatcher` — which ICP segments actually convert
- the Solution Catalog — which recommended solution type gets traction per sector

This is only possible because Track 1 already gives every decision a traceable
evidence chain (§3) — the feedback loop is cheap to add *because* that discipline
exists upstream. It's what separates a static rules engine from a system that
improves with volume, and it's explicitly a Phase-12-not-Phase-1 item: it needs real
outcome data from Track 2 to have anything to learn from.

---

## 12. Track 4 — AI Platform Resilience, Trust & Governance

Grounded directly in incidents from *this session*, not hypotheticals — each phase
below maps to something that actually broke and cost real debugging time.

### Phase 13 — Model Health Checks & Automatic Fallback

This session hit the same failure mode twice: a pinned Gemini model name
(`gemini-2.5-pro`, then `gemini-2.5-flash`) silently became unavailable ("no longer
available to new users"), discovered only when a live call 404'd mid-demo. Add a
startup/periodic health check per provider (building on the `health_check()` method
each client already implements but nothing calls externally) and an ordered fallback
list (`AI_PROVIDER=gemini` with `AI_PROVIDER_FALLBACK=openai,azure_openai`) so one
model deprecation degrades gracefully instead of failing an entire batch.

### Phase 14 — AI Cost & Quota Governance

Also hit this session: Gemini's 20-req/day free-tier limit and an OpenAI account with
zero credits, both discovered only via failed live calls mid-batch. For a system
whose entire design principle is "spend AI budget only on qualified candidates" (§4),
there is currently no tracking of *actual* spend/usage anywhere. Add persisted
per-provider request/token counters, a configurable daily/monthly budget, and a
pre-flight budget check in `SearchCompaniesHandler` before fanning out verification
calls — fail fast with one clear message instead of the 17 near-identical error lines
this session's own Swagger test produced.

### Phase 15 — Config Diagnostics

Also this session: a stale Windows-user-scope `OPENAI_API_KEY` silently shadowed
`.env` for an unknown period, found only through several rounds of manual
`os.environ` inspection. A small `/admin/ai-config` endpoint (or CLI command)
reporting *effective* resolved config — provider, model, key fingerprint (last 4
chars only, never the full key), and source (`.env` vs. real process env var) — would
have cut that entire diagnosis to one call. Cheap to build, reusable for every future
key/provider issue.

### Phase 16 — Human-in-the-Loop Review Queue & Explainability

Nothing in Track 1 or Track 2 should send outbound communication or finalize a Lead
fully autonomously without an inspectable trail — at least until Track 3 has earned
more autonomy with real feedback data. A review queue (a state on `Lead`/`Sequence`:
`pending_review → approved → sent`) where a human sees the full evidence → hypothesis
→ recommendation → message chain before the first touch sends, and can approve/edit/
reject. The edit/reject action itself becomes Track 3 training signal. This also
matters for adoption: sales teams reject opaque AI output far more than output whose
reasoning they can see — and since §3's evidence model already produces a traceable
chain, surfacing it is a presentation problem, not a new architecture problem.

**This phase should land before or alongside Track 2 Phase 9** — do not ship
autonomous multi-touch outreach without the review gate in place first.

---

## 13. Track 5 — Data Quality & Enrichment

### Phase 17 — Enrichment Waterfall

Tavily is currently the only data source for both discovery and enrichment — a
single point of failure with a hard completeness ceiling. This session's own test run
returned junk candidates ("Company search", "Browse by size: 51-200 employees") —
direct evidence of Tavily-only discovery's precision limits, consistent with the
"discovery-side candidate quality" issue flagged and deferred earlier in this
project. Introduce a waterfall behind the existing discovery/enrichment ports: cheap
structured sources first (Phase 2's directory tier), Tavily as fallback, and room for
a future paid enrichment API as a third tier — same port contract, swappable adapter,
no caller changes.

---

## 14. Track 6 — Scale, Multi-Tenancy & Compliance (as-needed, not urgent now)

Flagged for awareness, not proposed as near-term work unless you say otherwise:

- **Multi-tenancy** — if Pamacore ever serves multiple client organizations (not just
  one company's own pipeline), every aggregate needs a `tenant_id`/`organization_id`
  boundary now rather than retrofitted later. Far cheaper to add at Phase 3 (entity
  resolution) time than after real data exists.
- **Data retention & PII handling** — discovered contacts are personal data; define a
  retention/deletion policy before Phase 5 (Contact Discovery) goes live at real
  volume, not after.
- **Audit logging** — who approved/edited/sent what (ties into Phase 16's review
  queue). Needed for any regulated-industry customer — a real possibility given
  Healthcare/Pharma/Financial Services are explicit target domains (§1).

---

## 15. Sequencing Across Tracks

Not a single dependency chain — several tracks parallelize:

```text
Track 1 Phase 0-1 (Domain Profile, Evidence v2)   ─┐
Track 4 Phase 13-15 (AI resilience/governance)     ─┼─→ start immediately, in parallel, low risk
                                                     ┘
Track 1 Phase 2-3 (Cheap discovery, Entity resolution) ─→ prerequisite for Track 5 Phase 17

Track 1 Phase 4 (Solution Catalog) ─┐
Track 1 Phase 5 (Contact Discovery) ─┼─→ prerequisite for Track 1 Phase 6 (Lead bridge)
                                     ┘
Track 1 Phase 6 (Lead bridge) ─→ prerequisite for Track 2 (Engagement) and Track 3 (Learning)

Track 4 Phase 16 (Human review queue) ─→ before or alongside Track 2 Phase 9 — never ship
                                          autonomous multi-touch outreach without the gate.

Track 6 (Scale/Tenancy) ─→ decide the tenant_id boundary before Track 1 Phase 3 if
                            multi-tenancy is a near-term reality, not a someday one.
```

**Recommendation as principal architect, if you want one linear starting point:**
**Track 4 Phase 13–15 first** (cheap, immediately valuable, directly prevents repeats
of failures already hit this session) → **Track 1 Phase 0–1** → **Track 1 Phase 2–6**
through to the Lead bridge → **Track 4 Phase 16 together with Track 2** (never ship
engagement without the review gate) → **Track 3** once there's real outcome data to
learn from. Track 5 and Track 6 slot in opportunistically wherever their prerequisites
land.

---

## 16. Future Direction — Genuine Agentic AI (documented, not committed, no points allocated)

Everything in Tracks 1–6 is **AI-assisted automation**, not agentic AI in the
technical sense: single-shot LLM calls at fixed points in an otherwise
deterministic pipeline (one Gemini call for identity verification, one for
recommendation generation). The AI never decides what to do next, never calls
tools autonomously, never loops or self-corrects. This section exists so the
distinction — and the reasoning for not pursuing it yet — isn't lost.

**What genuine agentic behavior would require**, none of which exists today:
tool use/function calling (the AI chooses which function to invoke next, not a
human-coded sequence calling it once); a control loop (act → observe → decide
next action → repeat, not one prompt → one response → done); state across the
loop (a working memory of what's already been tried/found); self-evaluation (the
AI judges "do I have enough evidence?" instead of a hardcoded threshold); and
hard stopping criteria/guardrails, since a loop that decides its own next move
can also decide to loop forever or spend without limit.

**Where it would fit, if pursued:** company_research's per-candidate research
step (`SearchCompaniesHandler._research_candidate`) is the natural candidate —
today every candidate gets the same fixed sequence (verify → gather 2-3 fixed
evidence queries → classify → score) regardless of what's actually found, where
an adaptive agent could search again on ambiguous evidence or stop early on a
clear dead end. Recommendation generation is a weaker candidate since its input
(a human-validated Assessment) is already complete — less for an agent to
adaptively go find out.

**Why this isn't scheduled:** real, concrete constraints already hit earlier in
this project would get worse under a naive agentic redesign, not better --
Gemini's 5 requests/minute free-tier limit (Track 4 Phase 13's finding) would be
strained by an agent that costs 3-6 calls per candidate instead of 1;
`AIBudgetGuard` (Phase 14) assumes one call per candidate and would need a
worst-case-steps redesign before it's safe; test strategy shifts from "assert
exact output" to "assert valid state," since an agent can legitimately choose a
different tool sequence for identical input across runs; and "why did it decide
X" needs first-class tool-call tracing, not an afterthought, or the
evidence-traceability principle this whole architecture is built around is lost.

**If this gets revisited**, the shape of a safe pilot: three tools for the
evidence-gathering step only (`search(query)`, `classify_scope(text)` — reusing
Track 1 Phase 1's existing function as-is, `stop()`); a hard cap of 3 tool calls
per candidate (barely more than today's fixed 2 queries); routed through the same
`AIBudgetGuard`, pre-charged for the worst case; feature-flagged against the
existing deterministic path so the two can be compared on a sample before any
further commitment. Scoped narrowly enough to validate the idea without betting
the whole module on it, and it wouldn't touch identity verification or scoring.

---

## Appendix A — AI Solution Catalog (seed content, cleaned)

Recommendation order for every generated opportunity: (1) identify pain points, (2)
map to this catalog, (3) if nothing fits, propose a generic sector-appropriate AI
opportunity, (4) label each as **catalog offering** or **generic opportunity** —
never blur the two.

### SMB / general sectors

| Sector | Pain points | Candidate solutions |
|---|---|---|
| Retail & E-commerce | Slow product copy, cart abandonment, generic support, poor personalization | AI product listing generator; visual merchandising AI; shopping assistant chatbot; personalized campaign generator |
| Real Estate & Property | Slow listing creation, weak virtual tours, unqualified leads | Listing/brochure generator; AI staging; lead qualification chatbot; neighborhood Q&A assistant |
| Healthcare Clinics & Diagnostics (small practices) | Admin overload, missed follow-ups, no-shows, documentation burden | AI medical scribe; appointment reminder/follow-up bot; patient FAQ assistant; referral/discharge drafting |
| Legal Services (small firms) | Slow drafting, contract review bottlenecks, intake friction | Contract drafting assistant; case summary/research assistant; intake chatbot; compliance checklist generator |
| Restaurants & Food | Menu updates, review management, marketing content, order overhead | Menu/description generator; AI review responder; social content engine; voice/chat ordering assistant |
| Education, Coaching, Ed-tech | Content bottleneck, engagement, feedback at scale | Course/quiz generator; AI tutor chatbot; personalized feedback generator; marketing content generator |
| Local Services (salons, gyms, wellness, home services) | No marketing team, inconsistent booking follow-up | Booking/reminder/upsell chatbot; social content generator; review/reputation management |
| Travel & Tourism (agencies, small operators) | Manual itinerary creation, slow lead response | AI itinerary builder; multilingual travel chatbot; marketing content generator |
| Manufacturing & B2B SMBs | Technical documentation, slow RFP/quote response, lead qualification | Proposal/quote generator; technical documentation assistant; inbound lead qualification bot |
| Accounting, Finance & Insurance Advisors | Client communication overhead, report generation, compliance docs | Financial report summarizer; client query chatbot; policy/plan comparison generator |
| Marketing & Creative Agencies | Content velocity, ad variant testing, client reporting time | Multi-format content generator; AI ad variant generator; auto-generated performance reports |
| Automotive (dealers, service centers) | Service reminder follow-ups, lead-to-test-drive conversion | Service reminder/upsell bot; vehicle description generator; lead qualification chatbot |

### Research-heavy sectors

| Sector | Pain points | Candidate solutions |
|---|---|---|
| Biotech & Pharma Research Labs | Discovery timelines, literature overload, documentation burden, regulatory writing | Literature review/synthesis assistant; molecule/protein generation & property prediction; lab-notebook-to-report assistant; regulatory drafting; grant proposal assistant |
| Academic & R&D Institutions | Slow literature review, manuscript drafting, grant-writing bottlenecks, data-analysis reporting | Research summarization/citation assistant; manuscript drafting/editing; data-to-insight generator; peer-review prep; grant/funding matcher |
| Clinical Trials & CROs | Protocol drafting time, recruitment matching, adverse-event documentation | Trial protocol drafting; patient-trial matching; adverse-event report generator; recruitment content generator |
| Agri-Tech & Food Science Research | Crop/soil data interpretation, R&D documentation, slow trial-to-insight cycles | Field trial data summarizer; formulation/recipe R&D assistant; research report generator |
| Materials Science & Chemical R&D | Slow candidate-material screening, dense technical documentation | Materials property prediction/generation; patent-landscape assistant; technical report/datasheet generator |
| Environmental & Climate Research | Fragmented data sources, policy-report writing load, public communication gap | Multi-source data synthesis assistant; policy brief generator; public-facing content generator |

**Positioning note for research/biotech vs. SMB retail:** the value proposition shifts
from "save time on content" to "accelerate discovery and reduce documentation burden
without compromising rigor." Emphasize retrieval-augmented generation over raw
generation with human-in-the-loop verification (hallucination risk matters a lot to
these buyers), regulatory-format awareness (FDA, journal standards, IRB), and
integration with existing tools (ELN, LIMS, Zotero/EndNote) over a standalone chatbot.

### Common wedge offer across all sectors

Most SMBs don't need a custom LLM — they need three things wrapped simply:

1. A content/document generation tool (saves hours/week)
2. A customer-facing chatbot (captures leads 24/7, cuts response time)
3. Automated reporting/summarization (turns raw data into decisions)

### Reference: sector taxonomy (for Domain Profile seeding, §5/Phase 0)

- **Primary (Raw Materials):** Agriculture & Farming; Forestry & Logging; Mining &
  Metals; Oil & Gas
- **Secondary (Manufacturing & Construction):** Aerospace & Defence; Automotive;
  Chemicals; Construction & Infrastructure; Consumer Goods; Food & Beverage;
  Pharmaceuticals & Biotech
- **Tertiary (Services):** Banking & Finance; Education; Energy & Utilities;
  Healthcare; Hospitality & Tourism; Media & Entertainment; Retail & E-commerce;
  Transportation & Logistics
- **Quaternary (Knowledge & Technology):** IT; Telecommunications; Consulting &
  Professional Services; R&D

---

## Open decisions for you

1. **Track 1 Phase 3 persistence default** — opt-in flag vs. always-on
   company/contact/lead creation from `/company-research/search`. Recommend opt-in to
   preserve the current "research-only" contract for existing callers.
2. **Starting point** — my recommendation is Track 4 Phase 13–15 first (cheap,
   prevents repeats of this session's own incidents), then Track 1 Phase 0–1. Confirm
   or redirect.
3. **Solution catalog storage** — static config vs. DB table for Track 1 Phase 4.
   Static is faster to ship; DB is needed if non-engineers will edit the catalog.
4. **Engagement channels** — should Track 2 Phase 9 target email only first, or
   email + LinkedIn from day one? Significantly changes that phase's scope.
5. **Autonomy posture** — is human-in-the-loop (Track 4 Phase 16) a permanent
   requirement, or a bootstrap phase you expect to relax once Track 3 has enough
   outcome data to trust the system more? Changes how much investment Phase 16's UI
   deserves.
6. **Multi-tenancy** — is Pamacore single-tenant (your own pipeline) or will it serve
   multiple client organizations? Determines whether Track 6's `tenant_id` work
   should be pulled forward before Track 1 Phase 3.
