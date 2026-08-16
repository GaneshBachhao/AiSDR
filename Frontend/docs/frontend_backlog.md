# AiSDR Frontend — Backlog

Source of truth for frontend scope. Companion to
[`frontend_sprint_plan.md`](frontend_sprint_plan.md) (schedule) and
[`design_system.md`](design_system.md) (visual system, information
architecture, and the corrected pipeline order — read that before touching
navigation or any entity workspace screen). Mirrors the structure of the
backend's `Backend/docs/product_backlog.md` for consistency, but is
**deliberately informal/untracked** — not part of the backend's committed
17-epic roadmap, per the 2026-08-15 decision to keep frontend work separate
for now. Revisit that decision once this backlog's shape is proven out.

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
| `[x]` Done | EPIC-F01 | App shell & navigation (v2: sidebar, corrected pipeline order) | — | 5 |
| `[x]` Done | EPIC-F01b | Command Center (real KPI/pipeline counts) | company/contact/lead/discovery/assessment/qualification/recommendation (list endpoints only) | 5 |
| `[ ]` Backlog | EPIC-F02 | Generated API client (replace hand-written types) | all | 5 |
| `[ ]` Backlog | EPIC-F03 | Company screens | `company_router` | 8 |
| `[ ]` Backlog | EPIC-F04 | Contact screens | `contact_router` | 5 |
| `[ ]` Backlog | EPIC-F05 | Lead screens | `lead_router` | 5 |
| `[ ]` Backlog | EPIC-F06 | Discovery screens | `discovery_router` | 5 |
| `[x]` Done | EPIC-F07 | Assessment screens + lifecycle action | `assessment_router` | 8 |
| `[ ]` Backlog | EPIC-F08 | Recommendation screens (read-mostly) | `recommendation_router` | 3 |
| `[ ]` Backlog | EPIC-F09 | Qualification screens | `qualification_router` | 5 |
| `[ ]` Backlog | EPIC-F10 | Cross-entity drill-down | company/contact/lead/discovery/assessment/recommendation | 5 |
| `[ ]` Backlog | EPIC-F11 | Admin diagnostics view | `admin_router` | 2 |
| `[ ]` Parked | PARK-F-AUTH | Authentication | — | — |
| `[ ]` Parked | PARK-F-ACT | Actions (persisted) | — (no backend router exists) | — |
| `[ ]` Parked | PARK-F-SEARCH | Global search / command palette | — (no search endpoint or index exists) | — |

**Total sequenced scope:** 61 points across 12 epics (excludes the parked
epics, none of which have a backend counterpart to build against yet).

---

## Epic Detail

### EPIC-F00 — Company Research search + retry · `[x]` Done

Shipped 2026-08-15. `src/app/company-research/` — search form,
results/failures tables, retry action. See `Frontend/README.md` for what it
covers and its documented first-slice tradeoffs (hand-written types,
template-driven form, no auth).

### EPIC-F01 — App shell & navigation (5 pts) · `[x]` Done (v2, revised 2026-08-16)

Originally shipped 2026-08-16 as a horizontal top nav bar. **Revised the
same day**, before any CRUD screens were built on top of it, after a design
review surfaced that a flat module list doesn't communicate the product's
actual pipeline, and that horizontal space runs out fast once auth/search
land. See `design_system.md` for the full reasoning and the corrected IA.

`App` (`app.ts`/`app.html`/`app.scss`) is now a **left sidebar**, grouped
by pipeline stage (Discover / Discover Needs / Assess / Qualify /
Recommend / Act), with Command Center and Admin as ungrouped top/bottom
entries. Every module still has a real route from day one via
`app.routes.ts`, most pointing at the shared
`shared/coming-soon/coming-soon.ts` placeholder until its own epic ships.
`''` now redirects to `command-center` (EPIC-F01b), not `company-research`
— Company Research is a Discover-stage tool, not the product's front door.

| Story | Acceptance Criteria | Status |
|---|---|---|
| Left sidebar layout | Persistent shell wrapping `<router-outlet>`, not per-page duplication | `[x]` Done |
| Navigation grouped by real pipeline stage | Groups match the verified dependency order (Qualify after Assess, not before) — see `design_system.md` §2 | `[x]` Done |
| Route structure supports the rest of this backlog | `app.routes.ts` has a named route per module, plus `command-center` and `actions`, even before each screen is built (can lazy-stub) | `[x]` Done |
| Design tokens shared app-wide | `src/styles.scss` root CSS custom properties (`design_system.md` §4); existing `company-research.scss` and `coming-soon.ts` re-themed to use them instead of their own hardcoded palette | `[x]` Done |

