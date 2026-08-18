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
| `[x]` Done | EPIC-F02 | Generated API client (replace hand-written types) | all | 5 |
| `[x]` Done | EPIC-F03 | Company screens | `company_router` | 8 |
| `[x]` Done | EPIC-F04 | Contact screens | `contact_router` | 5 |
| `[x]` Done | EPIC-F05 | Lead screens | `lead_router` | 5 |
| `[x]` Done | EPIC-F06 | Discovery screens | `discovery_router` | 5 |
| `[x]` Done | EPIC-F07 | Assessment screens + lifecycle action | `assessment_router` | 8 |
| `[x]` Done | EPIC-F08 | Recommendation screens (read-mostly) | `recommendation_router` | 3 |
| `[x]` Done | EPIC-F09 | Qualification screens | `qualification_router` | 5 |
| `[x]` Done | EPIC-F10 | Cross-entity drill-down | company/contact/lead/discovery/assessment/recommendation | 5 |
| `[x]` Done | EPIC-F11 | Admin diagnostics view | `admin_router` | 2 |
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

### EPIC-F08 — Recommendation screens (3 pts) · `[x]` Done

Shipped 2026-08-17. `src/app/recommendations/` — list + detail, plus a
"generate" form instead of a real create form (`GenerateRecommendationRequest`
has exactly one field, `assessment_id`). Confirmed by reading
`recommendation_router.py` directly: only `POST/GET/GET {id}` are wired —
**no update or delete**, matching the plan's read-mostly-by-design
expectation. Detail view renders `SolutionSummaryDTO` entries with
`is_existing_offering` shown as a distinct badge (`✦ Existing Pamacore
offering` vs. a plain "AI-proposed idea") rather than flattened away, per
the plan's explicit instruction — the backend went to real effort to keep
that distinction meaningful.

Real findings from reading the router/handler source directly, not just
the generated schema:

- **`POST /recommendations` is really "generate", and it's idempotent per
  `assessment_id`** — confirmed by reading `CreateRecommendationHandler`:
  re-running it for an Assessment that already has a Recommendation
  returns the existing one instead of creating a duplicate (its own
  docstring says so explicitly). Live-verified: `POST`ing against an
  Assessment with an existing Recommendation returned `201` with the
  *same* `id`, not a new one. The form's button is labeled "Generate", not
  "Create", and its subtitle says so honestly.
- **Submit/Approve exist in the application layer but were never wired
  into any router endpoint** — `submit_recommendation_handler.py`/
  `approve_recommendation_handler.py` and their commands/validators are
  real, tested code, but `recommendation_router.py` only registers
  create/list/get. Confirmed by reading the router source line-by-line,
  not assumed from the handler files existing. This frontend can't drive
  a status transition beyond `Draft` for the same reason it couldn't drive
  Qualification cross-validation the backend doesn't enforce — the
  capability just isn't reachable through the API today. Noted in
  `recommendation.models.ts`'s own comment rather than silently building
  UI for endpoints that don't exist (the same orphaned-capability pattern
  already flagged for `ai_router.py` in `Backend/docs/product_backlog.md`).
- **`RecommendationStatus` isn't an OpenAPI enum**, same situation as
  `DiscoveryStatus`/`AssessmentStatus`/`QualificationStatus` — transcribed
  by hand from
  `Backend/app/domain/recommendation/enums/recommendation_status.py`.
