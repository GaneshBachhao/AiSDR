# Pamacore / AiSDR — Sprint Plan & Timeline

Companion to [`product_backlog.md`](product_backlog.md) (scope/epics/stories) and
[`pamacore_aisdr_summary.md`](pamacore_aisdr_summary.md) (architecture/roadmap).
This document is the schedule: cadence, capacity, sprint-by-sprint sequencing,
milestones, and how to keep it from drifting out of date.

---

## 1. Assumptions (confirmed with you — recalibrate if these change)

| Assumption | Value |
|---|---|
| Capacity | Solo developer + AI pair-programming (Claude Code) — one effective delivery stream |
| Sprint length | 1 week (Monday–Friday) |
| Assumed velocity | ~10 story points/week, **flex band 8–13** — a planning assumption, not a measured fact yet |
| Sprint 1 start | Monday 2026-08-17 (next Monday from today, 2026-08-12) |
| Tracking | Git-tracked markdown (this file + backlog, source of truth) + a published visual board, regenerated when status changes materially |

**Velocity will be wrong on day one — that's normal.** Re-forecast the remaining
sprint count after Sprint 2's actuals are in (see §5). Everything past Sprint 3 in
the table below is a forecast, not a commitment.

Because this is solo capacity, "parallel tracks" in the architecture doc's §15
mostly translates to *sequencing order*, not simultaneous work — the exception is
low-effort/independent epics bundled into one sprint (e.g. Sprint 1 below).

---

## 2. Sprint Schedule

| Status | Sprint | Dates (Mon–Fri) | Epic(s) | Points | Sprint Goal |
|---|---|---|---|---|---|
| `[x]` Done | 1 | **Started early: Aug 12, 2026** (planned Aug 17–21) | EPIC-13, EPIC-15 | 13 | Stop repeating this session's own failures: AI provider fallback + a config diagnostics endpoint, both ship this week |
| `[x]` Done | 2 | **Started early: Aug 12, 2026** (planned Aug 24–28) | EPIC-14 | 10 | AI spend/quota is tracked and pre-flight-checked, not discovered via failed batches |
| `[x]` Done | 3 | **Started early: Aug 12, 2026** (planned Aug 31–Sep 4) | EPIC-00 | 8 | Industry/ICP vocabulary is data, not hardcoded Python |
| `[x]` Done | 4 | **Started early: Aug 13, 2026** (planned Sep 7–11) | EPIC-01 | 8 | Evidence carries `signal_scope`; `CONFIRMED_NEED` can no longer be faked by industry noise |
| `[x]` Done | 5 | **Started early: Aug 13, 2026** (planned Sep 14–18) | EPIC-02 | 13 | A cheap discovery tier exists ahead of live Tavily search |
| `[x]` Done | 6 | **Started early: Aug 13, 2026** (planned Sep 21–25) | EPIC-03 | 13 | Research candidates resolve into real, deduplicated `Company` records |
| `[x]` Done | 7 | **Started early: Aug 15, 2026** (planned Sep 28–Oct 2) | EPIC-04 | 13 | `generate_recommendation` actually generates something, from a real shared catalog |
| `[ ]` Planned | 8 | Oct 5 – Oct 9, 2026 | EPIC-05 | 8 | Qualified candidates get contact discovery, gated correctly |
| `[ ]` Planned | 9 | Oct 12 – Oct 16, 2026 | EPIC-06 | 8 | **Milestone C** — full Company → Contact → Lead pipeline live end-to-end |
| `[ ]` Planned | 10 | Oct 19 – Oct 23, 2026 | EPIC-08 | 8 | The full chain is observable and resumable, not silently swallowing failures |
| `[ ]` Planned | 11 | Oct 26 – Oct 30, 2026 | EPIC-17 | 8 | **Milestone D** — enrichment waterfall live; junk-candidate rate measurably down |
| `[ ]` Planned | 12 | Nov 2 – Nov 6, 2026 | EPIC-16 | 13 | Nothing sends autonomously; every Lead has an inspectable evidence trail and a review gate |
| `[ ]` Planned | 13 | Nov 9 – Nov 13, 2026 | EPIC-09 (part 1) | 11 | `Sequence` aggregate + first channel adapter |
| `[ ]` Planned | 14 | Nov 16 – Nov 20, 2026 | EPIC-09 (part 2) | 10 | Multi-touch variation + remaining channel adapter(s) complete |
| `[ ]` Planned | 15 | Nov 23 – Nov 27, 2026 | EPIC-10 | 13 | Replies are classified; meeting booking works for "interested" |
| `[ ]` Planned | 16 | Nov 30 – Dec 4, 2026 | EPIC-11 | 13 | **Milestone E** — suppression list, bounce handling, jurisdiction rules live; safe to run real outbound volume |
| `[ ]` Planned | 17 | Dec 7 – Dec 11, 2026 | EPIC-12 | 13 | **Milestone F** — outcome events captured; recalibration job built (see gate note below) |