**A mistake worth recording (from the v1 pass):** the first attempt at
this epic wrote its five files to a stale path left over from before the
Backend/Frontend restructure (missing the `AiSDR/` segment), silently
recreating a disconnected directory tree instead of editing the real
project — `ng build`/`ng test` kept passing because they were unknowingly
running against the *old*, unchanged app the whole time. Caught by writing
a real assertion (`app.spec.ts` calls `fixture.detectChanges()` and checks
actual rendered DOM, not just "does the component instantiate") — that
test failed with an empty node list, which is what surfaced the stale
directory. Stray directory removed; files rewritten at the correct path;
rebuilt and retested clean. `app.spec.ts` now also asserts the nav group
headings render in the corrected pipeline order, so a future regression to
the wrong order would fail a real test, not just look wrong on screen.

### EPIC-F01b — Command Center (5 pts) · `[x]` Done

Shipped 2026-08-16, alongside the EPIC-F01 revision. Landing page
(`src/app/command-center/`) with a KPI strip (Companies/Contacts/Leads/
Recommendations) and a pipeline visual (Companies → Leads → Discoveries →
Assessments → Qualifications, the real dependency order). Every number is
real, fetched live from the existing list endpoints — no fabricated trend
deltas, no synthesized "AI Intelligence" or "Needs Attention" content (both
would need cross-entity synthesis logic that doesn't exist in the backend
today; see `design_system.md` §6 for exactly what was deferred and why).

Because no aggregate/stats endpoint exists, `DashboardCountsService`
fetches each module's list endpoint with `?limit=500` and uses the
response array's length as the count — an approximation, not a true total,
once any module exceeds 500 records. Documented in the service's own
comments and in `design_system.md` §6, not silently assumed accurate.

**Live-verified against the real backend:** confirmed real record counts
via direct API calls before/independent of the Angular service, and added
`dashboard-counts.service.spec.ts` — a real `HttpTestingController`-backed
test proving the service issues all seven requests and maps each response
to the correct field, not just that the class constructs.

**Correction (found during EPIC-F02, 2026-08-16):** the "qualifications: 3"
count reported here at ship time was wrong, and the wrongness was itself
informative. `?limit=500` against `/qualifications` actually fails with a
`422` (that router caps `limit` at 200) — my verification script's naive
`len(response_json)` was quietly counting the **3 keys of the error
response object** (`success`/`message`/`errors`), not 3 real records. The
real count is 0. Separately, `/assessments` and `/recommendations` don't
accept `limit` at all (they use `page`/`page_size`); FastAPI silently
ignored the unrecognized param and fell back to `page_size=10`, which
happened to still be correct only because both real counts were under 10.
Both are fixed under EPIC-F02 below, once the generated schema made the
real per-router parameter names impossible to keep guessing at.

### EPIC-F02 — Generated API client (5 pts) · `[x]` Done

Shipped 2026-08-16. Evaluated `openapi-typescript` (types-only, framework-
agnostic) against Angular-specific service generators (`ng-openapi-gen`
and similar); **chose `openapi-typescript` + hand-written thin services**,
not full service generation — this Angular 22 scaffold is brand new
(bundled TypeScript 6, released ahead of `openapi-typescript`'s declared
`^5.x` peer range, needed `--legacy-peer-deps` to install), and a
heavier, Angular-specific generator carries more version-compatibility
risk for less benefit at this app's current size. Types are generated
into `src/app/api/schema.d.ts` (tracked in git; the raw fetched
`openapi.json` is not, since it's a disposable intermediate); regenerate
with `npm run generate:api` (fetches the live `/openapi.json` from
`http://127.0.0.1:8000`, requires the backend running).

| Story | Acceptance Criteria | Status |
|---|---|---|
| Generate TS types + HTTP clients from `/openapi.json` | Evaluated both approaches, documented the choice above | `[x]` Done |
| Migrate `company-research.models.ts` to generated equivalents | Now type aliases onto `components['schemas'][...]` from the generated schema, not hand-written interfaces; existing EPIC-F00 screen's behavior unchanged (build + tests green, same field names preserved so no downstream changes needed beyond two null-safety fixes below) | `[x]` Done |
| Regeneration is a documented, repeatable command | `npm run generate:api` in `package.json`; documented in `Frontend/README.md` | `[x]` Done |

**Real bug found and fixed as a direct result of this epic:** generating
against the live schema exposed that `DashboardCountsService`
(EPIC-F01b, shipped one sprint earlier) was guessing wrong on two
counts — `/qualifications` caps `limit` at 200 (sending 500 caused a
`422`, which failed the whole dashboard load), and `/assessments`/
`/recommendations` don't use `limit` at all (they use `page`/`page_size`;
the unrecognized `limit` param was silently ignored by FastAPI, so both
counts were coincidentally right only because their real counts were
under the default `page_size` of 10). Fixed by reading the actual
generated operation types for each endpoint instead of assuming a uniform
convention — see `dashboard-counts.service.ts`'s own header comment for
the per-router breakdown. Live-verified the corrected param shapes
directly against the running backend before considering this closed.

