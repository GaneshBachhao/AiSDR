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
| `[x]` Done | F2 | EPIC-F01 — App shell & navigation (sidebar, v2) + EPIC-F01b — Command Center | 10 | Design review (2026-08-16) replaced the v1 horizontal nav before any CRUD screens were built on it — see `design_system.md`. Landed together since the shell and its landing page were designed as one piece |
| `[x]` Done | F3 | EPIC-F02 — Generated API client | 5 | Explicitly flagged in EPIC-F00's own README as a "revisit once a second module gets a screen" tradeoff — that threshold is F4, so switch before it, not after six modules have hand-written types to migrate |
| `[x]` Done | F4 | EPIC-F03 — Company screens | 8 | First full CRUD module; establishes the list/create/detail/edit/delete pattern the rest reuse |
| `[x]` Done | F5 | EPIC-F04 — Contact screens | 5 | Same shape as F4, should be faster now the pattern exists |
| `[x]` Done | F6 | EPIC-F05 — Lead screens | 5 | Same shape; also the module that visibly surfaces `LeadSource.AI_RESEARCH` |
| `[x]` Done | F7 | EPIC-F06 — Discovery screens | 5 | Same shape; also the real predecessor of Assessment (F8), not a parallel module |
| `[x]` Done | F8 | EPIC-F07 — Assessment screens + lifecycle action | 8 | First non-pure-CRUD module (the `/start` action) — costs more than F5–F7 |
| `[ ]` Planned | F9 | EPIC-F09 — Qualification screens | 5 | Moved up from last-in-backlog: confirmed (2026-08-16) that `Qualification` requires an `assessment_id` to exist at all, so it belongs immediately after F8, not after Recommendation. No longer "least understood" — its real DTO shape is now confirmed and documented in the backlog |
| `[ ]` Planned | F10 | EPIC-F08 — Recommendation screens | 3 | Read-mostly, cheap; sequenced after Qualification to match the corrected pipeline's Assess → Qualify → Recommend order |
| `[ ]` Planned | F11 | EPIC-F10 — Cross-entity drill-down | 5 | Needs every entity screen (F4–F10) to exist to link the full chain Company → Lead → Discovery → Assessment → Qualification → Recommendation — sequenced last of the screen work, not pulled forward, since partial drill-down between only a few modules is less valuable than the complete chain |
| `[ ]` Planned | F12 | EPIC-F11 — Admin diagnostics view | 2 | Cheapest epic, no dependency on anything else — natural place to end the sequence or slot in wherever there's spare capacity |

