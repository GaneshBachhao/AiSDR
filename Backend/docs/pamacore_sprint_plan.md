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
| `[x]` Done | 8 | **Started early: Aug 15, 2026** (planned Oct 5–9) | EPIC-05 | 8 | Qualified candidates get contact discovery, gated correctly |
| `[x]` Done | 9 | **Started early: Aug 15, 2026** (planned Oct 12–16) | EPIC-06 | 8 | **Milestone C** — full Company → Contact → Lead pipeline live end-to-end (mechanism live; Lead creation dormant until EPIC-17 adds a real email source — see notes) |
| `[x]` Done | 10 | **Started early: Aug 15, 2026** (planned Oct 19–23) | EPIC-08 | 8 | The full chain is observable and resumable, not silently swallowing failures |
| `[x]` Done | 11 | **Completed early: Aug 20, 2026** (planned Oct 26 – Oct 30) | EPIC-17 | 8 | **Milestone D** ⚙ Mechanism shipped — known-bad candidates now rejected pre-research; third-tier extensibility seam added, no real paid vendor integrated (see gate note below) |
| `[x]` Done | 12 | **Completed early: Aug 19, 2026** (planned Nov 2 – Nov 6) | EPIC-16 | 13 | Nothing sends autonomously; every Lead has an inspectable evidence trail and a review gate |
| `[x]` Done | 13 | **Completed early: Aug 20, 2026** (planned Nov 9 – Nov 13) | EPIC-09 (9.1 only) | 8 | `Sequence` aggregate — a cadence plan (ordered touches against a real Lead) is definable and useful without AI content or real channel credentials. Sequencing's *execution* half (story 9.3) moved to Sprint 18 — see note below. |
| `[x]` Done | 14 | **Completed early: Aug 21, 2026** (planned Nov 16 – Nov 20) | EPIC-09 (9.2 only) | 8 | Multi-touch content generation — each touch's angle (opener/proof-point/breakup) varies by position, grounded in real Lead evidence. |
| `[x]` Done | 15 | **Completed early: Aug 21, 2026** (planned Nov 23 – Nov 27) | EPIC-10 (10.1 + 10.3 only) | 8 | Replies are classified (6 categories) and Lead status/score update accordingly. Meeting-booking's calendar half (story 10.2) moved to Sprint 18 — see note below. |
| `[x]` Done | 16 | **Completed early: Aug 19, 2026** (planned Nov 30 – Dec 4) | EPIC-11 | 13 | **Milestone E** — suppression list, bounce handling, jurisdiction rules live; safe to run real outbound volume |
| `[x]` Done | 17 | **Completed early: Aug 19, 2026** (planned Dec 7 – Dec 11) | EPIC-12 | 13 | **Milestone F** — outcome events captured; recalibration job built (calendar gate on real data still open, see gate note below) |
| `[ ]` Planned — blocked | 18 | Dec 14 – Dec 18, 2026 | EPIC-09 (9.3) + EPIC-10 (10.2) | 10 | **Milestone G** — real outbound send (SMTP/LinkedIn) and real meeting-booking (calendar) go live. Everything in this sprint is customer/lead-outreach *execution* — deliberately bundled last, gated on real third-party credentials this project doesn't have yet. Not started; see note below. |

**Total:** 18 sprints, ~193 points, Aug 17 → Dec 18, 2026 (~18 weeks / ~4.5 months) as
originally planned. Sprint 1 actually started Aug 12 (see §5) — sprints 2–18 keep
their original dates for now rather than shifting the whole plan on one data point;
revisit after Sprint 2–3 actuals per the recalibration policy below. Sprint 18 was
split out of Sprints 13/14/15 on 2026-08-21 at the user's request: every remaining
customer/lead-outreach-execution story (real send channels, real calendar booking)
is now consolidated into one final sprint instead of sitting as partial/blocked
leftovers inside earlier sprints. This is a pure re-sequencing of already-scoped,
not-yet-startable work -- no new scope was added and no points changed epics.