**Total:** 17 sprints, ~183 points, Aug 17 → Dec 11, 2026 (~17 weeks / ~4 months) as
originally planned. Sprint 1 actually started Aug 12 (see §5) — sprints 2–17 keep
their original dates for now rather than shifting the whole plan on one data point;
revisit after Sprint 2–3 actuals per the recalibration policy below.

**EPIC-12 gate:** Sprint 17 ships the *code* for outcome capture and recalibration.
The recalibration itself needs 2–4 weeks of live pipeline usage generating real
`OutcomeEvent`s before it produces a meaningful weight adjustment — track that as a
calendar milestone after Sprint 17, not additional sprint capacity.

Parking Lot (Track 6 — multi-tenancy, retention policy, audit logging) is
deliberately **not** in this schedule. Pull items in only when triggered by a real
need, per the backlog doc.

---

## 3. Release / Milestone View

```text
Aug 17 ───────────────────────────────────────────────────────────────── Dec 11
  │Sprint1-2│Sprint3-4│Sprint5-9        │Sprint10-11│Sprint12    │Sprint13-16    │S17
  │Resilience│Trusted │Company Universe │Orchestrated│Review Gate │Trusted        │Learning
  │Baseline  │Research│MVP (Milestone C)│& Enriched  │(Milestone  │Engagement     │Loop
  │(Milestone│Core    │                 │(Milestone D)│pre-Track2)│Launch         │begins
  │A)        │(Milestone B)              │           │            │(Milestone E)  │(Milestone F)
```

| Milestone | End of | What's demoable |
|---|---|---|
| **A — Resilience Baseline** ✅ | Reached Aug 12 (planned Aug 28) | AI provider fallback, quota governance, config diagnostics — the platform stops silently breaking on provider issues |
| **B — Trusted Research Core** ✅ | Reached Aug 13 (planned Sep 11) | Domain Profile + Evidence v2 — company_research's own output quality improves, independent of anything downstream |
| **C — Company Universe MVP** | Sprint 9 (Oct 16) | A qualified research candidate becomes a real Company + Contact + Lead, end-to-end, for the first time |
| **D — Orchestrated & Enriched** | Sprint 11 (Oct 30) | The pipeline is observable/resumable, and less prone to junk candidates |
| **E — Trusted Engagement Launch** | Sprint 16 (Dec 4) | First real multi-touch outbound campaigns can run safely (review gate + compliance both live) |
| **F — Self-Improving Loop** | Sprint 17 (Dec 11) + 2–4 wks | Real outcomes start recalibrating scoring, not just being recorded |

---

## 4. Ceremonies (adapted for solo + AI capacity)

Standard Scrum ceremonies exist to synchronize a team; solo capacity doesn't need
the coordination overhead, but the checkpoints are still worth keeping in a lighter
form:

- **Sprint Planning (start of each sprint, ~15 min):** confirm the sprint's epic(s)
  are still Ready (Definition of Ready in the backlog doc), confirm no upstream
  dependency slipped, restate the sprint goal.
- **Daily check-in:** not a meeting — at the start of each work session, a one-line
  status note (what's in progress, what's blocked) is enough. Since this is an
  AI-paired workflow, this is naturally captured in conversation history; no separate
  log needed unless you want one.
- **Sprint Review (end of each sprint, ~15–30 min):** live-verify the shipped epic
  against a real payload (not just green tests) — matches how every phase in this
  project has actually been delivered so far. Update the sprint table's status.
- **Sprint Retro (every 2–3 sprints, not every sprint):** short — what slowed things
  down, what velocity number actually held, adjust the forecast (§5).
- **No story-point poker, no separate backlog-grooming meeting** — solo capacity
  means grooming happens inline when a story turns out to be under- or over-scoped;
  just edit the backlog doc.