**Also surfaced, not fixed here:** the generated type for
`list_qualifications`'s response body is `unknown`, not a proper DTO
array — the backend route is missing a `response_model=list[...]`
annotation that every sibling list endpoint has. Backend-side gap, left
for whoever picks up EPIC-F09 (Qualification screens) or a backend sprint,
not fixed from the frontend.

**Two null-safety fixes needed migrating off hand-written types:** the
hand-written interfaces had declared `results`/`failures`/
`discovered_contacts` etc. as always-present arrays; the generated types
correctly mark them optional, since Pydantic fields with
`default_factory=list` aren't in a JSON Schema's `required` list. Fixed
with `?? []` at the two call sites that assumed non-optional — a real
(if minor) accuracy improvement over the hand-written version, not just a
mechanical migration.

### EPIC-F03 — Company screens (8 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/companies/` — `company-list` (table +
search), `company-form` (shared create/edit, mode determined by whether
the route has an `:id`), `company-detail` (read view + Edit/Delete
actions). Establishes the list/form/detail pattern the remaining CRUD
epics (F04–F07, F09) reuse.

| Story | Acceptance Criteria | Status |
|---|---|---|
| List + search | Table view, calls `GET /companies` and `/companies/search` | `[x]` Done |
| Create | Form against `POST /companies` | `[x]` Done |
| Detail view | `GET /companies/{id}` | `[x]` Done |
| Edit | Form against `PUT /companies/{id}` | `[x]` Done |
| Delete | Confirm dialog, `DELETE /companies/{id}` | `[x]` Done (native `confirm()`, not a custom modal — revisit if a modal pattern is needed elsewhere) |

**Live-verified full CRUD cycle against the real backend**, matching the
exact request/response shapes the Angular service sends (not just the
DTOs in isolation): created a real Company, confirmed the backend
normalizes free-text `industry` input against its own taxonomy
(`"Software"` in → `"Information Technology"` out — worth knowing since
the detail/list views correctly show whatever the backend returns, not
what was typed), updated `employee_count`, confirmed it via `/search`,
deleted it, and confirmed the delete with a real `404` in the exact
`{success, message, error_code, details}` shape `describeError()` expects.
Test record cleaned up, not left in the real database.

12 tests total across `company.service.spec.ts` (all six HTTP verbs,
correct URLs/methods/bodies) and `company-list.spec.ts` (real rendered-DOM
assertions for both the happy path and a failed-load error state — not
component-instantiation-only tests).

### EPIC-F04 — Contact screens (5 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/contacts/` — same list/form/detail pattern as
EPIC-F03. Two real differences from Company found by checking the
generated schema/live backend directly rather than assuming Company's
shape carries over:

- **`/contacts/search` uses `search_text`, not `query`** (Company's param
  name) — a second confirmation that this backend's routers don't share a
  uniform pagination/search convention; check each one.
- **Search only matches one field at a time.** Live-verified: searching
  `"SearchProbe"` (first name) or a lowercase substring of it both matched;
  searching `"Live Test"` (first name + last name together) matched
  nothing, even though a contact named exactly that existed. The backend
  doesn't search a concatenated "first + last name" string. Reflected
  honestly in the search input's placeholder text rather than implying
  full-name search works.