**EPIC-12 gate:** Sprint 17 shipped the *code* for outcome capture and
recalibration (completed early, Aug 19). The recalibration itself still needs
2–4 weeks of live pipeline usage generating real `OutcomeEvent`s before it
produces a meaningful weight adjustment — confirmed live on Aug 19: 0 Leads have
captured `evidence_signals` yet. Track that as a calendar milestone after
Sprint 17, not additional sprint capacity.

Parking Lot (Track 6 — multi-tenancy, retention policy, audit logging) is
deliberately **not** in this schedule. Pull items in only when triggered by a real
need, per the backlog doc.

---

## 3. Release / Milestone View

```text
Aug 17 ──────────────────────────────────────────────────────────────────────── Dec 18
  │Sprint1-2│Sprint3-4│Sprint5-9        │Sprint10-11│Sprint12    │Sprint13-17    │S18
  │Resilience│Trusted │Company Universe │Orchestrated│Review Gate │Trusted        │Live
  │Baseline  │Research│MVP (Milestone C)│& Enriched  │(Milestone  │Engagement     │Outreach
  │(Milestone│Core    │                 │(Milestone D)│pre-Track2)│Launch (mech.) │Cutover
  │A)        │(Milestone B)              │           │            │(Milestone E/F)│(Milestone G)
```