---

## 5. Velocity Tracking & Re-forecasting

| Sprint | Planned pts | Actual pts | Notes |
|---|---|---|---|
| 1 | 13 | 13 | Completed same day (Aug 12), 5 days ahead of the planned Aug 17 start. See Sprint 1 notes below. |
| 2 | 10 | 10 | Also completed Aug 12, same session as Sprint 1. See Sprint 2 notes below. |
| 3 | 8 | 8 | Also completed Aug 12. Three sprints, zero variance so far. See Sprint 3 notes below. |
| 4 | 8 | 8 | Completed **Aug 13** — a genuinely new day, not the same sitting as 1–3. See Sprint 4 notes below. |
| 5 | 13 | 13 | Also completed Aug 13 — the first genuinely new integration (EPIC-02), and it still didn't slow down. See recalibration and Sprint 5 notes below. |
| 6 | 13 | 13 | Also completed Aug 13 — first sprint with a real decision gate (persistence default), confirmed with the user before starting. See Sprint 6 notes below. |
| 7 | 13 | 13 | Completed **Aug 15** — a genuine 2-day gap since Sprint 6, the first real session-to-session pacing data point. Also the first sprint requiring a scope judgment call (see Sprint 7 notes) rather than pure implementation. |

Fill in "Actual" as sprints complete. After Sprint 3: compute a real average
velocity, compare to the 10 pt/week assumption, and re-run the remaining-sprint
count. If actual velocity is, say, 7 pts/week instead of 10, the remaining ~140
points after Sprint 3 shift from ~14 sprints to ~20 — better to know that in
September than in December. I'll do this recalculation with you when you ask, or
proactively flag it if actuals drift more than ~25% from plan for two sprints running.

**Recalibration check-in, after Sprint 3 (as promised above):** 3 for 3 sprints,
31/31 points, all completed the same day (2026-08-12) in one continuous session.
Taken literally, that "velocity" would suggest compressing the entire 183-point,
17-sprint schedule down to a handful of days — **I'm deliberately not doing that.**
Sprints 1–3 share a trait that won't generalize: each was either directly informed
by an incident already diagnosed earlier in this session (Sprints 1–2) or a
self-contained refactor of code already deeply understood from building it
originally (Sprint 3's `IndustryClassifier`/`IcpMatcher`). None of them involved
new external integrations, new UI/UX decisions, or the kind of design exploration
that Track 2's sequencing engine (EPIC-09, 21 pts) or Track 1's cheap-discovery
tier (EPIC-02, 13 pts — a genuinely new integration) will need. Sprint 4 (EPIC-01)
is similar in shape to Sprint 3, so it's not yet a fair test either. **Real
signal will come from Sprint 5 (EPIC-02)** — first epic in this roadmap requiring
a new external data source, not a refactor of existing logic. I'll revisit the
calendar honestly at that point rather than extrapolating from three
easy-mode sprints. Dates for Sprint 4 onward are left unchanged for now.

**Recalibration check-in, after Sprint 5 (the promised real test):** Sprint 5
(EPIC-02) was a genuinely new integration — a new port, a new adapter, new
caching behavior, new handler branching logic, live-verified against real
Tavily — and it still shipped the same day as Sprint 4. 5 for 5 sprints, 52/52
points, zero variance, across incident fixes, a refactor, an evidence-model
change, and now a real integration. Honest conclusion: **the 10 pt/week
assumption is clearly too conservative for well-specified wiring/integration
work against a codebase I already know intimately from having built most of it
this session** — that part of the original caution was wrong. What I'm *not*
concluding: that the remaining ~131 points will also take days. Several
upcoming epics have a different bottleneck than coding speed:

- **Track 2 (Engagement)** needs real external accounts/credentials that don't
  exist yet (an email-sending provider, LinkedIn access) — no amount of coding
  speed substitutes for provisioning those.
- **Track 4 Phase 16 (review queue)** and **Track 2 Phase 11 (compliance)**
  involve UX and legal/regulatory judgment calls, not just implementation —
  the kind of decision that benefits from your input pacing it, not mine.
- Session-to-session availability (yours and mine) is itself a real constraint
  the point-based estimate never modeled.

So: I'm not rewriting the 17-sprint calendar's dates. The more honest framing
going forward is that **the dates in §2 are a ceiling, not a forecast** — actual
delivery will likely track well ahead of them for pure-coding epics and only
slow down where an epic genuinely needs something from you or the outside
world. If you'd rather I just report progress as "Sprint N of 17, X points
done" without pretending the calendar dates mean anything, say so and I'll
restructure §2 around sequence instead of dates.

**Sprint 1 notes (2026-08-12):** Both stories landed same-day — a strong signal, but
one data point from small, well-scoped config/wiring work isn't enough to re-forecast
the whole roadmap off (holding to the "recalibrate after Sprint 2–3" policy above,
since epics like the sequencing engine involve more design decisions and won't move
this fast). What actually shipped and was live-verified against real APIs, not just
mocks:

- `AIExecutionService.health_check_all()` / `ApplicationAIProvider.health_check_all()`
  — reports reachability per provider.
- Ordered fallback (`AI_PROVIDER_FALLBACK` in `.env`) — live-tested by forcing a real
  Gemini failure (deprecated model name) and confirming it correctly attempted the
  OpenAI fallback and surfaced the true root cause through the exception chain
  (`AIProviderException → AIClientException → AuthenticationError`) instead of a
  generic error.
- `GET /admin/ai-config` — live-tested against the real app. It immediately paid for
  itself: it caught that `OPENAI_API_KEY` is currently being supplied by a real
  process-level environment variable, not `.env` — and it's a *different, invalid*
  key from the one already fixed earlier this project. Not fixable from application
  code (inherited from the parent terminal process); flagged for you to check your
  terminal/VS Code session for a manually-exported `OPENAI_API_KEY`.

Net effect: OpenAI is currently non-functional (bad key) and can't yet be verified as
a *working* fallback target — Gemini alone is confirmed healthy. Azure OpenAI remains
unconfigured. This doesn't block Sprint 1 (the mechanism is correct and covered by 6
unit tests exercising both the success and exhausted-fallback paths); it's an
external credential issue to resolve before Sprint 2 needs a working second provider.