- **Generation genuinely requires a working AI provider, and today's
  backend doesn't have one** — confirmed live: with a real Assessment that
  has no existing Recommendation, `POST /recommendations` throws all the
  way up to a raw, unhandled `500 Internal Server Error` (not the app's
  usual `{success, message, error_code, details}` shape). The server log
  traced it precisely to `GeminiProvider.execute()` raising
  `AIProviderException("Gemini provider execution failed")` — the same
  `GEMINI_MODEL` 404 already tracked as a known, standing blocker (see the
  `project_gemini_model_deprecated` session memory, dated 2026-08-15,
  which is a *backend* configuration issue, not something this frontend
  sprint can fix). A **second, separate gap** surfaced alongside it:
  `AIProviderException` has no exception handler mapped in the FastAPI
  app, unlike `ValidationException`/`NotFoundException`, so it leaks as an
  opaque 500 instead of a clean error body — worth a backend-side fix
  later, not fixed here. The frontend's generic `describeError()` fallback
  message already covers this gracefully (no `error.message`/`error.detail`
  to read from a raw 500, so it falls through to "Generation failed. Check
  that the API is running and the AI provider is configured." — accurate
  as written, no special-casing added).
- **Extracted `AssessmentDisplayService`, reused a third time** (see
  EPIC-F09) — Recommendation's list and detail both resolve
  `assessment_id` to its Discovery's problem statement through the same
  service Qualification's screens use, no new join code needed.

Cross-link added: Assessment detail gained "+ Generate Recommendation"
alongside "+ Add Qualification".

Live-verified against the real backend (which required restarting the dev
`uvicorn` server — it had stopped between sessions): confirmed `GET
/recommendations` and `GET /recommendations/{id}` against a real
AI-generated Recommendation created in an earlier sprint (before the
Gemini blocker), matching this module's typed shape exactly; confirmed the
idempotent-create path returns the same existing record rather than
duplicating it; created a fresh Assessment with real `summary` content and
confirmed generation fails with the traced `AIProviderException` above
(the expected, already-known failure mode, not a surprise); cleaned up the
test Assessment afterward. 88 tests total now across 24 files, including
`recommendation.models.spec.ts`, `recommendation.service.spec.ts`, and
`recommendation-list.spec.ts` (real rendered-DOM assertion for the
resolved assessment label, solution count, and status badge).

### EPIC-F09 — Qualification screens (5 pts) · `[x]` Done

Shipped 2026-08-16. `src/app/qualifications/` — same list/form/detail
pattern. Field set confirmed by reading the real domain code (2026-08-16,
during the earlier design review): `QualificationResponseDTO` is
`{ qualification_id, lead_id, assessment_id, status (Qualified/Partially
Qualified/Needs Nurturing/Disqualified), score (single 0-100 float),
recommendation (free text) }` — no multi-dimension breakdown (no separate
Fit/Intent/Timing/Business Relevance/Tech Alignment fields exist anywhere
in the backend). Built against this real, simpler shape rather than faking
a richer scored breakdown.

Real findings from checking the router/domain code directly rather than
assuming this module works like its siblings:

- **`qualification_router.py` has no `response_model=` on any route** —
  confirmed by reading the router source, not just the generated schema.
  `openapi-typescript` correctly emits `unknown` for every response body
  as a result, so there's no generated DTO to alias onto — the first
  module where that's true. `qualification.models.ts` hand-writes
  `QualificationResponseDTO` from the real application-layer DTO
  (`Backend/app/application/qualification/dto/qualification_response.py`)
  instead, flagged to keep in sync manually, the same discipline already
  used for `DiscoveryStatus`/`AssessmentStatus`. (A real fix exists —
  adding `response_model=` server-side — but that's a backend change, out
  of scope for this frontend sprint; first flagged as a gap back in
  EPIC-F02.)
  **Fixed 2026-08-18** (see `AiSDR/docs/intermediate_sprint_no_api_quota.md`,
  IS-3) — `qualification_router.py` now declares `response_model=` on
  every endpoint; `qualification.models.ts` swapped from the hand-written
  interfaces onto real `import type { components } from '../api/schema'`
  aliases, matching every other module.