| Milestone | End of | What's demoable |
|---|---|---|
| **A — Resilience Baseline** ✅ | Reached Aug 12 (planned Aug 28) | AI provider fallback, quota governance, config diagnostics — the platform stops silently breaking on provider issues |
| **B — Trusted Research Core** ✅ | Reached Aug 13 (planned Sep 11) | Domain Profile + Evidence v2 — company_research's own output quality improves, independent of anything downstream |
| **C — Company Universe MVP** ⚙ Mechanism shipped | Code shipped Aug 15 (planned Oct 16) | A qualified research candidate becomes a real Company + Contact + Lead, end-to-end, for the first time -- the code path is real, tested, and live-verified, but Contact/Lead creation is dormant until EPIC-17 adds a real email source (see Sprint 9 notes). Full-milestone claim held back deliberately rather than declared reached on a technicality. |
| **D — Orchestrated & Enriched** ✅ | Reached Aug 20 (planned Oct 30) | The pipeline is observable/resumable (Sprint 10) and less prone to junk candidates (Sprint 11) -- both true today. Note this milestone's claim never depended on a real paid-enrichment vendor, unlike EPIC-06/EPIC-17's separate email-enrichment thread (still open, see Sprint 11 notes) -- so this one is a clean, full reach, not a partial like C/F. |
| **E — Trusted Engagement Launch** ⚙ Mechanism shipped | Code shipped Aug 21 (planned Dec 4) | Sequencing, touch content generation, reply classification, suppression, bounce handling, and jurisdiction rules are all real, tested, and live-verified -- a cadence can be planned, its content generated, and a reply correctly classified and acted on. But nothing can actually be *sent* yet (no channel adapter, story 9.3) and "interested" replies can't yet get a real calendar slot (story 10.2) -- both deliberately deferred to Sprint 18/Milestone G, not silently assumed. |
| **F — Self-Improving Loop** ⚙ Mechanism shipped | Code shipped Aug 19 (planned Dec 11) + 2–4 wks | `OutcomeEvent` capture, `evidence_signals` on `Lead`, and the recalibration script are real, tested, and live-verified -- but the *outcome* (scoring actually being recalibrated from real data) is still gated on 2–4 weeks of live pipeline usage (confirmed live: 0 Leads have captured signals yet). Full-milestone claim held back deliberately, same as Milestone C. |
| **G — Live Outreach Cutover** | Sprint 18 (Dec 18) | Real send channels (SMTP/LinkedIn, story 9.3) and real calendar booking (story 10.2) go live -- the two remaining pieces of customer/lead-outreach *execution*, both gated on real third-party credentials this project doesn't have configured yet. This is the last sprint by design: every other mechanism (planning, content, classification, compliance, learning loop) is already live and waiting on this. |

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
| 8 | 8 | 8 | Also completed Aug 15, same day as Sprint 7. First sprint with a real, previously-flagged decision gate resolved before writing code (company_research-specific port vs. shared contract). See Sprint 8 notes below. |
| 9 | 8 | 8 | Also completed Aug 15. Second decision gate in a row, this one discovered mid-sprint rather than flagged in advance: a mandatory-schema-field gap (no email source exists) that shapes whether the epic's output is live or dormant. See Sprint 9 notes below. |
| 10 | 8 | 8 | Also completed Aug 15. Third decision gate in a row: the domain module the story named to reuse turned out to be unused, untested, and internally inconsistent scaffolding -- built purpose-fit tracking instead. Also a public API contract change (response envelope), made deliberately and documented, not incidentally. See Sprint 10 notes below. |
| 12 | 13 | 13 | Completed **Aug 19** -- picked deliberately out of order, ahead of Sprint 11 (EPIC-17), because it's a zero-AI/Tavily-quota epic (pure CRUD/state-machine) that could ship without spending scarce Gemini daily budget, unlike Sprint 11's enrichment work. See Sprint 12 notes below. |
| 16 | 13 | 13 | Completed **Aug 19**, same day as Sprint 12 -- also picked out of order for the same zero-quota reason (EPIC-11 is pure CRUD/domain logic, no AI/Tavily calls). Sprint 16 now precedes Sprints 13-15 in actual completion order even though it's numbered after them -- see Sprint 16 notes below. |
| 17 | 13 | 13 | Completed **Aug 19**, same day as Sprints 12 and 16 -- picked out of order for the same zero-quota reason (EPIC-12's dev work is CRUD + pure statistics, no AI/Tavily calls). Formally depends on EPIC-10 (still Backlog) and EPIC-11 (Done); only the EPIC-11 half was actually needed for this sprint's scope. See Sprint 17 notes below -- the calendar-gate portion of Story 12.2 remains open regardless of dev completion. |
| 11 | 8 | 8 | Completed **Aug 20** -- the same epic Sprint 12's notes had deferred as needing real paid-API spend turned out, on rereading the code, to be only half true: EPIC-02 already shipped the cheap→Tavily fallback, so the only remaining zero-quota-buildable piece was the candidate-gate fix (17.2) plus an extensibility seam for a future paid tier (17.1), not a real vendor integration. See Sprint 11 notes below. |
| 13 | 8 | 8 | **Sequence aggregate completed Aug 20** -- story 9.1, a full vertical slice, definable and useful without AI content or real channel credentials. Re-scoped 2026-08-21: story 9.3 (channel adapter) was originally mapped partly to this sprint's points but never this sprint's *work*; it now lives entirely in Sprint 18 with EPIC-10.2, so this sprint's planned/actual both reflect 9.1 alone. See Sprint 13 notes below. |
| 14 | 8 | 8 | **Touch content generation completed Aug 21** -- story 9.2, picked up in a second pass once the user explicitly authorized a capped live-Gemini spend (2 calls total). Re-scoped 2026-08-21 for the same reason as Sprint 13 -- planned/actual now reflect 9.2 alone; the channel-adapter remainder lives in Sprint 18. See Sprint 14 notes below. |
| 15 | 8 | 8 | **Reply classification completed Aug 21** -- stories 10.1 + 10.3, picked out of order past EPIC-10's formal EPIC-09 dependency since a reply classifier only needs reply text, not a real inbound channel; user-authorized capped live-Gemini spend (3 calls total). Re-scoped 2026-08-21 -- story 10.2 (calendar integration) now lives in Sprint 18 with EPIC-09.3, so this sprint's planned/actual both reflect 10.1+10.3 alone. See Sprint 15 notes below. |
| 18 | 10 | — | **Not started.** EPIC-09.3 (channel adapters, 5 pts) + EPIC-10.2 (calendar integration, 5 pts) -- consolidated here 2026-08-21 at the user's request, so every remaining customer/lead-outreach-*execution* story sits in one final sprint instead of scattered as partial leftovers across 13/14/15. Both stories are blocked on the same class of thing: real third-party credentials (SMTP/LinkedIn, calendar API) this project doesn't have configured. Nothing to build until those are supplied. |

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

**Sprint 8 notes (2026-08-15):** Both EPIC-05 stories shipped, same day as
Sprint 7 (no calendar gap this time). Story 5.1's decision gate — new
company_research-specific `ContactDiscoveryPort` vs. implementing the
existing unimplemented `ContactDiscoveryService` contract, flagged in the
Parking Lot before Sprint 7 — was confirmed with the user before writing any
code, per the same discipline as Sprint 6's persistence-flag gate. Went with
the new port, matching the module's existing pattern
(`CompanyDiscoveryPort`/`IdentityVerificationPort`/`EvidenceResearchPort`);
the shared contract stays a Parking Lot candidate for if/when another module
needs it.

- `TavilyContactDiscoveryAdapter` mines real LinkedIn profile search results
  (filtered strictly to `linkedin.com/in/...` URLs) and parses the standard
  "Name - Title - Company | LinkedIn" title format — no profile found means
  an empty list, never a guessed contact.
- Gating (story 5.2) sits inside the same per-candidate pipeline step that
  computes qualification score, so a sub-threshold candidate never triggers
  a contact-discovery call at all, not just a discarded result. Role
  targeting reuses the `decision_maker_role` Sprint 7's catalog match
  already computes.
- Added `CompanySearchResult.discovered_contacts` (a list, richer than the
  pre-existing singular `decision_maker_name`) — the first request during
  Sprint 8 planning surfaced that the user wants a frontend built against
  this API eventually, so new response fields were shaped with that
  consumer in mind (flat, typed, no internal leakage) even though no
  frontend work is scheduled yet.
- **Live-verified against real Tavily**, full discovery → evidence → scoring
  → contact-discovery pipeline. Gemini identity verification hit its
  free-tier **daily** quota (already exhausted from earlier live testing
  today, not a new issue) — substituted a scripted trust-the-website stub
  for identity only, the same workaround Sprint 4 used for the same known
  limitation. For a real qualifying candidate ("Jabil", score 74), found a
  genuine LinkedIn profile and correctly populated both
  `discovered_contacts` and `decision_maker_name`; for pre-existing
  discovery-tier noise candidates (already tracked under EPIC-17), correctly
  returned an empty contact list rather than fabricating anyone.

**Sprint 9 notes (2026-08-15):** All three EPIC-06 stories shipped, same day
as Sprints 7 and 8. Story 6.2 surfaced a real blocker before any code was
written: `Contact.email` is mandatory and validated, but Sprint 8's
LinkedIn-sourced `DiscoveredContact` never carries one -- LinkedIn search
results don't expose emails. Laid out two options for the user (pattern-guess
an email vs. only create Contact/Lead when a real one exists) and confirmed
**the never-guess option** before writing the bridge, consistent with
`IdentityVerificationPort`/`ContactDiscoveryPort`'s existing discipline of
treating absent evidence as a hard stop, not a best-effort guess.