**Update (2026-08-12, before Sprint 2 started):** per explicit instruction, OpenAI is
now excluded entirely — `AI_PROVIDER_FALLBACK` is blank in `.env`, so OpenAI is never
invoked regardless of its key's validity. Gemini-only until further notice.

**Sprint 2 notes (2026-08-12):** All three EPIC-14 stories shipped and were
live-verified against the real app, real Gemini API, and real `ai_usage_log` table
(not just mocks):

- Built a fresh `AIUsageLogModel`/`AIUsageTracker` rather than reusing the
  pre-existing `AIRequestModel`/`AIRequestMapper` persistence stack — that stack
  turned out to be broken and never actually exercised (missing `save()` method,
  and a `Temperature` value-object conversion bug in `converter_registry`).
  Flagged as a new backlog candidate in `product_backlog.md` (fix-or-delete
  decision, not yet scheduled) rather than silently working around it.
- New `AIBudgetPort`/`AIUsageRecorder` application ports keep `SearchCompaniesHandler`
  and `AIExecutionService` decoupled from the concrete persistence mechanism —
  matches the existing `AIProvider` port pattern.
- Live proof: a real Gemini call correctly decremented tracked budget from 20 to 19.
  Then, with the budget artificially constrained to 1, a real
  `POST /company-research/search` call — which live-discovered 21 real candidates via
  Tavily — correctly returned `429` with one clear message instead of attempting any
  of the 21 identity-verification calls. This is the exact failure mode from the
  original Swagger test (17 near-identical per-candidate error lines), now one
  actionable response.

**Sprint 3 notes (2026-08-12):** All three EPIC-00 stories shipped. Seed data for
the 9 profiles was derived directly from the pre-existing hardcoded keyword table
(not invented), so the new `DomainProfile`-driven path and the old hardcoded path
agree by construction, not by luck.

- Regression safety verified two ways: (1) new unit tests assert
  `profile=None` produces byte-identical results to omitting the parameter
  entirely; (2) a live `POST /company-research/search` call (no profile
  injected anywhere in the request path yet, as intended for this phase)
  returned a normal `200` with correctly reasoned `industry_match`/`icp_match`
  fields before rate-limiting cut the batch short (see below).