- **`ListQualificationResponseDTO` genuinely omits `recommendation`** —
  not a doc error, confirmed by reading `qualification_mapper.py`'s
  `to_list_response` and live-verified: creating a Qualification with a
  `recommendation` set, then listing it back, showed the field absent from
  the list row entirely (not `null` — absent). The list screen doesn't
  render recommendation text anyway, so this cost nothing, but it's a real
  reason `QualificationResponseDTO` isn't reused uniformly across list vs.
  get/create/update the way Assessment's four DTOs were.
- **A new Qualification always starts `"Partially Qualified"` / score `0`
  regardless of what's requested, unless the create request explicitly
  sets `status`/`score`** — `Qualification.__init__` hardcodes those
  defaults; the create handler only calls `update_status()`/`update_score()`
  afterward if the request included a value. Live-verified: a bare
  `{lead_id, assessment_id}` create returned `"Partially Qualified"`/`0`
  exactly as the domain constructor sets them. `emptyQualificationForm()`
  matches this default rather than defaulting to something arbitrary.
- **The backend does not enforce that `assessment_id`'s discovery belongs
  to the given `lead_id`** — unlike Lead's company/contact 404, Qualification
  accepts any valid-UUID pair of an existing Lead and Assessment with no
  cross-check (confirmed by reading `QualificationValidator.validate_create`,
  which only checks UUID shape). The create form's Lead and Assessment
  pickers are therefore independent, not filtered against each other like
  Lead's contact picker was — a real, honestly-disclosed UX gap (a hint
  under the Assessment picker says so) rather than client-side validation
  the backend doesn't actually require.
- **Extracted `AssessmentDisplayService`** (`app/assessments/
  assessment-display.service.ts`), mirroring `LeadDisplayService`
  (EPIC-F06): the second place needing "Assessment → its Discovery's
  problem statement" (`AssessmentList` already did this inline) was
  `QualificationList`/`QualificationForm`/`QualificationDetail`, all
  needing the same join to show a human-readable assessment label instead
  of a raw UUID. Refactored `AssessmentList`/`AssessmentDetail` onto the
  shared service too, rather than adding a third inline copy — behavior-
  preserving, all 63 pre-existing tests stayed green unchanged.

Cross-link added: Assessment detail gained "+ Add Qualification"
(preselects `assessment_id` only — deriving the correct Lead would need a
third hop through the Assessment's Discovery, judged not worth the added
complexity given the backend doesn't require the pairing to be consistent
anyway).

**Shared-style budget note:** unlike every CRUD module since EPIC-F04,
Qualification's own component `.scss` files were written directly against
the global `styles.scss` tokens from the start (no `@use` of a per-
component partial) — the EPIC-F07 fix (global styles instead of a
duplicated `@use`d partial) landed before this module existed, so there
was nothing to migrate.

Live-verified full CRUD against the real backend: created a fresh
Assessment against an existing Discovery to get a valid `assessment_id`,
created a Qualification with only `lead_id`/`assessment_id` and confirmed
the domain default (`"Partially Qualified"`, score `0`), updated `status`
to `"Qualified"`/`score` to `88`/added a `recommendation`, confirmed via
`GET`, confirmed the list row's `recommendation` field is genuinely
absent (not `null`), deleted both the Qualification and the test
Assessment, and confirmed the resulting `404`s. 79 tests total now across
21 files, including `qualification.models.spec.ts`, `qualification.
service.spec.ts`, `qualification-list.spec.ts` (real rendered-DOM
assertion for the resolved lead/assessment labels, score, and status
badge), and a new `assessment-display.service.spec.ts` for the extracted
service.

### EPIC-F10 — Cross-entity drill-down (5 pts) · `[x]` Done

Shipped 2026-08-17. "A Lead should link to its Contact and Company" was
already true going into this epic — `LeadDetail` has linked both since
EPIC-F05/F06 via `LeadDisplayService`. The real remaining scope was the
other two asks:

- **Company detail surfaces its Contacts/Leads/Discoveries.** Three new
  sections added below the existing actions, each row linking to the real
  detail page. Checked each list endpoint's actual filter support instead
  of assuming symmetry: **Lead's list endpoint does support a `company_id`
  filter server-side** (`LeadService.listByCompany()`, new) — confirmed by
  reading `lead_router.py`, not assumed from Company's convention. Contact
  and Discovery have **no** such filter (Contact confirmed already in
  EPIC-F04; Discovery confirmed here by reading `discovery_router.py`,
  which only takes `skip`/`limit`), so Contacts are fetched in full
  (`limit=500`) and filtered client-side by `company_id`, and Discoveries
  are fetched in full and filtered by cross-referencing the company's own
  Lead ids (a Company → Leads → Discoveries two-hop, done inline in
  `CompanyDetail` rather than a new shared service, since this is the only
  screen that needs it).
- **Discovery detail links to its Assessment and Recommendation.** Before
  this epic, Discovery detail always showed a "+ Add Assessment" link
  regardless of whether one already existed. That was worse than
  cosmetically incomplete: reading `assessment_model.py` while wiring this
  up surfaced a **real, previously-undocumented backend gap** — `discovery_id`
  has a `unique=True` constraint at the persistence layer, so a second
  `POST /assessments` for a Discovery that already has one throws an
  unhandled `IntegrityError` that leaks as a raw `500`, not the clean `409`
  Discovery's own one-per-Lead rule gets. (A third instance of the same
  shape of gap as EPIC-F08's `AIProviderException` finding — a real
  constraint exists, but isn't mapped to a clean HTTP error. Not fixed
  here, consistent with this frontend track's standing decision to leave
  backend fixes to a backend sprint.) The practical fix on this side:
  `AssessmentService.listByDiscovery()` (new, server-side `discovery_id`
  filter — confirmed working via `assessment_router.py`) checks for an
  existing Assessment first, and the detail view now shows "View
  Assessment (status)" instead of the create link whenever one exists,
  which also incidentally prevents users from ever hitting that 500 by
  clicking a stale create link. Once an Assessment is found, its
  Recommendation (if any) is resolved the same way `AssessmentDisplayService`
  resolves Discovery labels for Assessments — fetch the (capped, page_size
  200) full recommendation list and filter client-side by `assessment_id`,
  since `GET /recommendations` has no `assessment_id` filter — and shown
  as "View Recommendation (status)".

Live-verified the full real chain end-to-end against the real backend
(not just mocked tests): Company `Sprint7 Test Co ef30983a` → its one real
Contact (Jane Doe) and Lead (both correctly filtered) → that Lead's
Discovery (`776fe911-...`, correctly cross-referenced) → that Discovery's
real Assessment (`eb3d0f50-...`, found via the new `discovery_id` filter)
→ that Assessment's real Recommendation (`78de26ee-...`, found via
client-side filtering) — every hop matched exactly what the frontend's new
code would request and render. 91 tests total now across 26 files,
including new `company-detail.spec.ts` (real rendered-DOM assertions for
all three related-records sections, plus a negative assertion that an
unrelated company's contact/discovery don't leak in) and
`discovery-detail.spec.ts` (asserts the create-link-vs-existing-link
branching in both directions).

### EPIC-F11 — Admin diagnostics view (2 pts) · `[x]` Done