- `PromoteCandidateToLeadHandler` mirrors Sprint 6's
  `PromoteCandidateToCompanyHandler` shape: resolve-or-create Contact
  (dedup by email), resolve-or-create Lead (dedup by company+contact, reusing
  `LeadRepository.list`'s existing filters -- no new repository method
  needed), `notes` carrying score/hypothesis/evidence/trigger-event using the
  Lead schema's existing free-text field.
- Reused the existing `persist_as_companies` flag rather than adding a new
  one -- judgment call, documented in the backlog: since Contact/Lead
  creation is a no-op without a real email today, this changes zero live
  behavior for existing callers.
- Story 6.3's E2E dedup test supplies a scripted email on the test fixture
  (documented as simulating a future email source) to prove the mechanism
  itself against a real DB, independent of today's missing-email gap:
  running the same result through promotion twice produces exactly one
  Company, one Contact, one Lead.
- **Live-verified against real Tavily and the real production DB:** a real
  `persist_as_companies=true` search created three genuine Company rows and
  found two real LinkedIn profiles via Sprint 8's contact discovery (no
  emails, as expected). All three results correctly reported
  `lead_creation_skipped_reason: "no_verified_email_found"` -- confirmed
  directly against the database that zero new Contact/Lead rows were
  created. Milestone C is therefore marked "mechanism shipped," not "reached"
  -- see §3 above -- since a qualified candidate doesn't yet become a live
  Lead without EPIC-17 adding a real email source.

