# AiSDR Frontend — Backlog

Source of truth for frontend scope. Companion to
[`frontend_sprint_plan.md`](frontend_sprint_plan.md) (schedule). Mirrors the
structure of the backend's `Backend/docs/product_backlog.md` for
consistency, but is **deliberately informal/untracked** — not part of the
backend's committed 17-epic roadmap, per the 2026-08-15 decision to keep
frontend work separate for now. Revisit that decision once this backlog's
shape is proven out.

Every epic here targets a router already registered and live in
`app/presentation/api/routers/__init__.py`. `ai_router.py` is excluded on
purpose — it exists in the backend but was never wired into `api_router`
(a known, already-flagged orphan, see `Backend/docs/product_backlog.md`
EPIC-14 notes), so there is nothing running to build a screen against.

---

## Definition of Ready

- The backend endpoint(s) the story needs are registered and reachable
  (confirmed via `Backend/app/presentation/api/routers/__init__.py`, not
  assumed from a DTO alone)
- Response DTO shape is known (checked against the live `/openapi.json`,
  not just recalled from a prior session)
- No open UX decision blocking the story (see "Open decisions" below)

## Definition of Done

- Component builds (`ng build`) and unit tests pass (`ng test`)
- TypeScript interfaces for any new DTO verified against the live
  `/openapi.json` schema (same discipline used for the company_research
  slice — see `Frontend/README.md`)
- At least one live smoke test against the real running backend, not just
  a mocked `HttpClient` in a spec file
- Nothing committed until explicitly requested (same standing rule as the
  backend repo)

---

## Epic Summary

| Status | Epic | Title | Backend router(s) | Points |
|---|---|---|---|---|
| `[x]` Done | EPIC-F00 | Company Research search + retry | `company_research_router` | 8 |
| `[ ]` Backlog | EPIC-F01 | App shell & navigation | — | 5 |
| `[ ]` Backlog | EPIC-F02 | Generated API client (replace hand-written types) | all | 5 |
| `[ ]` Backlog | EPIC-F03 | Company screens | `company_router` | 8 |
| `[ ]` Backlog | EPIC-F04 | Contact screens | `contact_router` | 5 |
| `[ ]` Backlog | EPIC-F05 | Lead screens | `lead_router` | 5 |
| `[ ]` Backlog | EPIC-F06 | Discovery screens | `discovery_router` | 5 |
| `[ ]` Backlog | EPIC-F07 | Assessment screens + lifecycle action | `assessment_router` | 8 |
| `[ ]` Backlog | EPIC-F08 | Recommendation screens (read-mostly) | `recommendation_router` | 3 |
| `[ ]` Backlog | EPIC-F09 | Qualification screens | `qualification_router` | 5 |
| `[ ]` Backlog | EPIC-F10 | Cross-entity drill-down | company/contact/lead/discovery/assessment/recommendation | 5 |
| `[ ]` Backlog | EPIC-F11 | Admin diagnostics view | `admin_router` | 2 |
| `[ ]` Parked | PARK-F-AUTH | Authentication | — | — |

**Total sequenced scope:** 51 points across 11 epics (excludes the parked
auth epic, which has no backend counterpart to build against yet).

---

## Epic Detail

### EPIC-F00 — Company Research search + retry · `[x]` Done

Shipped 2026-08-15. `src/app/company-research/` — search form,
results/failures tables, retry action. See `Frontend/README.md` for what it
covers and its documented first-slice tradeoffs (hand-written types,
template-driven form, no auth).

### EPIC-F01 — App shell & navigation (5 pts)

Right now there is exactly one route (`''`) and zero navigation — every
other epic below needs somewhere to link *from*. Do this first.

| Story | Acceptance Criteria |
|---|---|
| Top-level layout (header/sidebar) | Persistent shell wrapping `<router-outlet>`, not per-page duplication |
| Navigation linking every screen | One entry per epic below, using Angular's `routerLink`/`routerLinkActive` |
| Route structure supports the rest of this backlog | `app.routes.ts` has a named route per module (`/companies`, `/contacts`, `/leads`, `/discoveries`, `/assessments`, `/recommendations`, `/qualifications`, `/company-research`, `/admin`), even before each screen is built (can lazy-stub) |

### EPIC-F02 — Generated API client (5 pts)

`company-research.models.ts` was hand-written and explicitly flagged in the
README as a tradeoff to revisit "once a second module gets a screen." That
threshold is now — six more modules are coming. Do this **before** EPIC-F03
starts, not after, so nothing has to be redone.