Contact's `company_id` is a mandatory foreign key with no search-by-company
filter on the list endpoint, so:
- **Create** shows a company picker (`<select>`, populated from
  `CompanyService.list()`) — the "New Contact" link on a Company's detail
  page pre-selects it via a `company_id` query param, a small real cross-
  link (not the full EPIC-F10 drill-down epic, just reusing the picker's
  own preselection support).
- **Edit** shows the company as read-only context (`UpdateContactRequestDTO`
  has no `company_id` field at all — it isn't updatable through this
  endpoint), and the list/detail views resolve `company_id` to a real
  company name via a second fetch rather than showing a raw UUID.

**Shared styles extracted** (`src/app/shared/styles/entity-screens.scss`):
this is the second module to need the exact same list/form/detail CSS as
Company, so it was pulled out into one `@use`-able partial instead of
copy-pasted a second time; Company's stylesheets were refactored onto it
too, not just Contact's.

**Live-verified full CRUD cycle against the real backend**: created a real
Contact against a real Company id, read it back, updated `phone`, searched
for it (confirming the single-field-only search behavior above), deleted
it, confirmed the 404. Test records cleaned up. 19 tests total across the
whole frontend now (6 test files), including a real DOM assertion proving
the company-name resolution actually renders, not just that the two HTTP
calls fire.

### EPIC-F05 — Lead screens (5 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/leads/` — same list/form/detail pattern, on
the shared `entity-screens.scss`. Real findings from checking the schema
directly rather than assuming:

- **`/leads/search` uses `keyword`** — a third distinct param name
  (Company: `query`, Contact: `search_text`, Lead: `keyword`). Every CRUD
  module so far has used a different one; still not worth normalizing
  client-side, just worth continuing to check each one.