**Total:** 61 points across 12 sprints (F1–F2 done, F3–F12 planned),
matching `frontend_backlog.md`'s total. `PARK-F-AUTH`, `PARK-F-ACT`, and
`PARK-F-SEARCH` are excluded — none have a backend counterpart to build
against yet (see backlog's Parking Lot).

Sprint order here is the actual intended sequence; `frontend_backlog.md`'s
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
| F2 | EPIC-F01 (v1) | 5 | 2026-08-16 | v1 horizontal nav. Hit a real process bug mid-sprint (edits silently landed in a stale pre-restructure directory) — caught only because the unit test was strengthened to actually render and assert on DOM output instead of just checking the component instantiates. Superseded same day by the v2 revision below. |
| F2 | EPIC-F01 (v2) + EPIC-F01b | 10 | 2026-08-16 | Design review of an external UI/UX proposal, checked against the real domain code before adopting anything — confirmed `Discovery` really is business-needs-per-Lead (good), but corrected the proposed pipeline order (Qualification requires `assessment_id`, so Qualify comes after Assess, not before Discover Needs) and declined to build the Qualification screen's proposed 5-dimension score mockup, since no such fields exist in the backend. Command Center ships with real counts (live-verified against the running backend: 8 companies, 3 contacts, 3 leads, 3 discoveries, 2 assessments, 1 recommendation) — deliberately no fabricated trend deltas or synthesized "AI Intelligence"/"Needs Attention" content, since nothing in the backend generates that data yet. See `design_system.md` for the full design record. |
| F3 | EPIC-F02 | 5 | 2026-08-16 | Same day as F2. Generating against the live schema immediately paid for itself: found the reported "qualifications: 3" count above was wrong (a `422` error response's 3 JSON keys, miscounted as 3 records by a naive verification script — real count is 0), and that `/assessments`/`/recommendations` use `page`/`page_size`, not `limit` at all, so `DashboardCountsService`'s `?limit=500` was being silently ignored by both. Fixed using the real per-router param shapes now visible in `src/app/api/schema.d.ts`; live-verified the corrected requests against the running backend before calling it done. See `frontend_backlog.md` EPIC-F02 for the full record, including why `openapi-typescript` was chosen over a full Angular service generator. |
| F4 | EPIC-F03 | 8 | 2026-08-16 | Same day as F2/F3. First CRUD module — list/search/create/detail/edit/delete, all against generated types. Live-verified the full CRUD cycle against the real backend (not just mocked tests): create, read, update, search, delete, confirmed the 404 afterward, cleaned up the test record. Incidentally discovered the backend normalizes free-text `industry` input against its own taxonomy (`"Software"` → `"Information Technology"`) — the UI shows whatever comes back, not what was typed, which is correct but worth knowing for later modules with similar fields. |
| F5 | EPIC-F04 | 5 | 2026-08-16 | Same day. Confirmed two more per-router inconsistencies by checking the schema/live backend directly instead of assuming Company's shape: `/contacts/search` uses `search_text` not `query`, and search only matches one field at a time (a two-word "first last" query matched nothing, live-verified). Second module hitting the exact same list/form/detail CSS as Company, so extracted `shared/styles/entity-screens.scss` and refactored Company onto it too, rather than copy-pasting a third time. Contact's mandatory `company_id` gets a real company picker on create (populated live) and a small real cross-link from Company detail's new "+ Add Contact" button. |
| F6 | EPIC-F05 | 5 | 2026-08-16 | Same day. Third distinct search param name (`keyword`) confirms this backend genuinely has no shared search convention across routers — expected by now, still checked rather than assumed. First real use of the `✦` AI-content-marker rule from `design_system.md` (a new shared `.badge-ai` class for `source: "AI Research"` leads). Lead needs both `company_id` and `contact_id` from matching companies, and the backend 404s a mismatched pair — the create form's contact picker filters by the selected company client-side to make a bad combination unselectable, with that filtering logic unit-tested directly rather than only implied by manual testing. Live-verified updating a Lead's `status` to `"Qualified"` correctly cascades `is_qualified: true` from the domain layer. Two follow-up fixes landed the same day after user reports: Lead's status column was plain text (and the detail page's badge was hardcoded green regardless of real status) — fixed with one shared `leadStatusBadgeClass()`; then the "New" badge turned out unreadable (near-white on white), fixed with a real blue `.badge-info` fill instead of a border-only tweak. |
| F7 | EPIC-F06 | 5 | 2026-08-16 | Same day. `DiscoveryStatus` isn't an OpenAPI enum like Lead's were — transcribed the real 5 values from the backend enum source by hand, flagged to keep in sync manually. Found a real domain rule live rather than in any doc: one Discovery per Lead, enforced with a `409` — every dev-database Lead already had one, so had to create a fresh Lead to test the actual happy path. Since every needs field is genuinely optional on create and update, added a real "N / 4 captured" completeness indicator instead of a screen that implies completeness just because a record exists. Extracted `LeadDisplayService` (second module needing the same Lead → Company/Contact join) and refactored Lead's own list/detail onto it — behavior-preserving, all 33 prior tests stayed green unchanged. |
| F8 | EPIC-F07 | 8 | 2026-08-16 | Same day. First lifecycle-action module: `POST /assessments/{id}/start` drives `Created → In Progress`, the only status transition reachable through the REST API today (`UpdateAssessmentRequestDTO` has no `status` field, and no endpoint reaches `Under Review`/`Completed`/`Cancelled`) — the edit form and detail view both reflect that honestly rather than pretending a fuller lifecycle exists. `CreateAssessmentRequestDTO` is minimal (`discovery_id` only), and the backend's four structurally-identical response DTOs were consolidated to one canonical alias. Also fixed a real, growing build problem found while shipping this module: Sass `@use` of the shared `entity-screens.scss` partial (EPIC-F04) was duplicating its CSS into every one of the (by now 15) consuming components' own compiled stylesheets, which tripped Angular's per-component style budget on 6 of them. Moved the shared rules into the global `src/styles.scss` instead (no per-component duplication), deleted the partial, and stripped the now-unneeded `@use` line from all 15 files — `ng build` confirmed clean afterward, all prior tests stayed green, purely internal restructuring. Live-verified the full lifecycle against the real backend: created an Assessment against an existing Discovery with none yet, called `/start`, confirmed the `In Progress` transition, updated the findings fields, deleted, confirmed the `404`. 63 tests total now across 17 files. |

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