| Story | Acceptance Criteria |
|---|---|
| Generate TS types + HTTP clients from `/openapi.json` | Evaluate `openapi-typescript` vs. Angular-specific generators; pick one, document the choice and the regeneration command |
| Migrate `company-research.models.ts`/`company-research.service.ts` to generated equivalents | Existing EPIC-F00 screen's behavior unchanged — regression-check by hand since there's no E2E suite yet |
| Regeneration is a documented, repeatable command | e.g. an `npm run generate:api` script pointed at the backend's live `/openapi.json` |

### EPIC-F03 — Company screens (8 pts)

Backend: `POST /companies`, `GET /companies`, `GET /companies/search`,
`GET /companies/{id}`, `PUT /companies/{id}`, `DELETE /companies/{id}`.

| Story | Acceptance Criteria |
|---|---|
| List + search | Table view, calls `GET /companies` and `/companies/search` |
| Create | Form against `POST /companies` |
| Detail view | `GET /companies/{id}` |
| Edit | Form against `PUT /companies/{id}` |
| Delete | Confirm dialog, `DELETE /companies/{id}` |

### EPIC-F04 — Contact screens (5 pts)

Backend: same CRUD + search shape as Company
(`POST/GET/GET search/GET {id}/PUT/DELETE /contacts`). Once EPIC-F03
establishes the list/create/detail/edit/delete component pattern, this
should be mostly repetition against a different DTO — hence fewer points
than EPIC-F03, which pays for establishing the pattern.

### EPIC-F05 — Lead screens (5 pts)

Same CRUD + search shape against `/leads`. Notable field to surface:
`source` (now includes `LeadSource.AI_RESEARCH` as of backend Sprint 9) —
worth a visibly distinct badge for research-originated leads vs. manually
created ones, mirroring the company_research screen's badge style.

### EPIC-F06 — Discovery screens (5 pts)

Same CRUD + search shape against `/discoveries`.

### EPIC-F07 — Assessment screens + lifecycle action (8 pts)

Backend: `POST/GET/GET {id}/PUT/DELETE /assessments`, plus
`POST /assessments/{id}/start` — a lifecycle action, not plain CRUD, so
this epic costs more than a same-shaped CRUD-only module.

| Story | Acceptance Criteria |
|---|---|
| List + create + detail + edit + delete | Same pattern as EPIC-F03 |
| "Start" action on the detail view | Calls `POST /assessments/{id}/start`, reflects the resulting status without a full page reload |

### EPIC-F08 — Recommendation screens (3 pts)

Backend: `POST/GET/GET {id} /recommendations` only — **no update or
delete** (AI-generated content, read-mostly by design, matches backend
Sprint 7's `CreateRecommendationHandler`). Lower points than other modules
because there's no edit/delete form to build. Detail view should render
`SolutionSummaryDTO` entries with the `is_existing_offering` flag shown
distinctly (existing Pamacore offering vs. AI-proposed generic idea) — the
backend went to real effort (Sprint 7) to keep that distinction meaningful;
don't flatten it away in the UI.

### EPIC-F09 — Qualification screens (5 pts)

Same CRUD shape against `/qualifications`
(`POST/GET {id}/GET/PUT/DELETE`), no search endpoint. Scope the actual
field set from the live `QualificationResponseDTO` when this epic starts —
not deeply covered in this session's prior work, so don't assume the shape
from memory.

### EPIC-F10 — Cross-entity drill-down (5 pts)

None of the screens above link to each other yet. A Company detail page
should surface its Contacts/Leads/Discoveries; a Lead should link to its
Contact and Company; a Discovery should link to its Assessment and
Recommendation. Do this once enough of EPIC-F03–F09 exist to have
somewhere to link *to* — namely after at least Company, Contact, and Lead
are done.

### EPIC-F11 — Admin diagnostics view (2 pts)

Surface `GET /admin/ai-config` (provider, model, key fingerprint, source)
in a simple read-only panel — mirrors what Sprint 1 built server-side.
Low points: one endpoint, no forms, no CRUD.

---

## Parking Lot

- **PARK-F-AUTH — Authentication.** The backend has no login endpoint, no
  session/JWT handling, nothing to build a login screen against yet (see
  `project_frontend_direction.md` session memory). Pull this in only once
  the backend actually adds auth — building a frontend login screen first
  would mean guessing at a contract that doesn't exist.

## Open decisions

- **Styling approach.** EPIC-F00 used hand-rolled SCSS with no design
  system. Worth deciding whether to adopt a component library (Angular
  Material, PrimeNG, or similar) before EPIC-F03 multiplies the same
  decision across six more modules — cheaper to decide once, early, than
  to retrofit six screens later.
- **State management.** EPIC-F00 uses local component signals only — fine
  for one screen. Once EPIC-F10 needs data to flow between screens
  (e.g. a Company detail page showing live Lead data), decide whether
  plain signals + services are still enough or whether a shared store is
  warranted. Don't introduce one speculatively before EPIC-F10 needs it.