**Sprint 10 notes (2026-08-15):** Both EPIC-08 stories shipped, same day as
Sprints 7-9. Investigating story 8.1 before writing any code found that
`app.domain.workflow` -- the module the story explicitly named to reuse --
is complete-looking domain scaffolding (`Workflow` aggregate, `WorkflowStep`,
validation/execution services) that has **never been wired to anything**:
no application layer, no persistence, no router, zero tests, zero
references anywhere else in the codebase. It also has an internal defect of
its own (two duplicate `WorkflowId` classes in different subpackages) and a
sync/async mismatch (`WorkflowRepository` is a synchronous ABC in an
otherwise fully-async codebase). Laid out the tradeoffs for the user
(fix-and-adopt vs. purpose-fit tracking) before starting -- third decision
gate in three sprints, this one surfaced mid-investigation rather than
flagged in advance. **Chose purpose-fit tracking**, confirmed with the user;
`app.domain.workflow` moved to the Parking Lot as unused/inconsistent
scaffolding.

- The actual bug: `SearchCompaniesHandler._research`'s blanket
  `except Exception: return None` made a genuine crash (network error,
  provider outage) indistinguishable from a candidate that was correctly
  checked and just doesn't qualify -- both silently vanished from the
  response the same way. Fixed by wrapping the two real I/O boundaries
  (identity verification, evidence gathering) so an unexpected exception
  becomes a tagged `CandidateResearchFailure` instead of a bare `None`.
  Deterministic disqualification branches are completely unchanged.
- **Public API contract change, made deliberately:**
  `POST /company-research/search` now returns `{results, failures}` instead
  of a bare array -- the only honest shape for surfacing crashed candidates
  without conflating them with legitimate rejections. New
  `POST /company-research/retry` endpoint re-runs one failed candidate
  without paying for a fresh Tavily discovery pass.
- **Live-verified against real Tavily:** ran a real discovery batch, made
  the evidence step genuinely crash for one specific real candidate
  (simulating a Tavily outage) while three others proceeded normally.
  `failures` correctly isolated the one crashed candidate with the right
  step tag and error message; the other three landed in `results`
  unaffected. Retrying the failed candidate -- no new discovery call --
  produced a real qualified result (score 74), concretely proving
  resumability rather than just asserting a flag.
- **Unrelated finding surfaced during live verification:** the real Gemini
  identity adapter is already correctly defensive (never raises, per its
  existing contract), so it couldn't demonstrate a step failure itself --
  but every real call against it today returns `404 NOT_FOUND:
  models/gemini-2.5-flash is no longer available to new users`, a model
  deprecation distinct from the daily-quota exhaustion tracked in Sprints
  8-9. Flagged to the user directly and added to the Risk Register; not
  fixed here.

**Sprint 12 notes (2026-08-19):** All three EPIC-16 stories shipped, picked
deliberately out of order ahead of Sprint 11 (EPIC-17) -- it's the first
formal-roadmap sprint completed after a separate, cross-cutting
zero-AI-quota effort (see `docs/intermediate_sprint_no_api_quota.md` and
`docs/company_search_and_prompt_tuning.md`, both completed earlier this
same day) established the pattern of front-loading quota-free work while
Gemini's daily budget was scarce. EPIC-16 is pure CRUD/state-machine --
no AI, no Tavily -- unlike Sprint 11's enrichment-source work.