- **`source: "AI Research"` gets a distinct `✦ AI Research` badge**,
  using a new shared `.badge-ai` class (cyan-tinted, per
  `design_system.md` §5's "one AI marker" rule) — the first real use of
  that design-system rule in actual UI, not just documented intent.
  Live-verified: created a real Lead with `source: "AI Research"`, and
  updating its `status` to `"Qualified"` correctly cascaded
  `is_qualified: true` in the response (the domain's own
  `update_status()` behavior, not something the frontend computes).
- **Lead requires both `company_id` and `contact_id`, and the backend
  rejects a mismatched pair** (a Contact from a different Company) with a
  404. The create form fetches all Contacts once and filters the picker
  to the selected Company client-side, so a mismatched combination can't
  be submitted in the first place — the filtering logic itself is
  unit-tested directly (`lead-form.spec.ts`), not just implied by the
  UI working in passing.
- **`UpdateLeadRequestDTO` allows changing `contact_id` and `status`, but
  not `company_id`** — matches Company/Contact's pattern of the parent
  relationship being create-time-only, but Lead's own contact link is
  more flexible than Contact's company link was.

Cross-links added (not the full EPIC-F10 epic, just reusing the same
preselection pattern EPIC-F04 established): Company detail gained
"+ Add Lead"; Contact detail gained "+ Add Lead" preselecting both
`company_id` and `contact_id`.

28 tests total across 9 files now. Full CRUD cycle live-verified against
the real backend; test record cleaned up.

**Fix (2026-08-16, same day, caught by inspection):** the initial ship
rendered `status` as plain text in the list — inconsistent with the
Active/Inactive color-badge treatment every other module uses — and the
detail page's status badge was worse: hardcoded to `.badge-ok` regardless
of the lead's actual status, so a Disqualified lead would have shown a
green "success" badge. Added `leadStatusBadgeClass()` (`lead.models.ts`) —
Qualified/Converted → ok, Disqualified → fail, Contacted → warn,
New/Closed → neutral — used identically by both the list and detail
views, plus a dedicated `lead.models.spec.ts` asserting the mapping and an
extended `lead-list.spec.ts` assertion checking the actual rendered badge
class, not just the status text. 32 tests total now.

**Second fix, same day:** the color-badge fix above was correctly compiled
and served (confirmed by inspecting the actual served bundle), but user
report said it still looked like plain text — root cause was contrast, not
staleness: `.badge-neutral`'s background (`--color-bg`, `#f8fafc`) sits on
a table whose own background is `--color-surface` (`#ffffff`), a
~1%-lightness difference that reads as invisible. `New`/`Closed` (the two
statuses mapped to neutral) were affected; `New` is also the default
status every Lead starts at, so this was the *first* badge most people
would ever see. Fixed by giving the shared `.badge` base class a
`1px solid transparent` border and setting a real `border-color` on
`.badge-neutral` specifically — the colored variants (ok/fail/warn/ai)
already had enough of their own contrast and are visually unchanged.

**Third fix, same day (a border alone wasn't enough):** the border fix
was confirmed compiled and served, but a border-only badge (no fill) still
reads as an outline, not a "colored badge" — exactly the follow-up report
("New showing with borders only"). Rather than tune `.badge-neutral`'s
near-white fill further, added a real second variant: `.badge-info`
(reusing the existing `--color-accent-soft`/`--color-accent` tokens — the
same blue used for active nav/primary buttons), and remapped
`New → badge-info`. `.badge-neutral` also got a genuinely visible gray
fill (`--color-border` instead of `--color-bg`) rather than only a border,
reserved now for truly inert/terminal states (`Closed`) where no color
signal is warranted. Confirmed the exact CSS the dev server was serving
after each of these three passes by inspecting the compiled bundle
directly, not just assuming a rebuild took effect.

### EPIC-F06 — Discovery screens (5 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/discoveries/` — same list/form/detail
pattern, `/discoveries/search` uses `search_text` (same as Contact).

- **`DiscoveryStatus` isn't exposed as an OpenAPI enum** the way
  `LeadStatus`/`LeadSource` are — the generated schema types `status` as a
  bare `string`. Transcribed the real 5 values (`CREATED`, `IN_PROGRESS`,
  `ON_HOLD`, `COMPLETED`, `CANCELLED`) directly from
  `Backend/app/domain/discovery/enums/discovery_status.py` into
  `DISCOVERY_STATUSES`, flagged in a comment to keep in sync by hand since
  it can't be generated. `discoveryStatusBadgeClass()` reuses the same
  badge vocabulary Lead's status fix established (`CREATED` → `badge-info`,
  not the washed-out neutral one).
- **Every needs field is honestly optional, and the UI says so.** All 4 of
  `problem_statement`/`current_solution`/`business_impact`/
  `success_criteria` are nullable on create *and* update — live data
  confirmed most records only have 1 of 4 filled. Added
  `discoveryCompleteness()` (a real "N / 4 captured" indicator, own unit
  tests) instead of a screen that implies a record is complete just
  because it exists; the detail view renders each unfilled field as an
  explicit italicized "Not yet captured", not a blank space that looks
  like a rendering bug.
- **One real domain rule found live, not in any doc:** the backend
  rejects creating a second Discovery for the same Lead with a `409`
  ("Discovery already exists for this lead") — discovered because every
  existing Lead in the dev database already had one. The error surfaces
  correctly through the existing `describeError()` handling without any
  special-casing needed. Not proactively hidden in the UI (e.g. disabling
  "+ Add Discovery" when one exists) — deferred, since that needs an extra
  fetch per Lead detail view for a one-Discovery-per-Lead edge case that's
  already handled honestly via the error message.
- **Extracted `LeadDisplayService`** (`app/leads/lead-display.service.ts`)
  — the second module needing the exact "Lead → real Company/Contact
  names" join `LeadList`/`LeadDetail` already did inline. Refactored both
  onto the shared service (behavior-preserving — all 33 pre-existing tests
  still passed unchanged) rather than duplicating the triple-fetch a third
  time.

Cross-link added: Lead detail gained "+ Add Discovery".

Live-verified full CRUD against the real backend: hit the real
one-per-lead conflict first (informative in itself), then created a fresh
Lead to test the actual happy path — create, read, a partial update
(added `success_criteria` while `current_solution` stayed `null`,
confirming the honest-partial-completeness design holds against real
data), search, delete. Both test records (Discovery and the fresh Lead)
cleaned up. 51 tests total now across 14 files.

### EPIC-F07 — Assessment screens + lifecycle action (8 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/assessments/` — same list/form/detail pattern,
plus a real lifecycle action (`POST /assessments/{id}/start`), the first
non-CRUD backend action any frontend module has driven.

| Story | Acceptance Criteria | Status |
|---|---|---|
| List + create + detail + edit + delete | Same pattern as EPIC-F03 | `[x]` Done |
| "Start" action on the detail view | Calls `POST /assessments/{id}/start`, reflects the resulting status without a full page reload | `[x]` Done |

Real findings from checking the schema/live backend directly:

- **The backend emits four structurally-identical response DTOs**
  (`Create/Get/List/UpdateAssessmentResponseDTO`) instead of one shared
  shape. Verified field-for-field identical in the generated schema, so the
  frontend uses one canonical `AssessmentResponseDTO` alias (onto
  `GetAssessmentResponseDTO`) everywhere rather than juggling four names
  for the same data.
- **No `/assessments/search` endpoint exists at all** (unlike every prior
  module) — `list()` only supports `page`/`page_size`/`discovery_id`, so
  there's no search bar on this list screen; the subtitle says so honestly
  instead of implying search exists.
- **`CreateAssessmentRequestDTO` has exactly one field, `discovery_id`** —
  create mode is intentionally minimal (a discovery picker, nothing else);
  every other field is set later via edit or produced by the domain layer.
- **No reachable status transition exists through the REST API except
  `Created → In Progress` via `/start`.** `UpdateAssessmentRequestDTO` has
  no `status` field at all, and no other endpoint moves an assessment to
  `Under Review`/`Completed`/`Cancelled`. The edit form doesn't pretend
  otherwise — no status field is shown there, only a code comment
  explaining why; the detail view's "Start Assessment" button is
  conditionally shown only when `status === 'Created'`, since that's the
  only transition this API surface actually supports today.
- **`AssessmentStatus`/`MaturityLevel` aren't OpenAPI enums**, same
  situation as `DiscoveryStatus` — transcribed by hand from
  `Backend/app/domain/assessment/enums/{assessment_status,maturity_level}.py`,
  flagged in a comment to keep in sync manually.

Cross-link added: Discovery detail gained "+ Add Assessment".

**Shared-style duplication fixed, same day.** Building this module brought
the count of components `@use`-ing the shared `entity-screens.scss`
partial (EPIC-F04) to 15, which tripped Angular's per-component 4KB style
budget on 6 of them. Root cause: Sass `@use` of a partial containing real
CSS rules (not just variables/mixins) compiles those rules into *every*
consuming component's own view-encapsulated stylesheet — the shared CSS
was being duplicated 15 times, not shared once, and would only keep
getting worse as more modules ship. Fixed by moving the shared rules out
of the per-component-`@use`d partial and into the global `src/styles.scss`
(not view-encapsulated, applies app-wide without duplication), deleting
`entity-screens.scss`, and removing the now-unnecessary `@use` line from
all 15 consuming component `.scss` files. `ng build` confirmed clean (no
budget warnings) afterward, and all pre-existing tests stayed green — a
pure internal restructuring, no visual or behavioral change.

Live-verified full lifecycle against the real backend: found an existing
Discovery with no Assessment yet (`aa00d632-...`), created an Assessment
against it (`status: "Created"`), called `/start` and confirmed the
transition to `"In Progress"`, updated `summary`/`maturity_level`/
`readiness_score`/strengths-weaknesses-opportunities-risks (confirmed
`status` stayed unaffected by the update, as expected since it's not on
`UpdateAssessmentRequestDTO`), then deleted the test record and confirmed
the resulting `404`. 63 tests total now across 17 files, including
`assessment.models.spec.ts` (badge-mapping), `assessment.service.spec.ts`
(all five HTTP calls, including `/start`'s empty-body POST), and
`assessment-list.spec.ts` (real rendered-DOM assertion for the resolved
discovery label, maturity, readiness score, and status badge).

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
(`POST/GET {id}/GET/PUT/DELETE`), no search endpoint. Field set now
confirmed by reading the real domain code (2026-08-16, during the design
review): `QualificationResponseDTO` is `{ qualification_id, lead_id,
assessment_id, status (Qualified/Partially Qualified/Needs Nurturing/
Disqualified), score (single 0-100 float), recommendation (free text) }`
— no multi-dimension breakdown (no separate Fit/Intent/Timing/Business
Relevance/Tech Alignment fields exist anywhere in the backend). **Build
this screen against the real, simpler shape** — a richer scored breakdown
is a possible future *backend* feature request, not something to fake in
the UI. Also requires `Assessment` to exist first (`assessment_id` is
mandatory on create) — this screen makes the most sense reached via
EPIC-F10's drill-down from an Assessment, not as a cold-start standalone
list.

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
