# AiSDR Frontend — Sprint Plan

Companion to [`frontend_backlog.md`](frontend_backlog.md) (scope/epics).
This is the sequencing document — same spirit as the backend's
`Backend/docs/pamacore_sprint_plan.md`, but deliberately lighter and
**without calendar dates**, since this backlog is explicitly informal/
untracked (see the 2026-08-15 decision recorded in
`frontend_backlog.md`'s header). If/when frontend work gets formalized
into the backend's tracked roadmap, this is the file to convert into a
dated schedule.

Sprints here are labeled **F1, F2, ...** — deliberately not continuing the
backend's "Sprint 1–17" numbering, so a reference to "Sprint 6" is never
ambiguous between the two repos' planning docs.

---

## 1. Sequencing

| Status | Sprint | Epic | Points | Why this order |
|---|---|---|---|---|
| `[x]` Done | F1 | EPIC-F00 — Company Research search + retry | 8 | Proves the whole stack end-to-end on the backend's most complete flow first, before investing in shell/nav for screens that don't exist yet |
| `[ ]` Planned | F2 | EPIC-F01 — App shell & navigation | 5 | Every later screen needs somewhere to live; do this before adding more routes, not after |
| `[ ]` Planned | F3 | EPIC-F02 — Generated API client | 5 | Explicitly flagged in EPIC-F00's own README as a "revisit once a second module gets a screen" tradeoff — that threshold is F4, so switch before it, not after six modules have hand-written types to migrate |
| `[ ]` Planned | F4 | EPIC-F03 — Company screens | 8 | First full CRUD module; establishes the list/create/detail/edit/delete pattern the rest reuse |
| `[ ]` Planned | F5 | EPIC-F04 — Contact screens | 5 | Same shape as F4, should be faster now the pattern exists |
| `[ ]` Planned | F6 | EPIC-F05 — Lead screens | 5 | Same shape; also the module that visibly surfaces `LeadSource.AI_RESEARCH` |
| `[ ]` Planned | F7 | EPIC-F06 — Discovery screens | 5 | Same shape |
| `[ ]` Planned | F8 | EPIC-F07 — Assessment screens + lifecycle action | 8 | First non-pure-CRUD module (the `/start` action) — costs more than F5–F7 |
| `[ ]` Planned | F9 | EPIC-F10 — Cross-entity drill-down | 5 | Needs Company/Contact/Lead (F4–F6) done first to have something to link to; pulled forward ahead of F10/F11 below since it makes every screen shipped so far more useful immediately |
| `[ ]` Planned | F10 | EPIC-F08 — Recommendation screens | 3 | Read-mostly, cheap, no urgency either way |
| `[ ]` Planned | F11 | EPIC-F09 — Qualification screens | 5 | Least-understood module going in (see backlog's open note) — sequenced after the others so its shape can be scoped from a live `/openapi.json` check, not memory |
| `[ ]` Planned | F12 | EPIC-F11 — Admin diagnostics view | 2 | Cheapest epic, no dependency on anything else — natural place to end the sequence or slot in wherever there's spare capacity |

**Total:** 51 points across 12 sprints (F1 done, F2–F12 planned), matching
`frontend_backlog.md`'s total.

Note EPIC-F10 (cross-entity drill-down) is deliberately sequenced as F9,
*before* EPIC-F08/F09 in sprint order — reordered from the backlog's own
listing because drill-down makes every already-shipped screen more useful
immediately, whereas Recommendation/Qualification screens don't depend on
it. Sprint order here is the actual intended sequence; `frontend_backlog.md`'s
epic numbering (F00–F11) is a stable ID scheme, not a schedule.

---

## 2. Assumptions

- Solo developer + AI pair-programming, same capacity model as the backend
  (see `Backend/docs/pamacore_sprint_plan.md` §1) — but **no velocity
  assumption is set here**. The backend's own experience this project
  (10 pts/week assumed, actual delivery far faster for well-specified
  coding work) suggests a fixed points/week number would be more
  theater than signal for a solo AI-paired stream. Track actuals in §3
  below instead of forecasting against an assumption.
- Each CRUD-shaped epic (F4–F8, F11) assumes the pattern established in
  F4 (Company) is genuinely reusable — if it isn't, re-estimate F5 onward
  rather than forcing the same point value.

## 3. Actuals

| Sprint | Epic | Points | Shipped | Notes |
|---|---|---|---|---|
| F1 | EPIC-F00 | 8 | 2026-08-15 | See `frontend_backlog.md` EPIC-F00 and `Frontend/README.md`. Live-verified DTO shapes against the backend's real `/openapi.json`; full pipeline success run blocked by the backend's exhausted daily AI budget (a backend-side constraint, not a frontend defect). |

Fill in as sprints complete — same discipline as the backend's velocity
table, so drift between planned and actual is visible early, not
discovered after F12.

## 4. Status tracking convention

Same as the backend (`Backend/docs/pamacore_sprint_plan.md` §6):

```text
[ ] Backlog       — not yet started
[R] Ready         — meets Definition of Ready in frontend_backlog.md
[>] In Progress   — actively being worked
[?] In Review     — built, verifying (build + tests + live smoke check)
[x] Done          — meets Definition of Done
[!] Blocked       — note the blocker inline
```