Shipped 2026-08-17. `src/app/admin/` — a single read-only panel, not the
list/form/detail triad every other module uses, matching this epic's
actual shape (one `GET`, no forms, no CRUD). Shows `default_provider`,
`fallback_order` (rendered as an arrow-joined chain, "None configured"
when empty), and a `providers` table (provider name, a real
Configured/Not configured badge, model, masked key fingerprint, key
source) — a direct alias onto the generated `AIConfigDiagnosticsResponse`/
`ProviderDiagnosticsSchema` schema types, no hand-transcription needed
since this router (unlike Qualification's) does have `response_model=`.

Real finding from the live response, not assumed from the DTO shape
alone: `key_fingerprint` is genuinely `null` (not an empty string) for an
unconfigured provider — confirmed against the real backend's
`azure_openai` entry — rendered as `—` rather than blank, consistent with
every other module's `.not-captured`-style null handling.

Live-verified against the real backend: `GET /admin/ai-config` returned
three real providers (`gemini`/`openai` configured via `.env`,
`azure_openai` not configured), matching the frontend's typed shape and
rendering exactly. 93 tests total now across 28 files, including
`admin.service.spec.ts` and `admin.spec.ts` (real rendered-DOM assertion
for the fallback-order chain, the masked fingerprint, and both the
configured and not-configured badge variants).

This closes out the full 12-sprint sequenced frontend backlog
(EPIC-F00–F11, 61 points) — every module from Company through Admin now
has a real, live-verified screen.

---

## Parking Lot

All three previously-parked epics required backend capability that didn't
exist yet. PARK-F-AUTH is now built (below); PARK-F-ACT and PARK-F-SEARCH
remain parked for the same original reason.

- **PARK-F-ACT — Actions (persisted).** No backend router exists for the
  pipeline's "Act" stage. Pull this in once one does.
- **PARK-F-SEARCH — Global search / command palette.** No cross-entity
  search endpoint or index exists. Pull this in once one does.

### PARK-F-AUTH — Authentication · `[x]` Done (2026-08-17)

Built full-stack, in both `Backend/` and `Frontend/` -- the first (and so
far only) piece of this frontend track's work that required a real
backend change, not just a screen against an existing endpoint. JWT
bearer-token auth, no self-service registration (users are provisioned by
a human operator via `Backend/scripts/create_user.py`), no refresh-token
flow (8h access token; expiry just logs the user out).

**Backend** (`app/domain/user/`, `app/application/user/`,
`app/infrastructure/security/`, new `users` table via Alembic
migration): a `User` aggregate (email + bcrypt password hash, own bounded
context, same shape as `Company`); `POST /auth/login` (issues a JWT) and
`GET /auth/me`; every other existing router (`company`, `contact`,
`lead`, `discovery`, `assessment`, `qualification`, `recommendation`,
`admin`, `company_research`) now gated behind `Depends(get_current_user)`
applied once at the composition root
(`app/presentation/api/routers/__init__.py`), not per-router-file --
`/health` and `/auth/login` stay public. Every login/token failure path
(unknown email, wrong password, malformed email, inactive user, expired
token, missing header) raises the byte-identical `UnauthorizedException`
message, verified with a dedicated test asserting the strings match --
an attacker probing the login form or a stolen token can't distinguish
"no such account" from "wrong password" one guess at a time.

Two real, previously-undocumented findings surfaced while building this
(both already existed, just never exercised by anything before now):
`app/presentation/api/middleware/exception.py`'s catch-and-format block
is commented out (dead code) -- unrelated `ApplicationException`
subclasses like the new `UnauthorizedException` are actually formatted by
a *different*, already-registered handler
(`application_exception_handler`), which is why 401s came out clean
without needing to fix that middleware; and `/admin/ai-config` (AI
provider config, including key fingerprints) was completely unauthenticated
before this change -- now gated like everything else.

**Frontend** (`src/app/auth/`): `AuthService` (signal-based, localStorage-
backed so a page refresh doesn't force a re-login), the first
`HttpInterceptorFn` in this codebase (attaches the bearer token, logs out
on a 401), the first route guard (`authGuard`, wraps every existing route
in one guarded parent instead of repeating `canActivate` per route), and
a `Login` screen. The sidebar shell (`app.html`) now only renders once
authenticated; logged out, only the `<router-outlet>` (i.e. the login
page) shows.

**Verified two ways, not just unit tests:** a full backend curl sequence
against the real running server (login success/failure with
byte-identical error bodies, `/auth/me` and a real protected route both
authed/unauthed, `/health` still public, `/admin/ai-config` now correctly
401ing where it used to leak); and a real headless-Chromium Playwright
session driving the actual dev server end-to-end -- logged-out redirect
to `/login`, wrong-credentials error banner, successful login landing on
Command Center with the real user's email in the sidebar, a real data
page (`/companies`, 8 real rows) loading through the interceptor, logout
clearing storage and redirecting, a direct post-logout URL visit
re-redirecting, an injected expired/garbage token correctly triggering
the interceptor's 401 handling, and a page refresh while logged in
preserving the session -- with screenshots taken at each step, not just
DOM-text assertions.

**Known minor gap, not fixed:** the sidebar's `.nav-footer` (now showing
email + "Log out" below "Admin") can sit right at or past the fold on a
short viewport (confirmed via the ~720px-tall Playwright default,
narrower than most real monitors) -- the element is still fully
functional (Playwright clicked it without needing to scroll), but a
`.sidebar { overflow-y: auto }` would make it robustly reachable on any
viewport height. A pre-existing sidebar-layout gap this change made
slightly more visible, not introduced by it; left for a future UI pass
rather than folded into this feature.

Backend test count: 532 passing (up from 519), including the first
full-`api_router`-mounted presentation test in this codebase (every prior
router test mounts an isolated single router, which never exercises
blanket `include_router(..., dependencies=[...])` gating). Frontend test
count: 105 passing (up from 93).

## Decisions

Both items below were tracked as open since EPIC-F00 and formally decided
2026-08-17, after EPIC-F00–F11 gave enough real evidence (12 modules, one
shared design system, two cross-entity join services) to decide from
rather than guess ahead of.

- **Styling approach: stay hand-rolled, no component library adopted.**
  Every screen shipped so far is plain `<table>`/`<select>`/`<input>`
  against the tokens in `design_system.md` (Navy/Blue/Cyan, Inter, the
  badge vocabulary) — nothing built has needed a date picker, autocomplete,
  drag-drop, or any interaction Angular Material/PrimeNG earn their keep
  on. Adopting either now would mean fighting their theming to match
  tokens already shipped consistently across 12 modules, or abandoning
  that work to accept their default look — real cost against a
  speculative benefit. **Revisit trigger:** a specific screen that
  genuinely needs rich interaction behavior HTML forms can't do well (a
  searchable combobox over 500+ companies, a Kanban-style pipeline view).
  If that happens: prefer **PrimeNG's unstyled/token preset** over
  Material — its CSS-custom-property theming cooperates with the tokens
  already in `styles.scss`, where Material's Sass-mixin theming fights
  overrides hard. For pure interaction primitives (focus trap, listbox
  keyboard nav, overlay positioning) without visual opinion, add
  **Angular CDK alone** (no `@angular/material` components) rather than a
  full library.
- **State management: no shared store adopted; keep evolving the signal +
  injectable-service pattern already in place.** Every screen is
  self-contained CRUD (load on `ngOnInit`, mutate, navigate away) — the
  only real friction found is `LeadDisplayService`/`AssessmentDisplayService`
  re-fetching and re-joining the same records on every screen visit, which
  is a caching gap, not a state-orchestration problem classic NgRx's
  actions/reducers/effects would actually solve. **Revisit trigger:**
  repeated fetches start costing something real (data volume grows, or a
  screen like Command Center wants live counts without a full reload).
  When that happens, the natural next step is giving the existing
  "Display service" pattern a signal-backed cache (`signal<Map<id,
  Entity>>`, invalidated after mutations) — not a new dependency, just
  evolving what `LeadDisplayService`/`AssessmentDisplayService` already
  are. If that ever needs more structure than a hand-rolled cache
  provides, **`@ngrx/signals` (SignalStore)** is the fallback, since it
  composes naturally with the signals every component already uses;
  classic NgRx remains a disproportionate leap for this app's shape.