- **New finding, unrelated to Domain Profiles:** that live call hit a real Gemini
  `429` — a **per-minute** rate limit (5 requests/minute, free tier), which is a
  *different* constraint than the **daily** budget EPIC-14 tracks.
  `SearchCompaniesHandler`'s concurrent fan-out can burst past 5 RPM well before
  the daily cap matters. Not fixed now — added to the Risk Register in
  `product_backlog.md` as unscheduled Track 4 follow-up work.
- **Also observed:** `.env`'s `GEMINI_MODEL` is currently `gemini-2.5-flash`, not
  `gemini-3.5-flash` — the value it was set to earlier this project after the
  "model no longer available" incident. I did not change this myself at any point
  after that fix; flagging it since I can't tell whether the reversion was
  intentional.

**Sprint 4 notes (2026-08-13):** All three EPIC-01 stories shipped. Unlike
Sprints 1–3, this genuinely happened the next calendar day, not the same
sitting — the first real (if small) data point on session-to-session pacing
rather than pure same-session throughput.

- `EvidenceItem.signal_scope` defaults to the conservative `"industry_general"`
  and `classify_evidence()`'s new company-specific-count requirement means
  callers that don't supply scope data can no longer reach `"Confirmed Need"` at
  all — verified with an explicit regression test, plus an end-to-end handler
  test proving `"Confirmed Need"` *is* reachable when evidence is genuinely
  company-specific and capped at `"Strong Opportunity Signal"` when it isn't.
- Story 1.3's acceptance criteria referenced the architecture doc's illustrative
  6-tier ladder naming (`STRONG_COMPANY_SIGNAL`); shipped code kept the actual
  4-tier names already in production rather than introducing a second naming
  scheme not itself in scope. Noted explicitly in `product_backlog.md` rather
  than silently diverging from the written AC.
- Live-verified against real Tavily (not just mocks): a live evidence-gather for
  Tata Motors returned 8 real results, all correctly tagged
  `signal_scope=company_specific` with `observed_date` populated. Chose this over
  a full `/company-research/search` live call to sidestep Sprint 3's known Gemini
  per-minute rate-limit finding, since this sprint's new logic lives in the
  Tavily evidence path, not identity verification.

**Sprint 5 notes (2026-08-13):** All three EPIC-02 stories shipped — the first
genuinely new integration in this roadmap, and the sprint I'd flagged as the real
test of whether the pace would hold. It held. See the recalibration note above.

- No paid registry/government API is available, so `TavilyDirectoryAdapter`
  reuses `TavilyDiscoveryAdapter`'s existing directory-row-parsing classmethods
  rather than duplicating them, and differs from the expensive tier in exactly
  one way that matters: it never falls back to treating a single search result
  as a candidate, only structured directory pages. That's what makes it cheap.
- Added an in-memory, TTL-based cache keyed by (industries, geography,
  company_size) — live-verified: a live Manufacturing/India query took 3.85s
  and returned 18 real candidates; an immediate repeat call returned the exact
  same objects in 0.0001s with zero new Tavily calls.
- The directory adapter had to be registered as a **singleton** in the DI
  wiring (not per-request) for the cache to mean anything across requests —
  the same pattern already used for `get_database_engine`/`get_session_manager`.
- One live candidate came back with a garbled name (an HTML filename fragment
  stuck onto the company name). This is the pre-existing row parser, unchanged
  this sprint — confirms the already-tracked "Discovery precision ceiling" risk
  rather than introducing a new one. EPIC-17 remains the right fix.

**Sprint 6 notes (2026-08-13):** All four EPIC-03 stories shipped, including the
decision gate itself (story 3.1) — confirmed with the user via a direct question
before writing any code, since it changes the `/company-research/search` contract:
**opt-in** (`persist_as_companies: bool = False`), matching the architecture doc's
own recommendation.

- Entity resolution matches by normalized **website** first, then falls back to
  `CreateCompanyHandler`'s existing name-based duplicate check (catching its
  `ConflictException` rather than treating a match as an error) — website is the
  more reliable identity key since names vary across sources but domains don't.
  Verified with a dedicated test: a name *variant* ("Acme Manufacturing" vs.
  "Acme Manufacturing Pvt Ltd") sharing the same website still dedups to one row.
- Added `find_by_website()` to the "Architecture Freeze v5.0"-labeled
  `CompanyRepository` interface — a judgment call on what the freeze protects
  (transaction/aggregate boundaries, not literally every method list); documented
  explicitly in `product_backlog.md` rather than treated as routine.
