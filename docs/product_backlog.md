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
| `[ ]` Backlog | EPIC-05 | 1 | Contact Discovery | 8 | **M** | EPIC-03, EPIC-04 |
| `[ ]` Backlog | EPIC-06 | 1 | Lead creation bridge | 8 | **M** | EPIC-05 |
| `[ ]` Backlog | EPIC-08 | 1 | Workflow orchestration | 8 | **S** | EPIC-06 |
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

### EPIC-05 — Contact Discovery (8 pts) · Track 1

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 5.1 | As the platform, I want a contact-discovery port + adapter | New `ContactDiscoveryPort`, Tavily-backed adapter | 5 |
| 5.2 | As the platform, I want contact discovery gated by qualification score | Adapter never invoked below `minimum_qualification_score`; role targeting driven by the EPIC-04 catalog match | 3 |

### EPIC-06 — Lead creation bridge (8 pts) · Track 1

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 6.1 | As the platform, I want to distinguish research-originated leads | Add `AI_RESEARCH` (or similar) value to `LeadSource` | 1 |
| 6.2 | As the platform, I want qualified candidates to become real Leads | For candidates above threshold: create `Company` (EPIC-03) + `Contact` (EPIC-05) + `Lead`, carrying score/hypothesis/evidence as metadata | 5 |
| 6.3 | As a QA reviewer, I want the full chain covered end-to-end | E2E test: one candidate above threshold → exactly one Company, one Contact, one Lead; no duplicates on rerun | 2 |

### EPIC-08 — Workflow orchestration (8 pts) · Track 1

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 8.1 | As an operator, I want the DISCOVER→...→LEAD chain observable per candidate | Wrap it as a `Workflow`/`WorkflowStep` execution reusing `app.domain.workflow` | 5 |
| 8.2 | As an operator, I want failures to be resumable, not silently dropped | A failed step leaves the Workflow in a resumable/failed state instead of `SearchCompaniesHandler._research` swallowing the exception | 3 |

### EPIC-17 — Enrichment waterfall (8 pts) · Track 5

| ID | Story | Acceptance Criteria | Pts |
|---|---|---|---|
| 17.1 | As the platform, I want a fallback order behind the discovery/enrichment ports | Cheap structured source (EPIC-02) → Tavily → room for a future paid enrichment API, same port contract | 5 |
| 17.2 | As a QA reviewer, I want measurably fewer junk candidates | Regression test set using known-bad candidates from live testing ("Company search", "Browse by size...") — all rejected pre-research | 3 |

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
- **`ContactDiscoveryService` reconsideration for EPIC-05** (found before Sprint 7)
  — an unimplemented contact-discovery contract already exists in
  `app/application/contracts/services/`. EPIC-05 was planned as a new
  company_research-specific port; worth deciding whether to implement *that*
  existing contract instead so contact discovery isn't company_research-private.
- **`complete_assessment_handler.py`** (found before Sprint 7) — completely empty
  file, no `/complete` route wired; assessment "completion" today only happens
  indirectly via the generic update endpoint.

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
| Solo+AI velocity estimate is wrong | Medium | Medium (schedule slip, not scope loss) | Recalibrate after Sprint 2–3 actuals (see sprint plan) | — |
| Scope creep beyond committed 17 epics | Medium | Medium | MoSCoW priority + Parking Lot boundary enforced | — |
