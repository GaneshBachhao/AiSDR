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

| Sprint | Dates (Mon–Fri) | Epic(s) | Points | Sprint Goal |
|---|---|---|---|---|
| 1 | Aug 17 – Aug 21, 2026 | EPIC-13, EPIC-15 | 13 | Stop repeating this session's own failures: AI provider fallback + a config diagnostics endpoint, both ship this week |
| 2 | Aug 24 – Aug 28, 2026 | EPIC-14 | 10 | AI spend/quota is tracked and pre-flight-checked, not discovered via failed batches |
| 3 | Aug 31 – Sep 4, 2026 | EPIC-00 | 8 | Industry/ICP vocabulary is data, not hardcoded Python |
| 4 | Sep 7 – Sep 11, 2026 | EPIC-01 | 8 | Evidence carries `signal_scope`; `CONFIRMED_NEED` can no longer be faked by industry noise |
| 5 | Sep 14 – Sep 18, 2026 | EPIC-02 | 13 | A cheap discovery tier exists ahead of live Tavily search |
| 6 | Sep 21 – Sep 25, 2026 | EPIC-03 | 13 | Research candidates resolve into real, deduplicated `Company` records |
| 7 | Sep 28 – Oct 2, 2026 | EPIC-04 | 13 | `generate_recommendation` actually generates something, from a real shared catalog |
| 8 | Oct 5 – Oct 9, 2026 | EPIC-05 | 8 | Qualified candidates get contact discovery, gated correctly |
| 9 | Oct 12 – Oct 16, 2026 | EPIC-06 | 8 | **Milestone C** — full Company → Contact → Lead pipeline live end-to-end |
| 10 | Oct 19 – Oct 23, 2026 | EPIC-08 | 8 | The full chain is observable and resumable, not silently swallowing failures |
| 11 | Oct 26 – Oct 30, 2026 | EPIC-17 | 8 | **Milestone D** — enrichment waterfall live; junk-candidate rate measurably down |
| 12 | Nov 2 – Nov 6, 2026 | EPIC-16 | 13 | Nothing sends autonomously; every Lead has an inspectable evidence trail and a review gate |
| 13 | Nov 9 – Nov 13, 2026 | EPIC-09 (part 1) | 11 | `Sequence` aggregate + first channel adapter |
| 14 | Nov 16 – Nov 20, 2026 | EPIC-09 (part 2) | 10 | Multi-touch variation + remaining channel adapter(s) complete |
| 15 | Nov 23 – Nov 27, 2026 | EPIC-10 | 13 | Replies are classified; meeting booking works for "interested" |
| 16 | Nov 30 – Dec 4, 2026 | EPIC-11 | 13 | **Milestone E** — suppression list, bounce handling, jurisdiction rules live; safe to run real outbound volume |
| 17 | Dec 7 – Dec 11, 2026 | EPIC-12 | 13 | **Milestone F** — outcome events captured; recalibration job built (see gate note below) |

**Total:** 17 sprints, ~183 points, Aug 17 → Dec 11, 2026 (~17 weeks / ~4 months).

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
| **A — Resilience Baseline** | Sprint 2 (Aug 28) | AI provider fallback, quota governance, config diagnostics — the platform stops silently breaking on provider issues |
| **B — Trusted Research Core** | Sprint 4 (Sep 11) | Domain Profile + Evidence v2 — company_research's own output quality improves, independent of anything downstream |
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
| 1 | 13 | _TBD_ | |
| 2 | 10 | _TBD_ | |
| 3 | 8 | _TBD_ | |

Fill in "Actual" as sprints complete. After Sprint 3: compute a real average
velocity, compare to the 10 pt/week assumption, and re-run the remaining-sprint
count. If actual velocity is, say, 7 pts/week instead of 10, the remaining ~140
points after Sprint 3 shift from ~14 sprints to ~20 — better to know that in
September than in December. I'll do this recalculation with you when you ask, or
proactively flag it if actuals drift more than ~25% from plan for two sprints running.

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