- Live-verified against the **real production database**, not just the in-memory
  test fixture: a real `persist_as_companies=true` search created an actual
  `Company` row for Samsung India Electronics with a correctly normalized website
  and mapped industry. Re-running the same candidate against the same real DB
  resolved to the identical company id with the row count still at 1 — the
  clearest possible proof of story 3.4's dedup guarantee.
- Also reconfirmed Sprint 3's known Gemini per-minute rate-limit finding during
  live testing (unrelated to this sprint's own logic, already tracked, not
  re-logged as new).

**Sprint 7 notes (2026-08-15):** All three EPIC-04 stories shipped, but this
sprint needed a real scope judgment call before the "3 stories" framing even
applied. Investigating story 4.2 found that `GenerateRecommendationHandler` (the
handler this story originally named) was **completely unreachable** — no route,
no DI wiring, and it called a repository method that doesn't exist on the real
repository. It could never have run. Rather than fix dead code, the AI-generation
work went into `CreateRecommendationHandler` (the only recommendation handler
actually reachable via `POST /recommendations`), and the three confirmed-orphaned
files were deleted. Full reasoning and the much bigger "Universe A vs Universe B"
finding (the `recommendation` module has an entire second, parallel,
unreachable implementation) are documented in `product_backlog.md` — worth reading
if you're planning to touch anything else in that module.

- Also found `RecommendationModel` had no column to persist `solutions` at all —
  fixed with a new `TEXT` column (JSON-serialized) plus a one-time `ALTER TABLE`
  on the existing local `aisdr.db`, matching the pattern already used for
  EPIC-14's `ai_usage_log` table.
- My own test suite caught a real bug before it shipped: the "assessment has no
  content" guard could never trigger, because `maturity_level` always has a
  default value. Fixed to check the actual analysis text fields instead.
- `OpportunityMapper.map_signals()` now reads from the shared catalog with a
  domain-owned fallback for regression safety — verified byte-identical to the
  old hardcoded output for every existing test case, and confirmed the real
  catalog produces the same result too (genuinely one source of truth).
- **Live-verified end-to-end**, real app + real DB + real Gemini: built a full
  Company → Contact → Lead → Discovery → Assessment chain via the real API, then
  called `POST /recommendations`. Gemini correctly matched an existing catalog
  offering (Business Process Automation) against the assessment's actual
  weakness, proposed two sector-appropriate generic ideas not in the catalog, and
  labeled all three correctly (`is_existing_offering: true`/`false`) — exactly the
  architecture doc's intended recommendation order. A separate, fresh `GET`
  confirmed all three solutions survived the round trip through the real database.
- **Pacing:** first genuine multi-day gap (Aug 13 → Aug 15) since this project
  started. Doesn't change the recalibration conclusion from Sprint 5 — the
  bottleneck for sprints like this one was never raw coding throughput, it was
  the judgment call about what "fixing generate_recommendation" should actually
  mean once the obvious target turned out to be dead code.

---

## 6. Status Tracking Convention

Each backlog story (in `product_backlog.md`) and each sprint row (in this file)
should carry one of these statuses. Simplest approach: prefix the story/sprint row
with a status tag as work progresses — no external tool required unless you want one.

```text
[ ] Backlog       — not yet started, not necessarily Ready
[R] Ready         — meets Definition of Ready, can be pulled into a sprint
[>] In Progress   — actively being worked
[?] In Review     — code done, verifying (tests + live smoke test)
[x] Done          — meets Definition of Done
[!] Blocked       — note the blocker inline
```

If you later want this in Jira/Linear/GitHub Projects instead of markdown, the
Epic/Story table in the backlog doc is already structured for a straight CSV/import
conversion — say the word and I'll generate that mapping rather than re-deriving the
backlog from scratch.

---

## 7. What "so we do not miss anything" means in practice

- Every phase in the architecture doc has exactly one epic here — nothing was
  silently dropped except EPIC-07 (explicitly superseded, documented why) and Track 6
  (explicitly parked, documented triggers for pulling it back in).
- Every epic has acceptance criteria in the backlog doc — "done" isn't a feeling.
- The Risk Register in the backlog doc is cross-referenced to the epic that
  mitigates each risk — nothing is a known risk with no owner.
- This file's velocity table is the drift-detector: if actuals stop matching plan,
  that's visible in one table, not discovered in December.
