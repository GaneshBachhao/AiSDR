# Pamacore / AiSDR — Product Backlog

Source of truth for scope. Companion to [`pamacore_aisdr_summary.md`](pamacore_aisdr_summary.md)
(architecture/roadmap) and [`pamacore_sprint_plan.md`](pamacore_sprint_plan.md) (schedule).
Every Epic ID below matches the Phase number from the architecture doc's Track 1–6
breakdown, so the two documents cross-reference directly.

**Methodology:** Scrum-style, 1-week sprints, solo developer + AI pair-programming
capacity (see sprint plan for the capacity assumption and why). Story points use
Fibonacci (1, 2, 3, 5, 8, 13, 21). Priority uses MoSCoW (**M**ust / **S**hould /
**C**ould / **W**on't-now).

---

## Definition of Ready (a story can enter a sprint)

- Acceptance criteria are written and testable
- Dependencies (other stories/epics) are already Done, or explicitly not blocking
- Files/modules to touch are identified (no "figure out where this goes" left open)
- Any external decision it needs (see "Open decisions" in the architecture doc) is resolved

## Definition of Done (a story can be marked Done)

- Code written, follows existing layer conventions (domain/application/infrastructure/presentation)
- Unit tests added/updated; full suite green (no regressions to unrelated modules)
- For anything touching a live external API (AI providers, Tavily, calendar, email):
  at least one live smoke-test run, output reviewed, not just mocked tests
- No secrets/keys printed in logs, chat output, or committed files
- Docs updated if the story changes a public contract (API request/response shape,
  `.env` variables, README)
- Nothing committed to git until explicitly requested (standing rule for this project)

---

## Epic Summary

| Status | Epic | Track | Title | Points | Priority | Depends on |
|---|---|---|---|---|---|---|
| `[x]` Done | EPIC-13 | 4 | Model health checks & automatic fallback | 8 | **M** | — |
| `[x]` Done | EPIC-15 | 4 | AI config diagnostics endpoint | 5 | **M** | — |
| `[x]` Done | EPIC-14 | 4 | AI cost & quota governance | 10 | **M** | EPIC-13 |
| `[x]` Done | EPIC-00 | 1 | Domain Profile foundation | 8 | **M** | — |
| `[x]` Done | EPIC-01 | 1 | Evidence Model v2 (`signal_scope`) | 8 | **M** | — |
| `[x]` Done | EPIC-02 | 1 | Company Universe cheap-discovery tier | 13 | **M** | EPIC-00 |
| `[x]` Done | EPIC-03 | 1 | Entity Resolution → canonical `Company` | 13 | **M** | EPIC-02 |
| `[x]` Done | EPIC-04 | 1 | AI Solution Catalog + fix `generate_recommendation` | 13 | **M** | EPIC-01 |
| `[x]` Done | EPIC-05 | 1 | Contact Discovery | 8 | **M** | EPIC-03, EPIC-04 |
| `[x]` Done | EPIC-06 | 1 | Lead creation bridge | 8 | **M** | EPIC-05 |
| `[x]` Done | EPIC-08 | 1 | Workflow orchestration | 8 | **S** | EPIC-06 |
| `[ ]` Backlog | EPIC-17 | 5 | Enrichment waterfall | 8 | **S** | EPIC-02, EPIC-03 |
| `[ ]` Backlog | EPIC-16 | 4 | Human-in-the-loop review queue & explainability | 13 | **M** | EPIC-06 |
| `[ ]` Backlog | EPIC-09 | 2 | Multichannel sequencing engine | 21 | **M** | EPIC-16 |
| `[ ]` Backlog | EPIC-10 | 2 | Reply intelligence & meeting booking | 13 | **M** | EPIC-09 |
| `[ ]` Backlog | EPIC-11 | 2 | Deliverability & compliance | 13 | **M** | EPIC-09 |
| `[ ]` Backlog | EPIC-12 | 3 | Outcome feedback loop | 13 | **S** | EPIC-10, EPIC-11 |
| `[ ]` Won't-now | EPIC-07 | 1 | Outreach (thin placeholder) | — | **Won't-now** | superseded by EPIC-09–11, see note |
| `[ ]` Parked | PARK-T6 | 6 | Multi-tenancy / retention / audit logging | — | **C** | as-needed, see Parking Lot |

**EPIC-07 note:** the architecture doc's original Phase 7 ("thin single-touch outreach
placeholder") is dropped from the sequenced backlog. Track 2 (EPIC-09–11) replaces it
with the real thing; building a throwaway placeholder first would be wasted work for
a solo+AI stream with no separate "demo team" needing something earlier. Revisit only
if you need something demoable before Track 2 is ready.

**Total sequenced scope:** 183 points across 17 epics (excluding EPIC-07 and the
Track 6 parking lot, which are explicitly out of the committed roadmap).

---

## Backlog Detail

### EPIC-13 — Model health checks & automatic fallback (8 pts) · Track 4 · `[x]` Done — Sprint 1

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 13.1 | As the platform, I want a `health_check_all()` on `AIExecutionService` so I know which providers are actually reachable right now | Calls each configured provider's existing `health_check()`; returns `{provider: bool}`; no live call for providers with no key configured | 3 | `[x]` Done |
| 13.2 | As an operator, I want an ordered fallback list so one provider's model deprecation doesn't fail a whole batch | New `AI_PROVIDER_FALLBACK` env var (comma-separated); `ApplicationAIProvider` tries the next provider in the list on `AIProviderException`/`AIClientException` | 5 | `[x]` Done |

Shipped in `app/application/ai/ports/ai_provider.py`, `app/infrastructure/ai/adapters/application_ai_provider.py`,
`app/infrastructure/configuration/ai_provider_settings.py`, `app/infrastructure/ai/composition.py`.
Live-verified: forcing a real Gemini failure (deprecated model) correctly triggered
fallback to OpenAI and surfaced the true root cause via the exception chain rather
than a generic error — see sprint plan §"Sprint 1 notes."

### EPIC-15 — AI config diagnostics endpoint (5 pts) · Track 4 · `[x]` Done — Sprint 1

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 15.1 | As an operator, I want to see effective resolved AI config without writing a debug script | New `GET /admin/ai-config` (or CLI) returns provider, model, key fingerprint (last 4 chars only), and source (`.env` vs. real process env var) for each configured provider | 5 | `[x]` Done |

Shipped as `GET /admin/ai-config` (`app/presentation/api/routers/admin_router.py`,
`app/infrastructure/ai/composition.py::ai_config_diagnostics()`). Live-verified
against the real running app — and immediately caught a real, previously-unknown
issue: a process-level `OPENAI_API_KEY` (different from the one already fixed
earlier, and different from `.env`'s value) is shadowing config with an invalid
key. Flagged to the user; not fixable from application code since it's inherited
from the parent terminal process.

### EPIC-14 — AI cost & quota governance (10 pts) · Track 4 · `[x]` Done — Sprint 2

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 14.1 | As the platform, I want every AI call's token usage persisted so spend is visible | New `ai_usage_log` table/repo; `AIExecutionService.execute()` records provider, model, tokens, timestamp on every call | 5 | `[x]` Done |
| 14.2 | As an operator, I want a configurable daily/monthly budget per provider | New `AIBudgetSettings`; budget values read from `.env` | 2 | `[x]` Done |
| 14.3 | As the platform, I want a pre-flight budget check before fanning out a research batch | `SearchCompaniesHandler` checks projected usage vs. remaining budget before dispatching identity-verification calls; fails fast with one clear message instead of N per-candidate failures | 3 | `[x]` Done |

Shipped as a fresh `ai_usage_log` table (`AIUsageLogModel`, `AIUsageTracker`) rather
than reusing the pre-existing `AIRequestModel`/`AIRequestMapper`/`ExecuteAIRequestHandler`
stack — that stack was discovered to be **broken and never actually exercised**:
`SqlAlchemyAIRequestRepository` doesn't implement the `save()` its own domain
interface declares, and once patched, persisting through `AIRequestMapper`'s
`converter_registry` fails on the `Temperature` value object (`TypeError: float()
argument must be a string or a real number, not 'dict'`). Not fixed here (out of
Sprint 2 scope); flagged below as a new backlog candidate. New port
`AIBudgetPort`/`AIUsageRecorder` added to `app/application/ai/ports` to keep
`SearchCompaniesHandler` and `AIExecutionService` decoupled from the concrete
infrastructure implementation. Live-verified end-to-end: a real Gemini call
correctly decremented the tracked budget (20 → 19), and constraining the budget to
1 caused a real `/company-research/search` call (21 live-discovered candidates) to
correctly return `429` with one clear message instead of attempting any of the 21
identity-verification calls.

**New backlog candidate (not yet estimated/scheduled):** decide whether to fix
(`converter_registry` value-object conversion + missing `save()`) or delete the
orphaned `AIRequestModel` / `AIRequestMapper` / `ExecuteAIRequestHandler` /
`GenerateAIResponseHandler` / `ai_router.py` stack -- it duplicates what
`AIExecutionService`/`AIUsageTracker` now do, was never wired into the live app
(`ai_router.py` isn't registered in `api_router`), and is confirmed broken. Same
"confirmed-dead, never actually worked" pattern as the deleted legacy
`app/company_research/` module and the orphaned `SettingsLoader`/`AISettings`
duplicate stacks found earlier in this project.

### EPIC-00 — Domain Profile foundation (8 pts) · Track 1 · `[x]` Done — Sprint 3

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 0.1 | As the platform, I want industry/ICP vocabulary as data instead of hardcoded dicts | New `DomainProfile` value object (vocabulary, size rules, exclusions, evidence keywords, scoring weight overrides) | 3 | `[x]` Done |
| 0.2 | As an operator, I want seed profiles for the 9 initial sectors | JSON/YAML profiles under `app/infrastructure/configuration/domain_profiles/` for Manufacturing, Healthcare, Pharma, Biotech, Research, Logistics, Financial Services, Construction, Retail | 3 | `[x]` Done |
| 0.3 | As the platform, I want `IndustryClassifier`/`IcpMatcher` to use the injected profile | Both accept a `DomainProfile`; behavior for the default profile is unchanged (regression-safe) | 2 | `[x]` Done |

Shipped as `app/domain/company_research/value_objects/domain_profile.py`
(`DomainProfile`, frozen dataclass) + 9 JSON seed files under
`app/infrastructure/configuration/domain_profiles/`, loaded via
`load_domain_profile()`/`load_all_domain_profiles()`. `IndustryClassifier.infer_industry`/
`matches` and `IcpMatcher.enterprise_exclusion` now take an optional `profile`
parameter; the pre-existing class constants remain the single source of truth for
the default (no-profile) behavior, so nothing downstream changed. Seed data was
derived directly from the existing hardcoded keyword table (not invented), so
there's no drift between the old defaults and the new seed profiles.
**Deliberately not done this sprint** (out of the committed 0.1–0.3 scope):
`SearchCompaniesHandler` does not yet select/inject a profile per request —
profiles are loadable and provably change behavior when passed explicitly, but
nothing in the live request path picks one yet. That's future wiring, not part of
this "no pipeline behavior change" phase.

**New finding (2026-08-12, live verification):** a live `/company-research/search`
call surfaced a real Gemini `429 RESOURCE_EXHAUSTED` — a **per-minute** rate limit
(5 requests/minute on the free tier), distinct from the **daily** budget EPIC-14
already guards. `SearchCompaniesHandler`'s bounded-concurrency fan-out
(`max_concurrent_research`, default 6) can burst past a 5 RPM limit well before
the daily cap is reached. Not fixed here (out of Sprint 3 scope) — added to the
Risk Register below as a new backlog candidate (e.g. a token-bucket/RPM limiter
alongside the existing daily `AIBudgetGuard`).
Also observed: `.env`'s `GEMINI_MODEL` is currently `gemini-2.5-flash`, not
`gemini-3.5-flash` (which is what it was set to earlier in this project after the
"model no longer available" incident) — flagging since I didn't change it back
myself; worth confirming whether that reversion was intentional.

### EPIC-01 — Evidence Model v2 (8 pts) · Track 1 · `[x]` Done — Sprint 4

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 1.1 | As the platform, I want evidence tagged by scope so industry noise can't fake company-level confidence | `EvidenceItem` gets `signal_scope: "company_specific" \| "industry_general"` | 3 | `[x]` Done |
| 1.2 | As the platform, I want evidence dated so recency can be judged | `EvidenceItem` gets `source_date`/`observed_date` | 2 | `[x]` Done |
| 1.3 | As a reviewer, I want `CONFIRMED_NEED` to require real company-specific evidence | `classify_evidence()` requires `confirmed_company_specific_count >= 2`, not just `confirmed >= 2` regardless of scope; regression test: an all-industry evidence set can never classify above `STRONG_COMPANY_SIGNAL` | 3 | `[x]` Done |

Shipped as: `EvidenceItem.signal_scope` (defaults to the conservative
`"industry_general"` so unclassified evidence is never mistaken for proof) and
`EvidenceItem.observed_date`, both populated by `TavilyEvidenceAdapter` at gather
time; `EvidenceSignalExtractor.classify_scope()` (new) does the actual
company-name-match classification; `classify_evidence()` now takes optional
`company_specific_signals`/`company_specific_evidence_count` and **only** reaches
`"Confirmed Need"` when those are supplied and sufficient — callers that don't
pass them (i.e. don't know the scope) can never reach it, which is the safe
default, not the permissive one.

**Naming note:** story 1.3's AC text referenced the architecture doc's
illustrative 6-tier ladder (`STRONG_COMPANY_SIGNAL`, etc.). The shipped code kept
the actual, already-existing 4-tier names (`"Confirmed Need"` / `"Strong
Opportunity Signal"` / `"Reasonable Business Hypothesis"` / `"Unverified
Assumption"`) rather than introducing a parallel naming scheme — renaming the
enum wasn't itself a committed backlog item. The regression test asserts the
equivalent claim against the real tier name: an all-industry-general evidence set
can never classify above `"Strong Opportunity Signal"`.

**Deliberately not done this sprint:** `_evidence_text()` in
`company_research_mapper.py` still says "Public sources show **company-specific**
signals..." even though the underlying `signals` dict it describes is still
combined-text (not scope-filtered) — this prose predates Sprint 4 and was already
slightly overclaiming; fixing the wording is a small follow-up, not part of the
committed 1.1–1.3 scope. `SearchCompaniesHandler` doesn't use `evidence_date` vs.
`observed_date` differently anywhere yet either (`observed_date` is populated and
available, not yet consumed downstream).

Live-verified: `TavilyEvidenceAdapter.gather()` against real Tavily (Tata Motors)
returned 8 real evidence items, all correctly tagged `signal_scope=company_specific`
with `observed_date` populated, proving the classification runs against live data,
not just mocks.

### EPIC-02 — Company Universe cheap-discovery tier (13 pts) · Track 1 · `[x]` Done — Sprint 5

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 2.1 | As the platform, I want a discovery port distinct from live web search | New `CompanyDirectoryPort` (application layer) | 2 | `[x]` Done |
| 2.2 | As the platform, I want at least one cheap structured-source adapter | One concrete adapter (registry/directory source, or a cached/batched directory-page miner reusing `TavilyDiscoveryAdapter._extract_directory_candidates`) | 8 | `[x]` Done |
| 2.3 | As the platform, I want the cheap tier tried before the expensive one | `SearchCompaniesHandler` calls `CompanyDirectoryPort` first; falls back to `CompanyDiscoveryPort` (Tavily) only when the cheap tier doesn't fill the candidate pool | 3 | `[x]` Done |

No paid registry/government API is available, so shipped the AC's own suggested
fallback: `TavilyDirectoryAdapter` (new `CompanyDirectoryPort` implementation) that
**only** harvests structured directory/listing pages via `TavilyDiscoveryAdapter`'s
existing `_discovery_metadata`/`_extract_directory_candidates` classmethods (reused
directly, not duplicated) — unlike the expensive tier, it never falls back to
treating a single search result as one candidate, which is what keeps its
candidates-per-Tavily-call ratio high. Added an in-memory cache keyed by
`(industries, geography, company_size)` with a configurable TTL
(`AI_DAILY_REQUEST_BUDGET_*`-style setting: `directory_cache_ttl_seconds`, default
3600s) so repeated requests for the same sector/region don't re-query Tavily at
all. `SearchCompaniesHandler` gained a `directory_port` constructor param
(`None`-safe, regression-tested) and a `_discover_candidates()` helper: cheap tier
first, expensive tier only when the cheap tier returns fewer candidates than
`request.number_of_companies` — results are simply concatenated, since
`DiscoveryFunnel.gate_candidates()` already deduplicates downstream (no new dedup
logic needed).

**Wiring note:** the directory adapter is registered as a **singleton** in
`dependencies/company_research.py` (`get_directory_adapter`, mirroring the existing
`get_database_engine`/`get_session_manager` module-global pattern) — a per-request
instance would reset the in-memory cache on every call and defeat its entire
purpose.

Live-verified against real Tavily: first call for Manufacturing/India took 3.85s
and returned 18 real candidates from directory-page mining; an immediate repeat
call for the same request returned the identical list in 0.0001s from cache
(confirmed same object identity, zero new Tavily calls). One of the 18 live
candidates had a garbled name (an HTML filename fragment concatenated into the
company name) — this is the pre-existing `_extract_directory_candidates` row
parser (reused as-is, not modified this sprint), and directly confirms the
already-tracked "Discovery precision ceiling" risk below rather than introducing a
new one; EPIC-17 (Enrichment Waterfall) remains the right place to improve
directory-row parsing quality.

### EPIC-03 — Entity Resolution → canonical `Company` (13 pts) · Track 1 · `[x]` Done — Sprint 6

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 3.1 | **Decision gate:** opt-in `persist_as_companies` flag vs. always-on | Resolved per architecture doc §11 decision #1 before this epic starts | 1 | `[x]` Done — **opt-in**, confirmed with user before starting |
| 3.2 | As the platform, I want candidates normalized and matched against existing companies | Normalize name+website; check `CompanyRepository` for an existing match before creating | 5 | `[x]` Done |
| 3.3 | As the platform, I want a new `Company` created only when no match exists | Wired through the existing `CreateCompanyHandler`/`company_commands` path | 4 | `[x]` Done |
| 3.4 | As a QA reviewer, I want re-running the same search to not duplicate companies | Dedup regression test: same search run twice → same `Company` row count | 3 | `[x]` Done |

Shipped `CompanyResearchRequest.persist_as_companies: bool = False` (opt-in, per
the confirmed decision) and `CompanySearchResult.persisted_company_id: str | None`.
New `PromoteCandidateToCompanyHandler` (application layer, the first
company_research component to own a `UnitOfWork`) resolves entity identity in two
steps: match by **normalized website** first (more reliable than name — names vary
across sources, domains usually don't), then fall back to the existing
`CreateCompanyHandler`'s own name-based duplicate check (catching its
`ConflictException` and resolving to the existing row rather than treating it as
an error). A new `Company` is created only when neither check finds a match.
`SearchCompaniesHandler` calls this only for the final, truncated result set, and
only when `persist_as_companies=True` — persistence failures are logged and
swallowed per-candidate so a DB hiccup never breaks the research response itself.

**Repository extension:** added `find_by_website()` to `CompanyRepository`
(interface + `SqlAlchemyCompanyRepository`) — a small, additive query method on an
"Architecture Freeze v5.0"-labeled interface. Judgment call: interpreted the freeze
as protecting transaction/aggregate boundaries (matching how AI was deliberately
excluded from `UnitOfWork` earlier), not as forbidding any new query method on an
actively-maintained, single-implementer interface. Flagging the interpretation
here rather than treating it as an unremarkable change.

Live-verified against the **real production database** (not just the in-memory
test fixture): a real `/company-research/search?persist_as_companies=true` call
created a genuine `Company` row for Samsung India Electronics with a correctly
normalized website (`https://www.samsung.com/in/business/info/legal` →
`https://samsung.com`) and correctly mapped industry ("Manufacturing"). Re-running
`PromoteCandidateToCompanyHandler` for the same candidate against the same real DB
resolved to the identical company id, with the row count confirmed still at 1.

### EPIC-04 — AI Solution Catalog + fix `generate_recommendation` (13 pts) · Track 1 · `[x]` Done — Sprint 7

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 4.1 | As the platform, I want the AI Solution Catalog as structured data | New `SolutionCatalogEntry` value object; seeded from Appendix A of the architecture doc (sector, pain point, `SolutionType`, catalog-offering vs. generic-opportunity flag) | 5 | `[x]` Done |
| 4.2 | As a sales rep, I want `generate_recommendation` to actually generate something | ~~`GenerateRecommendationHandler` calls `AIExecutionService`~~ **`CreateRecommendationHandler`** calls `AIExecutionService` with Assessment findings + matched catalog entries, populates real `Solution` entries | 5 | `[x]` Done (target handler changed — see finding below) |
| 4.3 | As the platform, I want one catalog, not two | `OpportunityMapper` in company_research reads the same catalog instead of its own hardcoded list | 3 | `[x]` Done |

**Major finding: the `recommendation` module has two parallel, disconnected
implementations.** Investigating story 4.2 surfaced that `GenerateRecommendationHandler`
(the handler this story originally named) was never reachable at all:
`recommendation_router.py` has no `/generate` route, no DI dependency was ever
wired for it, and it calls `recommendation_repository.get_by_assessment(...)` — a
method that **does not exist** on the real, concrete repository (the real one is
`get_by_assessment_id`). It could never have run successfully even if wired. The
same "second universe" pattern extends further than this one handler:
`app/application/recommendation/{handlers,commands,validators,mappers}/__init__.py`
each contain **inline, fully-duplicate class definitions** (e.g. a second
`UpdateROIHandler`) built against a *different*, domain-layer
`RecommendationRepository` interface (`app/domain/recommendation/repositories/`)
that has no concrete implementation anywhere. Several standalone handler files
(`add_solution_handler.py`, `submit_recommendation_handler.py`,
`approve_recommendation_handler.py`, `update_roi_handler.py`, ...) and DTOs
(`solution_dto.py`, `mappers/solution_mapper.py` — which itself references fields
that don't exist on the real `Recommendation` entity) belong to this same
unreachable universe. `tests/domain/recommendation/test_recommendation.py` and
`tests/application/recommendation/handlers/test_reject_recommendation_handler.py`
are both **empty files** (0 bytes); the existing `FakeRecommendationRepository`
test double is built against the dead domain-layer interface too — meaning the
pre-existing recommendation test suite was entirely testing (or rather, not
testing) code nothing can reach.

**Decision:** rather than fix a handler nothing calls, the AI generation work went
into `CreateRecommendationHandler` — the only recommendation handler actually
reachable via `POST /recommendations`, which previously just set a hardcoded
`executive_summary="Recommendation generated successfully."` string (a lie) and
saved an empty shell. Deleted the three files most directly superseded
(`generate_recommendation_handler.py` + its command + validator — confirmed zero
callers). Left the broader "Universe B" mess (the `__init__.py` duplicates, the
other orphaned handlers, `solution_mapper.py`) untouched — it's real, substantial,
separate cleanup, not a Sprint 7 side quest. **New backlog candidate:** a dedicated
cleanup epic for the whole `recommendation` module (needs its own scoping).

**Second, smaller finding:** `RecommendationModel` had **no column to persist
`solutions` at all** — even a correctly-populated `Recommendation.solutions` list
would silently vanish on save/reload. Added a `solutions` `TEXT` column
(JSON-serialized) + mapper serialization, and applied a one-time `ALTER TABLE` to
the existing local `aisdr.db` (fresh/test DBs get the column automatically via
`create_all()`, matching the established pattern from EPIC-14's `ai_usage_log`
table). Also enriched `RecommendationDTO.solutions` from `list[str]` (titles only)
to full `SolutionSummaryDTO` objects (title/description/type/priority/
`is_existing_offering`) — a bare title string would have made the AI-generated
detail invisible to API callers, which defeats the point of this story.

**Bug caught by my own test, before it shipped:** the "assessment has no content"
guard (`_generate_solutions`) initially could never trigger, because
`Assessment.maturity_level` defaults to `MaturityLevel.INITIAL` (never `None`), so
the context-assembly string was never actually empty. Fixed by checking the
meaningful text fields (`summary`/`strengths`/`weaknesses`/`opportunities_summary`/
`risks`) directly rather than the full assembled prompt string.

**Catalog design:** `SolutionCatalogEntry` (new, in `app/domain/recommendation/`)
has two kinds of entries — `is_existing_offering=True, sector="general"` for the 5
real Pamacore service lines (each carrying `signals` so `OpportunityMapper` can
still match deterministically), and `is_existing_offering=False, sector=<specific>`
for sector-appropriate generic ideas seeded from Appendix A, covering the same 9
sectors as Track 1 Phase 0's Domain Profiles (31 entries total). Two sectors
(Logistics, Construction) weren't in the architecture doc's original Appendix A
table — seeded reasonable, defensible entries for them using the doc's own "wedge
offer" pattern (content-gen / chatbot / reporting-automation) rather than leaving
gaps; flagging this honestly rather than claiming a literal, complete Appendix A
transcription. Remaining Appendix A sectors not seeded are a low-risk, data-only
follow-up, not blocking.

`OpportunityMapper.map_signals()` now takes an optional `catalog` parameter and
reads from it; when omitted, a domain-owned default (identical in content to
`general.json`) preserves exact prior behavior — same "default profile, optional
injected override" pattern as `IndustryClassifier`/`IcpMatcher` from Track 1 Phase
0, verified byte-identical against the old hardcoded output for every existing
test case. In production, `SearchCompaniesHandler` now receives the real loaded
catalog via DI, so there is genuinely one source of truth in practice.

**Live-verified end-to-end against the real app, real DB, and real Gemini** (not
mocks): built a full Company → Contact → Lead → Discovery → Assessment chain via
the real API, then called `POST /recommendations`. Gemini correctly matched
"Business Process Automation" from the real catalog (`is_existing_offering: true`)
against the assessment's manual-workflow weakness, and proposed two sector-
appropriate generic ideas not in the catalog ("ERP-Finance Integration Solution",
"Automated Financial Reporting"), both correctly labeled
`is_existing_offering: false` — exactly the architecture doc's §7 recommendation
order (map to catalog first, propose generic only when nothing fits, always label
which is which). A fresh `GET /recommendations/{id}` in a separate call confirmed
all three solutions round-tripped through the real database with full detail.

### EPIC-05 — Contact Discovery (8 pts) · Track 1 · `[x]` Done — Sprint 8

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 5.1 | As the platform, I want a contact-discovery port + adapter | New `ContactDiscoveryPort`, Tavily-backed adapter | 5 | `[x]` Done |
| 5.2 | As the platform, I want contact discovery gated by qualification score | Adapter never invoked below `minimum_qualification_score`; role targeting driven by the EPIC-04 catalog match | 3 | `[x]` Done |

**Decision gate resolved before starting:** the existing, unimplemented
`app/application/contracts/services/contact_discovery_service.py` contract
(flagged in the Parking Lot below before Sprint 7) was left untouched, and a
new company_research-specific `ContactDiscoveryPort` was built instead,
matching `CompanyDiscoveryPort`/`IdentityVerificationPort`/`EvidenceResearchPort`'s
existing pattern. Confirmed with the user first; the shared-contract
generalization remains a Parking Lot candidate if another module needs
contact discovery later, not a Sprint 8 side quest.

Shipped `ContactDiscoveryPort` (`discover(candidate, website, target_role) ->
list[DiscoveredContact]`) and `TavilyContactDiscoveryAdapter` — searches for
the candidate's public LinkedIn profiles, filters to genuine
`linkedin.com/in/...` profile URLs (never a company page or unrelated
result), and parses the standard "Name - Title - Company | LinkedIn"
search-result title format into a name + observed role title. No profile
found means an empty list, never a fabricated contact -- same
never-guess discipline as `IdentityVerificationPort`.

**Gating (story 5.2):** wired into `SearchCompaniesHandler._research_candidate`
*after* qualification scoring, checked against `request.minimum_qualification_score`
before the port is ever called -- so a sub-threshold candidate costs zero
contact-discovery Tavily calls, not just a discarded result. Role targeting
reuses `CompanySearchResult.decision_maker_role`, which Sprint 7's
`OpportunityMapper`/catalog match already computes -- no new role-inference
logic needed, just threading the existing value into the new port call.

**Response shape (frontend-facing, per user direction on 2026-08-15 --
see the architecture doc's framing on future frontend consumption):** added
`CompanySearchResult.discovered_contacts: list[DiscoveredContact]` (name,
role_title, linkedin_url, source_url) rather than only overloading the
pre-existing singular `decision_maker_name`/`public_contact_channel` fields
-- follows the same "richer list alongside the existing singular field"
pattern already used for `sources`/`discovery_metadata`. The singular
`decision_maker_name` is still populated (from the first discovered contact)
so existing consumers of that field keep working unchanged.

Live-verified against real Tavily end-to-end (discovery -> evidence ->
scoring -> contact discovery); Gemini identity verification was substituted
with a scripted trust-the-verified-website stub for this one smoke test
only, since the real Gemini key had already hit its free-tier **daily** quota
from earlier live testing today (a pre-existing, already-tracked constraint,
not a new one) -- same workaround Sprint 4 used for the same reason. For a
real qualifying candidate ("Jabil", score 74), the adapter found a genuine
LinkedIn profile (`May Yap`, `linkedin.com/in/may-yap-77997311`) and
populated both `discovered_contacts` and `decision_maker_name`. For two
other candidates that were pre-existing discovery-tier noise (tracked under
the "Discovery precision ceiling" risk, EPIC-17 -- not introduced this
sprint), contact discovery correctly returned an empty list instead of
fabricating a person, confirming the never-guess contract holds under real
data.

### EPIC-06 — Lead creation bridge (8 pts) · Track 1 · `[x]` Done — Sprint 9

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 6.1 | As the platform, I want to distinguish research-originated leads | Add `AI_RESEARCH` (or similar) value to `LeadSource` | 1 | `[x]` Done |
| 6.2 | As the platform, I want qualified candidates to become real Leads | For candidates above threshold: create `Company` (EPIC-03) + `Contact` (EPIC-05) + `Lead`, carrying score/hypothesis/evidence as metadata | 5 | `[x]` Done — see decision gate below |
| 6.3 | As a QA reviewer, I want the full chain covered end-to-end | E2E test: one candidate above threshold → exactly one Company, one Contact, one Lead; no duplicates on rerun | 2 | `[x]` Done |

**Decision gate resolved before starting (real, not hypothetical):**
investigating story 6.2 found that `Lead.contact_id` is mandatory and
`Contact.email` is a mandatory, validated field -- but Sprint 8's
`DiscoveredContact` (LinkedIn-sourced) never carries an email, since
LinkedIn search results don't expose one. Two options were laid out for the
user: (A) pattern-guess an email (`firstname.lastname@domain`, the
Apollo/Hunter.io convention) and flag it as unverified only via the Lead's
free-text `notes`, or (B) only create Contact/Lead when a real, verified
email actually exists somewhere in the pipeline -- which today is never, so
the bridge ships fully tested but produces zero live Leads until EPIC-17
adds a real email source. **Chose (B)**, confirmed with the user, for
consistency with this module's existing never-fabricate discipline
(`IdentityVerificationPort`, `ContactDiscoveryPort`) and because a guessed
value in a *mandatory* schema field is a sharper foot-gun than the guesses
this system already refuses to make elsewhere -- a future engagement
send-path (Track 2) reading `Contact.email` directly wouldn't know to check
`Lead.notes` first.

Shipped `LeadSource.AI_RESEARCH` (story 6.1) and
`PromoteCandidateToLeadHandler` (story 6.2, mirrors Sprint 6's
`PromoteCandidateToCompanyHandler` shape) -- resolves/creates a Contact by
email (via `ContactRepository.find_by_email`, catching `CreateContactHandler`'s
`ConflictException` the same way company promotion catches its own), then
resolves/creates a Lead (deduplicated via `LeadRepository.list(company_id,
contact_id)`, no new repository method needed -- that filter combination
already existed), with `notes` carrying qualification score, priority tier,
business-problem hypothesis, evidence summary, and trigger event -- literally
the free-text field this schema already has for exactly this purpose, so no
new column was needed (unlike EPIC-04's `solutions` gap). Wired into
`SearchCompaniesHandler._promote_results` right after company promotion
succeeds, gated by the same `persist_as_companies` flag rather than a new
one -- judgment call, documented here: this is the same "materialize this
research result as CRM data" opt-in, not a separate decision, and since
Contact/Lead creation is a no-op without a real email today, the practical
blast radius of reusing the flag is zero live behavior change. `DiscoveredContact`
gained an optional `email` field (always `None` from the current LinkedIn
adapter) so a future enrichment source has somewhere to put a verified
address without another DTO change. `CompanySearchResult` gained
`persisted_contact_id`, `persisted_lead_id`, and
`lead_creation_skipped_reason` -- the last one exists specifically so the
"nothing happened" outcome is visible in the API response, not silent.

**Story 6.3 E2E dedup test:** since no real email exists live, the test
supplies one on the `DiscoveredContact` fixture (documented in the test's
own docstring as simulating a future email source) and runs the real
`PromoteCandidateToCompanyHandler` → `PromoteCandidateToLeadHandler` chain
against a real in-memory DB twice: exactly one Company, one Contact, one
Lead row after both runs, proving the bridge mechanism itself -- independent
of today's missing-email gap.

**Live-verified against real Tavily and the real production DB:** a real
`persist_as_companies=true` search created three genuine Company rows.
Contact discovery found two real LinkedIn profiles (no emails, as expected).
All three results correctly reported `lead_creation_skipped_reason:
"no_verified_email_found"` with `persisted_contact_id`/`persisted_lead_id`
both `None` -- confirmed directly against the database that zero Contact/Lead
rows were created by this run (the 3 existing rows found belong to Sprint
7's live-verification chain, timestamped earlier the same day). Exactly the
dormant-but-honest behavior Option B was chosen for.

### EPIC-08 — Workflow orchestration (8 pts) · Track 1 · `[x]` Done — Sprint 10

| ID | Story | Acceptance Criteria | Pts | Status |
|---|---|---|---|---|
| 8.1 | As an operator, I want the DISCOVER→...→LEAD chain observable per candidate | ~~Wrap it as a `Workflow`/`WorkflowStep` execution reusing `app.domain.workflow`~~ **New `CompanyResearchBatchResult` envelope** (`results` + `failures`), each failure tagged with the pipeline step that crashed | 5 | `[x]` Done (target module changed — see finding below) |
| 8.2 | As an operator, I want failures to be resumable, not silently dropped | `PipelineStepFailure` distinguishes a crash from a legitimate disqualification; `POST /company-research/retry` re-runs one failed candidate without re-discovery | 3 | `[x]` Done |

**Finding, before any code was written:** `app.domain.workflow` (the module
story 8.1 named) turned out to be complete, coherent-looking domain
scaffolding -- `Workflow` aggregate, `WorkflowStep`, `WorkflowExecution`,
validation/execution services, all the right enums -- but **entirely
unwired**: zero application-layer usage, zero persistence, zero router, zero
tests, and zero references anywhere else in the codebase (confirmed by
`grep`). It also has its own internal defect nothing ever caught: two
separate, functionally-identical `WorkflowId` classes live in different
subpackages of the same unused module
(`value_objects/workflow_id.py` and `identifiers/workflow_id.py`). Beyond
being unused, its shape doesn't fit this use case either --
`WorkflowRepository` is a **synchronous** ABC (`def save`, not `async def`)
in an otherwise fully-async codebase, and `WorkflowStep` has no field for
which candidate it belongs to or what step-specific data it produced.
Presented the tradeoffs to the user (fix-and-adopt vs. build purpose-fit
tracking) before writing anything -- same discipline as the EPIC-05 and
EPIC-06 decision gates. **Chose purpose-fit tracking**; `app.domain.workflow`
is untouched and moved to the Parking Lot below as unused/inconsistent
scaffolding needing its own cleanup decision, same treatment as the
`recommendation` module's dead "Universe B" and the orphaned `AIRequestModel`
stack found in earlier sprints.

**What shipped instead:** the actual bug named in story 8.2's AC --
`SearchCompaniesHandler._research`'s blanket `except Exception: return None`
made a genuine crash (a Tavily network error, a provider outage) look
*identical* to a candidate that was correctly checked and just doesn't
qualify (wrong industry, unverified identity, ...). Both silently vanished
from the response the same way, with only a log line to tell them apart.
Fixed by wrapping the two real I/O boundaries in `_research_candidate`
(`IdentityVerificationPort.verify`, `EvidenceResearchPort.gather`) so an
unexpected exception raises `PipelineStepFailure` tagged with a
`PipelineStep` (`identity_verification` / `evidence_gathering` / `unknown`
as a defensive fallback for anything else), caught at the per-candidate
`asyncio.gather` boundary and converted into a `CandidateResearchFailure`
DTO -- carrying the original candidate's discovery fields so it can be
retried without paying for a fresh Tavily query. Deterministic disqualifying
branches (`return None` for low identity confidence, industry mismatch,
size mismatch, ...) are completely unchanged and still resolve to "just not
in `results`," exactly as before -- only genuine crashes changed behavior.

**Public API contract change (documented, not snuck in):**
`POST /company-research/search`'s response changed from a bare
`CompanySearchResult[]` array to `{results: [...], failures: [...]}`. This is
the natural, honest shape for the fix -- crashed candidates need somewhere
to be visible that isn't silently indistinguishable from a legitimate
rejection -- and keeps the frontend-consumability direction from Sprint 8/9
(flat, typed, no hidden gaps) rather than overloading the existing array
with a sentinel value. New `POST /company-research/retry` endpoint accepts
one `CandidateResearchFailure` + the original request and re-runs just that
candidate.

**Live-verified against real Tavily, real discovery, one real simulated
step failure:** ran a real discovery batch, then made the evidence step
genuinely raise for one specific real candidate (simulating a Tavily
outage) while the other three proceeded normally. `failures` correctly
contained exactly the one crashed candidate, tagged `evidence_gathering`
with the real error message; `results` correctly contained the other three,
unaffected. Retrying the failed candidate via `retry_candidate()` -- with no
new discovery call -- succeeded and produced a real qualified result (score
74), concretely proving the resumability claim rather than just asserting a
flag exists.

**Second, unrelated finding surfaced during live verification:** the real
Gemini identity adapter (`AiIdentityVerificationAdapter`) is already
correctly defensive -- it catches its own provider errors internally and
returns a `LOW`-confidence result rather than raising, per its existing
"never silently upgrade to a match" contract, so it couldn't be used to
demonstrate a step failure organically. But every real call against it
today returns a **new, more serious error**: `404 NOT_FOUND: models/
gemini-2.5-flash is no longer available to new users` -- a model
deprecation, not the daily-quota `RESOURCE_EXHAUSTED` seen in Sprints 8-9.
Not fixed here (out of this sprint's scope); flagged to the user directly
and added to the Risk Register below, since every future sprint needing a
live Gemini call will hit this until `.env`'s `GEMINI_MODEL` is updated to a
currently-supported model.

### EPIC-17 — Enrichment waterfall (8 pts) · Track 5

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 17.1 | As the platform, I want a fallback order behind the discovery/enrichment ports | Cheap structured source (EPIC-02) → Tavily → room for a future paid enrichment API, same port contract | 5 |
| 17.2 | As a QA reviewer, I want measurably fewer junk candidates | Regression test set using known-bad candidates from live testing ("Company search", "Browse by size...") — all rejected pre-research | 3 |

**Load-bearing for EPIC-06, not just discovery quality:** whatever real
paid enrichment source story 17.1 adds should also be checked for whether it
can populate `DiscoveredContact.email` (added in Sprint 9, currently always
`None`) -- that's the one missing piece keeping `PromoteCandidateToLeadHandler`
dormant in live use. See the Risk Register entry and EPIC-06's notes above.

### EPIC-16 — Human-in-the-loop review queue & explainability (13 pts) · Track 4

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 16.1 | As a sales rep, I want to see the full evidence → hypothesis → recommendation → message chain before anything sends | New review state on `Lead`/`Sequence`: `pending_review → approved → sent`; API/UI surface for the chain | 8 |
| 16.2 | As a sales rep, I want to approve, edit, or reject before send | Edit/reject actions persisted (feeds EPIC-12 later) | 3 |
| 16.3 | As the platform, I want nothing auto-sent while this gate is active | Enforcement test: no Track 2 send path can bypass `pending_review` | 2 |

### EPIC-09 — Multichannel sequencing engine (21 pts) · Track 2

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 9.1 | As the platform, I want a `Sequence` aggregate | New `app/domain/sequence`: ordered touches (email/LinkedIn/call-task), wait-time rules, branch on reply/no-reply/bounce | 8 |
| 9.2 | As a sales rep, I want each touch to say something different, not repeat itself | Touch generation varies angle per step (signal-led opener → different proof point → breakup message), grounded in Lead evidence | 8 |
| 9.3 | As the platform, I want channel adapters | Email adapter (SMTP/provider API) at minimum; LinkedIn/call-task per the "engagement channels" decision in the architecture doc | 5 |

### EPIC-10 — Reply intelligence & meeting booking (13 pts) · Track 2

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 10.1 | As the platform, I want inbound replies classified | New `ReplyClassificationPort`: interested / not now / objection / unsubscribe / OOO / wrong person | 5 |
| 10.2 | As a prospect, I want a fast, correct scheduling reply when I say yes | On "interested": suggest meeting times (calendar integration) + draft scheduling reply | 5 |
| 10.3 | As the platform, I want Lead status to reflect real engagement | `Lead.status`/`LeadScore` updated from classified replies, not only internal qualification | 3 |

### EPIC-11 — Deliverability & compliance (13 pts) · Track 2

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 11.1 | As the platform, I want a persisted do-not-contact list checked before every send | New suppression list; every send path checks it first | 5 |
| 11.2 | As the platform, I want bounce/complaint handling | Auto-suppress on bounce/complaint webhook | 3 |
| 11.3 | As the platform, I want jurisdiction-aware consent rules | Compliance ruleset keyed off `CompanyResearchRequest.geography`/Lead's company geography (CAN-SPAM/GDPR/TCPA variants) | 5 |

### EPIC-12 — Outcome feedback loop (13 pts) · Track 3

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 12.1 | As the platform, I want outcomes persisted against the originating Lead | New `OutcomeEvent` (meeting_booked / won / lost / no_response) | 5 |
| 12.2 | As an operator, I want a periodic recalibration pass | Offline job reviewing which evidence types correlated with booked meetings, feeding back into `QualificationScorer` weights per Domain Profile | 8 |
| **—** | **Milestone gate, not dev effort** | This epic's dev work can complete in Sprint 17, but Story 12.2 needs 2–4 weeks of live pipeline usage generating real outcomes before recalibration produces anything meaningful. Track as a calendar gate, not sprint capacity. | — |

---

## Parking Lot — Track 6 (as-needed, not sequenced)

Not estimated or scheduled. Pull into the backlog only when triggered by a concrete
need (see architecture doc §14 for full rationale):

- **Multi-tenancy** (`tenant_id` boundary) — pull forward before EPIC-03 if
  multi-tenant becomes a near-term reality; expensive to retrofit after data exists.
- **Data retention & PII policy** — needed before EPIC-05 goes live at real volume.
- **Audit logging** — needed for any regulated-industry customer (Healthcare/Pharma/
  Financial Services are explicit target domains).

## Parking Lot — unscoped cleanup candidates (found during delivery, not yet estimated)

- **`recommendation` module "Universe B" cleanup** (found Sprint 7) — an entire
  parallel, unreachable set of handlers/commands/validators/mappers
  (`__init__.py`-inlined duplicates + standalone orphans, built against a
  domain-layer `RecommendationRepository` with no concrete implementation).
  Needs its own scoping pass before touching — likely 8-13 points on its own.
- **`ContactDiscoveryService` generalization** (found before Sprint 7,
  resolved for Sprint 8) — an unimplemented contact-discovery contract sits
  in `app/application/contracts/services/`. Decided (2026-08-15, confirmed
  with the user) to ship EPIC-05 as a new company_research-specific
  `ContactDiscoveryPort` instead, matching the module's existing port
  pattern. The shared contract remains unimplemented; revisit only if
  another module (not just company_research) actually needs contact
  discovery -- don't generalize speculatively.
- **`complete_assessment_handler.py`** (found before Sprint 7) — completely empty
  file, no `/complete` route wired; assessment "completion" today only happens
  indirectly via the generic update endpoint.
- **`app/domain/workflow` cleanup** (found Sprint 10) — a complete-looking
  `Workflow`/`WorkflowStep`/`WorkflowExecution` domain module with validation
  and execution services, but entirely unwired (no application layer, no
  persistence, no router, zero tests, zero references anywhere else in the
  codebase) and internally inconsistent (two duplicate `WorkflowId` classes
  in different subpackages of the same unused module). `WorkflowRepository`
  is also a synchronous ABC, inconsistent with every other repository in
  this async-throughout codebase. EPIC-08 was originally planned to reuse it;
  built purpose-fit tracking instead (see EPIC-08 notes above). Needs its own
  scoping pass (fix-and-adopt vs. delete) before anything else touches it.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Owning epic |
|---|---|---|---|---|
| AI provider model deprecation breaks a live batch (already happened twice this session) | High | Medium | Health checks + fallback | EPIC-13 |
| AI quota/billing exhaustion mid-batch (already happened this session) | ~~High~~ Mitigated | Medium | Budget tracking + pre-flight check — `[x]` shipped Sprint 2, live-verified | EPIC-14 |
| Config drift (stale env var shadowing `.env` — already happened this session) | Medium | Low-Medium | Diagnostics endpoint | EPIC-15 |
| Autonomous outreach sends something wrong/off-brand | Medium | High | Review queue gate before EPIC-09 | EPIC-16 |
| Compliance violation (CAN-SPAM/GDPR/TCPA) from real outbound volume | Low-Medium | High (legal) | Suppression list + jurisdiction rules before real volume | EPIC-11 |
| Discovery precision ceiling (junk candidates observed in live testing; reconfirmed Sprint 5 with a garbled directory-row name) | High | Low-Medium | Cheap tier `[x]` shipped Sprint 5; row-parsing quality still needs EPIC-17 | EPIC-02, EPIC-17 |
| **New (Sprint 3):** Gemini per-minute rate limit (5 RPM free tier) distinct from the daily budget — concurrent fan-out can burst past it | High | Medium | Not yet mitigated — daily `AIBudgetGuard` doesn't cover RPM; needs a token-bucket/RPM limiter | Unscheduled — candidate for a Track 4 fast-follow |
| **New (Sprint 9):** Lead creation bridge (EPIC-06) is fully shipped and tested but produces zero live Leads until a real email-enrichment source exists -- public LinkedIn discovery (EPIC-05) never surfaces an email, and `PromoteCandidateToLeadHandler` deliberately never guesses one | High (today) | Low (by design -- honest gap, not a bug) | Mitigated once EPIC-17 (Enrichment waterfall) adds a real email source; `lead_creation_skipped_reason` makes the gap visible via the API rather than silent | EPIC-17 |
| **New (Sprint 10):** Configured Gemini model (`gemini-2.5-flash`) now returns `404 NOT_FOUND: ... no longer available to new users` on every real call -- a model deprecation, not the previously-tracked daily-quota/RPM limits | High | High (blocks every live AI call, not just a batch) | Not yet mitigated -- needs `.env`'s `GEMINI_MODEL` updated to a currently-supported model | Unscheduled — candidate for an urgent Track 4 fast-follow |
| Solo+AI velocity estimate is wrong | Medium | Medium (schedule slip, not scope loss) | Recalibrate after Sprint 2–3 actuals (see sprint plan) | — |
| Scope creep beyond committed 17 epics | Medium | Medium | MoSCoW priority + Parking Lot boundary enforced | — |