Full detail (scope calls, the persistence bug found and fixed, exact
shipped surface, live-verification steps) is in `product_backlog.md`'s
EPIC-16 section rather than duplicated here -- same cross-referencing
discipline as every other sprint. Headline points: `Sequence` doesn't
exist yet (EPIC-09 still Backlog), so the review gate landed on `Lead`
only; found and fixed a real pre-existing persistence bug
(`SqlAlchemyLeadRepository` had no `update()` override, silently
clobbering audit columns on every save -- same bug class already fixed
for `Recommendation`); live-verified against two real seeded Leads
(one with a full Discovery → Assessment → Recommendation chain, one
freshly-created) through the full `submit-for-review → approve` and
`submit-for-review → reject → submit-for-review` paths, plus a clean
`409` on an illegal transition. Backend suite: **662 passing** (up from
639).

**Sprint 16 notes (2026-08-19):** All three EPIC-11 stories shipped, same
day as Sprint 12, also picked deliberately out of order (ahead of Sprints
11 and 13-15) for the same zero-AI-quota reason. Full detail is in
`product_backlog.md`'s EPIC-11 section rather than duplicated here.
Headline points: same "no send path exists yet" gap EPIC-16 already
found (`EmailSender` is unused, EPIC-09 still Backlog) applies to 11.1
too -- resolved the same honest way, plus a real integration into
EPIC-16's own `GET /leads/{id}/review` (`contact_email_suppressed`), so
the suppression list is genuinely useful the moment it ships rather than
purely forward-looking. This app's first webhook endpoint
(`POST /webhooks/email-events`), with its own new shared-secret auth
mechanism (fails closed on an unconfigured secret) since JWT/
`get_current_user` doesn't fit a third-party caller. Jurisdiction
resolution deliberately uses only `Company.country` (the one geography
source that's actually persisted/authoritative at send time), not
`CompanyResearchRequest.geography` (request-time-only, gone by send
time) -- an explicit design call, not an oversight, documented in
`product_backlog.md`. Live-verified against a real seeded Lead
(Meridian Logistics Group): suppressed and lifted its real Contact's
email, confirmed the review-chain flag flipped both ways; posted a real
bounce webhook with correct/wrong/missing secrets; resolved its real
`Company.country: "US"` to the CAN-SPAM ruleset. Backend suite:
**710 passing** (up from 662).

**Sprint 17 notes (2026-08-19):** Both EPIC-12 stories shipped, same day as
Sprints 12 and 16, picked out of order for the same zero-AI-quota reason --
`OutcomeEvent` persistence and the recalibration mechanism are CRUD + pure
statistics, no AI/Tavily calls. Formally depends on EPIC-10 (still Backlog)
and EPIC-11 (Done); only EPIC-11 mattered for this sprint's actual scope.
Full detail is in `product_backlog.md`'s EPIC-12 section rather than
duplicated here. Headline points: found and fixed the same shape of gap
EPIC-16 found for Lead persistence -- `QualificationScorer` already computed
a 6-category `evidence_signals` dict (hiring/growth/technology/ai/process/
funding) but discarded it before it ever reached a Lead row; `Lead` now
carries it (6 flat nullable `Boolean` columns -- this codebase has no JSON-
column precedent, and the signal set is small and fixed, so flat columns
matched its own convention better than inventing one). Also wired the
previously-dead `DomainProfile.scoring_weight_overrides` field into
`QualificationScorer.score()` for the first time (optional
`weight_overrides` param, default `None` preserves every existing caller's
behavior exactly) -- explicitly did **not** additionally wire
`DomainProfile` selection into `search_companies_handler.py` itself, since
that's a separate, larger, pre-existing gap unrelated to outcome feedback.
The recalibration pass (`SignalCorrelationAnalyzer` +
`scripts/recalibrate_qualification_weights.py`, following the
`create_user.py` offline-script precedent -- this codebase has no
scheduler/cron infrastructure) deliberately stops at reporting correlation,
not auto-computing new weights; that's a human call. Live-verified against
the real running backend: `POST /outcomes` against a real seeded Lead,
listed, deleted, and a fabricated `lead_id` correctly 404'd; ran the
recalibration script for real and it honestly reported "Insufficient data:
0 Lead(s) with captured evidence signals" -- the correct answer, since no
Lead has been through a live `search_companies` → `promote` run yet (that
would cost real quota). The `evidence_signals` flatten/unflatten logic
itself is proven by a real-database repository round-trip test instead.
Backend suite: **746 passing** (up from 710).

**Sprint 11 notes (2026-08-20):** Both EPIC-17 stories shipped, the day after
Sprints 12/16/17. Full detail is in `product_backlog.md`'s EPIC-17 section
rather than duplicated here. Headline points: re-read
`SearchCompaniesHandler` before assuming this epic still needed real paid-API
spend (the reason it had been deferred past Sprints 12/16/17) and found that
assumption only half true -- the cheap-tier→Tavily fallback (17.1's literal
first half) was already shipped in EPIC-02/Sprint 5; the only genuinely new
part of 17.1 is "room for" a future paid tier, which the AC itself only asks
for as extensibility, not an actual vendor integration. Shipped that as one
new optional constructor parameter (`paid_directory_port`, defaulting to
`None`, provably a no-op when omitted -- not just tested-equal, unreachable
by construction) rather than fabricating an adapter against a vendor with no
real account, matching this project's established never-fabricate discipline
(same reasoning as EPIC-07's "Won't-now" and `ContactDiscoveryPort`'s
contract). 17.2 found a real, previously-unfixed gap: the two known-bad
candidates from live testing ("Company search", "Browse by size: 51-200
employees") did not trip any existing `DeterministicCandidateGate` rule --
added `blocked_name_markers` to catch nav/filter-UI text scraped as a
company name, plus the first-ever dedicated test file for that gate class
(previously only incidental coverage existed). Milestone D ("Orchestrated &
Enriched") is now a clean, full reach -- unlike Milestones C and F, its
demoable claim never depended on the still-missing real paid-enrichment
vendor. That vendor gap (EPIC-06's dormant Lead creation) remains open,
stated explicitly rather than claimed resolved. Zero live Tavily/Gemini
calls this sprint -- confirmed the app still imports and wires cleanly (all
64 routes) as a smoke check, did not spend a real call to prove the
waterfall end-to-end. Backend suite: **761 passing** (up from 746).

**Sprint 13 notes (2026-08-20):** Only story 9.1 (`Sequence` aggregate, 8 pts)
shipped -- the first genuinely partial sprint completion this session. Full
detail is in `product_backlog.md`'s EPIC-09 section rather than duplicated
here. Headline points: shipped as a full vertical slice (domain + persistence
+ application + API), not just domain classes, since a Sequence plan (ordered
touches against a real Lead) is fully definable and useful without AI content
(9.2) or real channel credentials (9.3) -- matches the honest-scoping
discipline used all session, just now applied *within* a single story instead
of across a whole epic. `StartSequenceHandler` is the first real caller of
EPIC-16's review gate (`Lead.review_status == Approved` required before a
cadence can start), closing a loop EPIC-16's own Risk Register note had left
open. Found and fixed a real gap in this codebase's persistence layer: no
existing precedent for an owned, immutable, ordered list of value objects on
an aggregate -- built a proper child table (`sequence_touches`) instead of
reaching for JSON or a sibling-aggregate relationship, and along the way hit
(then fixed, switching `lazy="joined"` to `lazy="selectin"`) a real SQLAlchemy
footgun where joined eager-loading against a collection duplicates parent rows
per child row. Live-verified against the real running backend: a Sequence's
`start()` correctly 409'd against a not-yet-approved Lead, succeeded once
approved via the real EPIC-16 endpoints, advanced through natural completion,
and separately exercised both the reply and bounce branches on fresh
sequences. Zero live Tavily/Gemini calls. Backend suite: **828 passing** (up
from 761).

**Sprint 14 notes (2026-08-21):** Story 9.2 (touch content generation, 8
pts) shipped -- the second genuinely partial sprint completion this session,
and the first sprint requiring a deliberate, user-authorized live-AI spend
(2 real Gemini calls total, capped in advance, not a batch). Full detail is
in `product_backlog.md`'s EPIC-09 section rather than duplicated here.
Headline points: corrected an earlier research finding from this same
session -- AI-generated outreach prose wasn't actually new to this codebase,
`CreateRecommendationHandler` (EPIC-04) already does it for Solution text;
this story followed *that* handler's shape (including its "refuse to
generate from nothing" gate) rather than the classification-only identity-
verification adapter this session had initially assumed was the closest
precedent. Each touch's angle (opener / proof point / breakup) is derived
purely from position, with prior touches' content listed in every later
prompt so repetition is mechanically avoidable. `Touch` gained a `content`
field without reopening EPIC-09.1's immutable-list persistence design -- the
delete-orphan-diffing problem that design avoided was about the touches
*collection* changing shape, never a scalar field on an already-stable
child row. Live-verified against a real seeded, Approved Lead with a
genuinely rich Discovery/Assessment/Recommendation chain: both touches came
back distinct and faithfully grounded in the real evidence (verified by
reading the chain back and comparing, not just eyeballing plausibility);
confirmed the Draft-only 409 gate and the zero-cost "no evidence" 422 gate
both fire correctly. Backend suite: **871 passing** (up from 828).

**Sprint 15 notes (2026-08-21):** Stories 10.1 (reply classification) + 10.3
(Lead status/score update) shipped together, past EPIC-10's formally-listed
EPIC-09 dependency -- EPIC-09.3 (real SMTP/LinkedIn channel adapters) is
genuinely blocked on credentials this project doesn't have, but a reply
classifier only needs reply *text*, not a real inbound channel to have
delivered it. Same "ship the genuinely unblocked part, document the honest
scope gap" move already used for Sprints 12, 16, and 17. New
`ReplyClassificationPort` + `AiReplyClassificationAdapter` mirror
`AiIdentityVerificationAdapter`'s JSON-mode-by-convention shape exactly
(fenced-JSON strip, safe-sentinel degrade on any parse/provider failure --
here, `NOT_NOW`/`LOW` rather than a 500). `ClassifyReplyHandler`
(`POST /leads/{id}/classify-reply`) applies a documented status/score/
Sequence mapping per category, with one deliberate asymmetry: `OUT_OF_
OFFICE` changes nothing and does not stop an Active Sequence, since an
auto-responder isn't a real reply from the person. The endpoint is
JWT-gated like the rest of `lead_router.py`, not the `verify_webhook_
secret` shared-secret tier used for `POST /webhooks/email-events` --
the caller here is an operator, not an unauthenticatable real ESP, so
reusing the webhook-secret mechanism would have reused the wrong
justification even though the mechanism itself is reusable. Live-verified
with 3 real Gemini calls (capped, user-authorized) against real seeded
Leads: a "not now" reply on an Approved/Qualified (score 82) Lead with two
real Active Sequences correctly dropped it to Contacted/score 77 and
stopped both Sequences; an "interested" reply on a fresh Lead correctly
qualified it and boosted score 0 → 20; an out-of-office auto-reply
correctly left status/score completely unchanged. Story 10.2 (calendar
integration) stays Backlog, explicitly documented as blocked rather than
attempted with a fabricated calendar adapter. Backend suite: **895
passing** (up from 871).

**Sprint 18 (planned, not started) — re-sequencing note (2026-08-21):** at
the user's request, every remaining customer/lead-outreach-*execution*
story was pulled out of Sprints 13/14/15 (where it sat as partial/blocked
leftovers) and consolidated into one final sprint: EPIC-09.3 (real
SMTP/LinkedIn channel adapters, 5 pts) + EPIC-10.2 (calendar integration
for meeting booking, 5 pts). Both are the only two pending stories left in
the entire 18-sprint plan — everything else is Done. Both are blocked on
the same class of thing (real third-party credentials this project doesn't
have configured), and both are, in substance, the same kind of work: making
the platform actually touch a real customer/lead-facing channel rather than
plan/generate/classify around one. Grouping them last means every other
mechanism -- sequencing, content generation, reply classification,
suppression/compliance, and the outcome-learning loop -- is already fully
built and live-verified, waiting only on real credentials to flip on. This
is a pure re-sequencing of already-scoped work; no new scope was added and
no points moved between epics, only between sprints.

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
