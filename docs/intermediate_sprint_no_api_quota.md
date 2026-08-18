# Intermediate Sprint — Zero API Quota Risk

Companion to `Backend/docs/product_backlog.md` + `pamacore_sprint_plan.md`
(the formal 17-sprint backend plan) and `Frontend/docs/frontend_backlog.md`
+ `frontend_sprint_plan.md` (the 12-sprint + PARK-F-AUTH frontend plan).
This is neither — it's a deliberately-inserted, cross-cutting sprint of
real, already-found work that needs **zero calls to Gemini or Tavily**,
so testing/verification can proceed freely without burning AI provider
quota (Gemini's free-tier daily budget is already exhausted/blocked per
`GEMINI_MODEL` returning 404) or Tavily usage.

**Rule for this sprint:** every item below must be buildable and
*live-verifiable* against the real running backend/frontend without
triggering `POST /company-research/search`, `POST /company-research/retry`,
or `POST /recommendations` (the only three endpoints that call an
external AI/search provider anywhere in this app). Everything else —
Company/Contact/Lead/Discovery/Assessment/Qualification CRUD, Auth,
Admin, cross-entity drill-down — is pure database/application code and
safe to exercise as much as needed.

---

## Progress notes

**IS-1 + IS-2, 2026-08-17, zero live API calls:**
- `app/presentation/api/middleware/exception.py` — restored the
  catch-and-format block (uncommented + given the app's real
  `{success, message, error_code, details}` shape with
  `error_code: "INTERNAL_ERROR"`, instead of the bare `{success, message}`
  that had been commented out). New test file
  `tests/presentation/api/middleware/test_exception_middleware.py`
  proves both directions: an unregistered exception now gets a clean 500
  (not a raw traceback), and a real `ApplicationException` (e.g.
  `NotFoundException`) still gets its own correct status code, not
  swallowed into a generic 500.
- `app/application/assessment/handlers/create_assessment_handler.py` —
  added the `get_by_discovery` pre-check + `IntegrityError` fallback,
  mirroring `CreateDiscoveryHandler`'s exact pattern; both raise
  `ConflictException` ("Assessment already exists for this discovery.").
  Also added `get_by_discovery` to the abstract `AssessmentRepository`
  contract (`app/application/contracts/repositories/assessment_repository.py`)
  — the concrete `SqlAlchemyAssessmentRepository` already implemented it,
  but it was missing from the interface. Two new tests in
  `tests/application/assessment/handlers/test_create_assessment_handler.py`
  cover the pre-check path and the race-condition `IntegrityError` path.
- **Live-verified against the real running backend** (the safe kind —
  plain CRUD, no AI/Tavily): `POST /assessments` against a discovery that
  already had one now returns a clean `409 {"error_code": "CONFLICT", ...}`
  instead of the old raw 500. Confirmed normal `200`s and existing
  `ApplicationException` status codes (e.g. a real `404`) are unaffected
  by the middleware change.
- Full backend suite: **539 passing** (up from 535 after the company-search
  fix, 532 before this session's work started), zero regressions.

**IS-3, 2026-08-18, zero live API calls:** added `response_model=` to all
four non-DELETE `qualification_router.py` endpoints
(`CreateQualificationResponseDTO`/`GetQualificationResponseDTO`/
`list[ListQualificationResponseDTO]`/`UpdateQualificationResponseDTO`) —
DELETE correctly gets none, matching every other module's 204-no-body
convention. Filled the previously-empty
`tests/presentation/api/test_qualification_api.py` stub with four real
tests proving each response actually validates against its declared
model (FastAPI enforces `response_model=` at runtime, so a handler/schema
mismatch would itself fail these), including an explicit assertion that
the list response's `recommendation` field is genuinely absent, not
`null`. **Immediate frontend payoff**: re-ran `npm run generate:api`
against the now-typed schema and swapped `qualification.models.ts` off
its hand-written interfaces onto real generated aliases
(`GetQualificationResponseDTO` for the single-record shape,
`ListQualificationResponseDTO` — now its own distinct
`QualificationListItemDTO` alias — for list rows, matching the real
narrower shape instead of overstating it). `QualificationService.list()`
and `QualificationList`'s row type updated to match. Backend suite: 543
passing (up from 539). Frontend suite: 105 passing, unchanged (a pure
type-source swap, no behavior change). **Live-verified against the real
backend**: full create/get/update/list/delete cycle for a real
Qualification, confirming FastAPI's `response_model=` validation doesn't
reject any real handler output, and that the list response's
`recommendation` omission is real (not a client-side assumption).

**IS-4, 2026-08-18, zero live API calls:** wired `POST
/recommendations/{id}/submit` and `POST /recommendations/{id}/approve`.
The handlers existed but were never reachable from any router, and their
original constructor shape (`repository, validator, mapper`, no real DI
factory) didn't match how any other handler in this codebase is wired —
rewrote both to the `unit_of_work` pattern `GetRecommendationHandler`
already uses, raising `NotFoundException`/`ConflictException` instead of
bare `ValueError`. Also deleted leftover debug code found in
`approve_recommendation_handler.py` (an `import inspect` plus five
`print()` calls dumping repository internals on every real call).

**A second, more consequential bug turned up during live verification,
not caught by the unit tests** (which mock the repository and can't see
this): `RecommendationModel` had no `status`/`submitted_at`/`approved_at`
columns at all, and `RecommendationMapper.to_domain` hardcoded every
loaded Recommendation back to `DRAFT` regardless of what had actually
happened to it — already flagged in the mapper's own docstring as a
"pre-existing gap," but nothing had exercised it end-to-end until now.
Submit/Approve genuinely transitioned the in-memory object and returned
the right status in that one response, but the change was silently lost
on the next load. Fixed by adding the three columns (new migration
`a3c5b2891152`, backfilling existing rows to `'Draft'` since none had
ever successfully transitioned), teaching the mapper to round-trip them,
and giving `SqlAlchemyRecommendationRepository` the same defensive
get-then-mutate `update()` override Company/Assessment/User already have
(it was relying on a blind `merge()` before). New test
`tests/infrastructure/persistence/repositories/recommendation/test_sqlalchemy_recommendation_repository.py`
proves the full Draft → Under Review → Approved cycle survives real
reloads. Backend suite: **555 passing** (up from 543). **Live-verified
against the real backend** using a real pre-existing Recommendation
(generated in an earlier sprint, before the Gemini blocker — zero new AI
calls needed): reproduced the bug first (submit "succeeded" but a fresh
`GET` still showed `Draft`), then confirmed the fix (submit → `GET`
correctly shows `Under Review` → approve → `GET` correctly shows
`Approved`, `approved_at` set, all 3 solutions still intact → re-approving
correctly 409s).

**IS-5, 2026-08-18, zero live API calls — scoped:** the real count of
empty test stub files across the backend is **71**, not the handful
`tests/domain/company/*`/`tests/domain/lead/*`/`tests/domain/qualification/*`
originally implied — most of the other ~57 are `application/*` handler
tests, `infrastructure/*` repository/mapper tests, `integrations/*`
(some of which are literally named `test_gemini_client.py`/
`test_gemini_pipeline.py`/`test_openai_pipeline.py` — **not** zero-quota-risk,
correctly excluded from this sprint on sight), and
`presentation/api/contact/*`. Filling all 71 would be its own multi-day
effort, not a same-sprint item — **scoped to exactly the domain-layer
stubs named in the original plan**: Company (entity, both events,
identifier), Lead (entity), Qualification (entity, score value object),
and Recommendation (entity — a natural sibling given IS-4's work in that
exact module, plus its two events since fixing them was necessary to test
them at all). Of the 14 files in that domain-layer set, 5 targeted
scaffolding for code that was never built (`CompanyFactory`, `LeadFactory`,
a `CompanyName`/`CompanyWebsite` value object, a `company_intelligence`
module) — left empty rather than inventing behavior for classes that
don't exist. The remaining ~57 stubs (`application/*`, `infrastructure/*`,
non-AI `integrations/*`, `presentation/api/contact/*`) are flagged as a
**separate, larger future item**, not silently absorbed into IS-5.

Writing these tests surfaced three more real, previously-undiscovered
bugs, none requiring any AI/Tavily call to find or fix:
- **`DomainEvent`'s custom `__init__` never ran for any of its 19
  `@dataclass` subclasses across the whole codebase** — a subclass
  dataclass's generated `__init__` doesn't call a non-dataclass base
  class's hand-written `__init__`, so `event.event_id`/`.occurred_at`
  raised `AttributeError` on every single domain event in this app.
  Never surfaced because nothing actually raises/dispatches these events
  yet (a dormant subsystem). Fixed by converting `DomainEvent` itself
  into a frozen dataclass with `init=False` default-factory fields, which
  composes correctly with dataclass inheritance — verified against all 8
  event classes in Company/Lead/Recommendation directly (the other 11 in
  AI/Assessment/Report/Workflow weren't individually re-verified but
  share the identical mechanism).
- **`recommendation_created.py` and `recommendation_submitted_for_review.py`
  both imported `RecommendationId` from a module that doesn't exist**
  (`..value_objects.recommendation_id` instead of the real
  `..identifiers.recommendation_id`) — a `ModuleNotFoundError` that made
  the entire `app.domain.recommendation.events` package fail to import.
  Fixed both import paths; `recommendation_approved.py` already had the
  correct one, confirming this was a copy-paste typo, not a real path
  change.
- **`Lead.update_notes()` didn't match its own constructor's whitespace
  normalization** — `notes.strip() if notes else None` only checked
  truthiness *before* stripping, so a whitespace-only string like `"   "`
  (truthy) stripped down to `""` and stuck, instead of clearing to `None`
  the way `Lead.__post_init__` already does for the exact same input at
  construction time. Fixed to re-check after stripping, matching
  construction-time behavior.

Backend suite: **614 passing** (up from 555) — 59 new tests, zero
regressions, zero Gemini/Tavily calls anywhere in this item.

**IS-6, 2026-08-18, zero live API calls:** gave `LeadDisplayService` and
`AssessmentDisplayService` a private `cache: Observable<Map<...>> | null`
field, lazily populated by `loadAll()` and cleared by a new public
`invalidate()`. Callers that mutate a record the cache could go stale
for now call `invalidate()` in their success callbacks: `LeadForm.save()`,
`LeadDetail.delete()`, `AssessmentForm.save()`, and both
`AssessmentDetail.start()`/`.delete()`. `resolve()` (used by detail/edit
screens) stays deliberately uncached — those screens must always show
the current state of the one record they're editing, not a stale bulk
join. First implementation used `share({ resetOnRefCountZero: false, ... })`,
which failed 2 new tests: `share()` only multicasts to subscribers active
*during* the original emission, it doesn't replay past values to a late
subscriber. Switched to `shareReplay({ bufferSize: 1, refCount: false })`
plus an explicit `catchError` that nulls the cache and re-throws (since
`shareReplay` has no `resetOnError` equivalent and would otherwise replay
a cached failure forever). 4 new tests added (2 per service): cache reuse
across a second `loadAll()` call (no duplicate HTTP requests), and
`invalidate()` forcing a genuine re-fetch with updated data. Frontend
suite: **109 passing** (up from 105). Build clean.

**IS-7, 2026-08-18, zero live API calls:** `.sidebar` was missing an
`overflow-y: auto` its sibling `.workspace` already had, and `.shell`
used `min-height: 100vh` rather than a bounded `height: 100vh` — so even
adding `overflow-y: auto` to `.sidebar` alone would have had no fixed
height to scroll within (the flex container would just keep growing).
The auth sprint's new `.nav-user`/`.nav-footer` block was what first made
sidebar content tall enough for this to matter on short viewports.
Fixed both in `Frontend/src/app/app.scss`: `.shell` now uses
`height: 100vh` (matching `.workspace`'s existing independent-scroll
design, which this bounded height silently made possible from the
start), and `.sidebar` now has its own `overflow-y: auto` to match.
`.workspace`'s existing scroll behavior is untouched. Build clean,
frontend suite still 109 passing (pure CSS, no test changes needed).

**IS-8, 2026-08-18, zero live API calls:** wired real Submit/Approve
actions into `RecommendationDetail`, closing the last gap IS-4 opened up
on the backend. Added `submit()`/`approve()` to `RecommendationService`
(`POST /recommendations/{id}/submit` / `/approve`); the component gained
`submitting`/`approving` signals and matching handlers that update the
local `recommendation` signal from the response on success (no separate
`invalidate()`+refetch needed the way list-caching screens do, since
there's exactly one record on this screen — `RecommendationDisplayService`
doesn't exist and wasn't needed). Template shows a "Submit for Review"
button only when `status === 'Draft'` and an "Approve" button only when
`status === 'Under Review'`, matching the real domain transition guard in
`Recommendation.approve()` (`ValueError` if not already Under Review).
Refreshed the stale doc comments in `recommendation.service.ts` and
`recommendation.models.ts` that still described Submit/Approve as
unreachable from the API (true before IS-4, false now). No new spec file:
confirmed via `Frontend/src/app/**/*-detail/*.spec.ts` that **no**
`*-detail` component in this codebase has ever had a dedicated spec (only
list/form/service specs do) — matched that existing convention rather
than inventing a new one for just this component. Build clean, frontend
suite unchanged at 109 passing. **Live-verified against the real
backend**: since the one real Recommendation fixture
(`78de26ee-c277-4241-9ef3-6558b5e5e5d3`) was already `Approved` from
IS-4's earlier verification, and a fresh one can't be created without
spending a real AI call (`generate()` hits Gemini), temporarily reset its
`status`/`submitted_at`/`approved_at` directly in `aisdr.db` to `Draft`,
then drove it back through the real `submit`→`approve` HTTP calls
(the exact request shape the new UI sends: `POST .../submit` and
`POST .../approve`, empty JSON body) — confirmed `Draft` → `Under Review`
→ `Approved` end-to-end, landing the fixture back in its original
`Approved` state, so nothing about the shared dev DB changed net of this
verification. (Also noticed live: every non-`/auth` endpoint now requires
a bearer token — the parked JWT auth work from `PARK-F-AUTH` has since
been completed and is live on this backend. Created a standing local
verification user, `verify@aisdr.local`, via `scripts/create_user.py`
for this and future live-curl checks, since no test credentials existed
yet in this environment.)

**IS-9, 2026-08-18, audit only, zero live API calls:** read every
`GET` list/search endpoint across all 7 CRUD routers directly (not the
generated OpenAPI schema, which doesn't distinguish `skip`/`limit` from
`page`/`page_size` well enough to audit this by itself). Findings:

*Pagination style — two conventions, split roughly 5/2:*
| Style | Routers |
|---|---|
| `skip` / `limit` | Company, Contact, Lead, Discovery, Qualification |
| `page` / `page_size` | Assessment, Recommendation |

*Free-text search param name — three different names for the same concept, across the 3 routers that have a `/search` endpoint at all:*
| Router | Param name |
|---|---|
| Company (`GET /companies/search`) | `query` |
| Contact (`GET /contacts/search`) | `search_text` |
| Discovery (`GET /discoveries/search`) | `search_text` |
| Lead (`GET /leads/search`) | `keyword` |

(Assessment, Qualification, Recommendation have no `/search` endpoint —
only list-with-filters.)

**Decision: documented, not normalized.** Renaming these is a genuine
breaking API-contract change (every query param above is a real, already
frontend-consumed part of the request shape — `CompanyService`,
`ContactService`, `LeadService`, `DiscoveryService`, `QualificationService`,
`AssessmentService`, `RecommendationService` would *all* need matching
edits, not just the 7 backend routers), for a purely cosmetic
consistency win with no behavior change and no bug attached. That's a
bigger, riskier item than "optional stretch, pull in only if there's
room to spare" scope warrants — recorded here as a real, verified
finding (not a guess) so a future dedicated item can normalize with full
context instead of re-discovering this from scratch. No code changed for
this item; backend/frontend suites unaffected.

**IS-10, 2026-08-18, zero live API calls:** neither `Backend/` nor
`Frontend/` had any lint, formatter, or CI configuration before this —
verified directly (no `pyproject.toml`, no `eslint.config.js`, no
`.github/workflows/`).

*Backend:* added `ruff` (lint + format in one tool) via a new
`Backend/pyproject.toml` + `requirements-dev.txt`. First full run found
630 issues; after tuning the config for this codebase specifically
(line-length 110; `B008` ignored — FastAPI's own `= Depends(...)` default-arg
idiom, not the mutable-default-arg bug that rule targets; `B024` ignored —
`DomainEvent`/`ValueObject`/`Identifier` are deliberate abstract marker
classes with no methods of their own; `UP042/043/046/047` ignored — PEP 695
generic-syntax/StrEnum rewrites are real modernizations but touch class
declarations broadly, left as a deliberate separate future pass; migrations'
`env.py` gets a per-file `F401` exemption since it imports every model
purely so Alembic's autogenerate can see them registered, never referencing
the names directly) — real, scoped findings dropped to 322. Auto-fixed the
217 mechanical ones (import sorting, `Optional[X]` → `X | None`, deprecated
typing imports) and ran `ruff format` across the whole backend (a one-time
618-file reformat, since no formatter had ever been run before — purely
whitespace/quote-style, verified via a full `pytest -q` pass after: still
**614 passing**, zero regressions). The remaining 8 are all long string
literals (a regex pattern, test fixture content, an f-string) that a
formatter legitimately can't wrap without changing the string's content —
left as accepted style debt, not worth hand-mangling.

Fixed the handful of findings that were genuine, not style noise:
- **`discovery_model.py`'s `AssessmentModel` forward-reference was a real
  `F821` (undefined name)** — every sibling model file (`lead_model.py`,
  `company_model.py`) already imports its forward-referenced sibling under
  `TYPE_CHECKING`; this one file had just been missed. Added the same
  `if TYPE_CHECKING: from ...assessment_model import AssessmentModel`.
  Harmless at runtime either way (SQLAlchemy resolves the string literal
  in `relationship("AssessmentModel", ...)` via its own registry, not the
  type annotation) but now type-checks cleanly too.
- **A dead `from pydantic import validator` sat unused in
  `presentation/api/dependencies/handlers.py`** (Pydantic v1 API, this
  codebase is on v2) — shadowed by every local `validator: XValidator =
  Depends(...)` parameter in the file, confirmed genuinely never
  referenced for its own purpose. Removed.
- **5 more genuinely-dead imports**: `qualification_router.py` imported
  all 5 raw `*Handler` classes it never uses (the router only uses the
  `*HandlerDependency` aliases from `dependencies/handlers.py`);
  `assessment_router.py` imported `CreateAssessmentCommand` unused for the
  same reason; `persistence.py` imported `Annotated` unused;
  `test_assessment_mapper.py` and `test_lead_entity.py` (the latter one of
  this session's own IS-5 additions) each had one unused test-fixture
  import. All confirmed via grep before removal, not assumed.
- **3 test files used `assert False`/blind `pytest.raises(Exception)`
  instead of the specific exception** (`B011`/`B017`) — rewrote to
  `pytest.raises(TypeError)` / `pytest.raises(AttributeError)` matching
  what's actually raised (a `dict`'s `TypeError` on a MappingProxy-style
  immutable details dict; a frozen dataclass's `FrozenInstanceError`,
  itself an `AttributeError` subclass), which is both more correct and
  more idiomatic than the try/except-with-assert pattern they replaced.

*Frontend:* added ESLint via `ng add @angular-eslint/schematics` (the
project's own peer-dependency graph has a pre-existing, unrelated
`typescript@~6.0.2` vs. `openapi-typescript`'s declared `^5.x` peer range
conflict — already latent in the lockfile, only surfaced when installing a
*new* package — so added `Frontend/.npmrc` with `legacy-peer-deps=true` to
unblock it; this doesn't change what's already resolved, just relaxes
strictness for future installs). First lint run surfaced 96 problems, 86 of
which were `@typescript-eslint/consistent-indexed-object-style` findings
against `src/app/api/schema.d.ts` — a generated file (`npm run
generate:api`), never hand-edited — so excluded it via `eslint.config.js`
`ignores`, matching how the file is already treated everywhere else in this
project (Prettier-ignored too, see below). That left 10 real findings:
- **6 identical instances of a `<label>` with no `for` attribute wrapping
  a static, read-only display value** (Company/Lead/Discovery/Assessment
  "static-value" fields in edit-mode forms — e.g. `contact-form.html`,
  `lead-form.html`, `discovery-form.html`, `qualification-form.html` ×2,
  `assessment-form.html`) — a real accessibility gap (`<label>` must be
  associated with a form control; these label a plain `<p>`, not one).
  Fixed by swapping the element to `<span class="field-label">` (the
  correct semantic choice for a static caption) and adding a matching
  `.form .field-label` rule alongside the existing `.form label` rule in
  the global `styles.scss` so the visual style is unchanged.
- **2 no-op mock callbacks in spec files** (`vi.spyOn(...).mockImplementation(()
  => {})`, `.subscribe({ error: () => {} })`) — legitimate, common test
  patterns, not "forgot to implement this" bugs. Disabled
  `@typescript-eslint/no-empty-function` for `**/*.spec.ts` files globally
  rather than patch each occurrence, since this pattern will keep recurring
  as more mocks get added.
- **1 unused import** (`auth.guard.spec.ts` imported `AuthService` and
  never used it) — removed.
- **1 "unused" destructured binding that's actually the idiomatic "extract
  to exclude from a rest spread" pattern** (`contact-form.ts`'s `const {
  company_id, ...updatable } = this.form()` deliberately drops
  `company_id` from the update payload, since company reassignment isn't
  exposed via contact edit — matches the read-only "Company" field in the
  same form). Enabled the built-in `ignoreRestSiblings` option for
  `@typescript-eslint/no-unused-vars` project-wide rather than rename the
  binding to `_company_id`, since this idiom is likely to recur.

Configured the `.prettierrc` that already existed (from the original
Angular CLI scaffold, unused until now) with a `.prettierignore` excluding
the generated schema file, and added `format`/`format:check` npm scripts
(`ng add` had already wired a `lint` script). First `format:check` found
47 never-formatted files; ran `format --write` once (the frontend
equivalent of the backend's one-time reformat) — verified after with a
full `ng build` + `ng test --watch=false`: build clean, **109 passing**,
unchanged.

*CI:* added `.github/workflows/backend-ci.yml` (Python 3.13, `ruff check`
+ `ruff format --check` + `pytest -q`) and `frontend-ci.yml` (Node 22,
`ng lint` + `format:check` + `ng build` + `ng test --watch=false`), each
path-scoped to its own directory so an unrelated change doesn't trigger
the other stack's pipeline. **Not just written and assumed correct**: every
step of both workflows was run locally in a CI-equivalent way before
considering this done, including deliberately hiding the local `.env` file
during the backend run to confirm none of the `Settings` classes require
one (`DatabaseSettings.database_url` and every other setting already has a
working default per this codebase's existing "importable/testable without
credentials" convention) — `ruff check .`, `ruff format --check .`, and
`pytest -q` all pass identically with zero `.env`; `npm ci` (not `npm
install`, matching exactly what the workflow runs) resolves cleanly given
the new `.npmrc`. Neither workflow has actually run on GitHub Actions
itself yet (nothing has been pushed) — that's the one part of "live
verification" this item can't reach without a real push, but every command
inside both workflows has been proven to succeed on this machine first.

This item's diff is large in file count (618 backend + 47 frontend files
touched by the one-time formatter passes) but is entirely mechanical
whitespace/import-order/quote-style change plus the small set of genuine
fixes listed above — both full test suites pass unchanged (**614** backend,
**109** frontend) and both full builds are clean.

**IS-11, 2026-08-18, zero live API calls:** the dev DB before this item
had only 8 companies / 3 leads / 3 discoveries / 2 assessments / **0**
qualifications / 1 recommendation — whatever had accumulated one record
at a time while testing individual features, no variety of pipeline
stage or status. Added `Backend/scripts/seed_demo_data.py`, following
`create_user.py`'s exact pattern (construct domain entities directly,
persist via `UnitOfWork`/repositories, no HTTP, no AI/search calls).

Before writing it, read every entity's real constructor directly (not
guessed) — `Company`, `Contact`, `Lead`, `Discovery`, `Assessment`,
`Qualification`, `Recommendation`/`Solution`/`RoadmapPhase` — to avoid
repeating this session's earlier `RoadmapPhase` field-name mistake. That
read surfaced two genuine, already-known persistence gaps worth calling
out explicitly rather than silently seeding around: **Assessment's
per-dimension score breakdown and its `Finding`/`Evidence`/`Opportunity`
entities have no backing columns at all** (`assessment_mapper.py`'s
`to_model` never references them), and **`Recommendation.roadmap_phases`
has no backing column either** (already flagged in that mapper's own
docstring from IS-4). Anything set on those fields is silently dropped on
save — so the seed script deliberately does *not* populate them, to avoid
producing demo data that looks richer in this script than it would ever
actually appear in the running app.

Seeded 5 complete chains, each deliberately stopped at a *different*
pipeline stage so every list/detail screen and status badge has real
data to show, and so the two most interesting Recommendation states are
live and clickable rather than needing a real AI-generated one:
- **Meridian Logistics Group** — full chain, Recommendation in **Draft**
  with 2 solutions (a "Submit for Review" button is live on this one).
- **Brightline Financial Services** — full chain, Recommendation already
  moved to **Under Review** via the real `recommendation.submit_for_review()`
  domain method (not a script-only shortcut — the same invariant
  `SubmitRecommendationHandler` enforces) — an "Approve" button is live
  on this one.
- **Coastal Retail Group** — stops at Qualification (`Needs Nurturing`,
  score 38) — no Recommendation yet, a realistic "not a good fit right
  now" outcome.
- **Fenwick Manufacturing Co.** — stops mid-Discovery (`IN_PROGRESS`) —
  no Assessment started yet.
- **Northgate Consulting Partners** — a bare new Lead, nothing else —
  freshest possible top-of-funnel record.

Idempotent per company: each seeder checks `CompanyRepository.find_by_name`
first and skips its entire chain if that company already exists, so
re-running the script is always safe — verified by running it twice in a
row (`Seeded: ...` ×5, then `Already exists, skipped: ...` ×5 with no row
count change). **Live-verified against the real running backend** (not
just raw SQLite): logged in as the standing verification user, listed
`/companies` (all 5 present), `/recommendations` (confirmed Meridian
shows `Draft` with 2 solutions, Brightline shows `Under Review` with 1
solution — matching the design exactly), `/qualifications` (`Needs
Nurturing`/`Qualified`/`Qualified` — the real variety), and `/discoveries`
(`IN_PROGRESS`/`COMPLETED`/`CREATED` mixed). Deliberately did **not**
drive Meridian/Brightline through Submit/Approve via curl here, since
that would consume the exact live-clickable demo states the script was
built to leave available for hands-on verification in the browser.
Backend suite: still **614 passing**, zero regressions; `ruff check`/
`ruff format --check` clean on the new file.

---

## Definition of Done (same discipline as both existing plans)

- Component builds and the full test suite passes (backend `pytest -q`,
  frontend `ng test`)
- Live-verified against the real running backend/frontend where
  applicable — but only via the safe endpoints above
- Nothing committed until explicitly requested

---

## Scope

| Status | ID | Area | Item | Size | Why it's zero-quota-risk |
|---|---|---|---|---|---|
| `[x]` Done | IS-1 | Backend | Fix `ExceptionMiddleware`'s dead catch-and-format block (currently commented out) so non-`ApplicationException` failures (e.g. `IntegrityError`, `AIProviderException`) return a clean structured error instead of a raw 500 | S | Pure exception-handling code; testable by triggering the *already-known* duplicate-Assessment 500 (a DB constraint violation), not by calling AI |
| `[x]` Done | IS-2 | Backend | Give Assessment a clean 409 on a duplicate `discovery_id` (pre-check-then-raise, mirroring Discovery's own one-per-Lead check) instead of letting the unique constraint throw | S | Same DB-constraint scenario as IS-1, no AI involved |
| `[x]` Done | IS-3 | Backend | Add `response_model=` to every `qualification_router.py` endpoint (currently the only router missing it, which is why the generated OpenAPI schema types its responses as `unknown` and the frontend had to hand-write `QualificationResponseDTO`) | S | Pure FastAPI/Pydantic typing change; verified via `GET /openapi.json` + `npm run generate:api`, no AI call |
| `[x]` Done | IS-4 | Backend | Wire Recommendation's existing, tested Submit/Approve handlers into `recommendation_router.py` (real application-layer code today, unreachable from any endpoint) | M | Submit/Approve only move a status field — no AI generation involved, unlike Create/"Generate" |
| `[x]` Done (scoped) | IS-5 | Backend | Fill in the empty backend test stub files (`tests/domain/company/*`, `tests/domain/lead/*`, `tests/domain/qualification/test_qualification.py`, and siblings — currently placeholder files with no content) | M | Pure unit tests against domain entities/value objects, no I/O at all |
| `[x]` Done | IS-6 | Frontend | Give `LeadDisplayService`/`AssessmentDisplayService` a signal-backed cache instead of re-fetching and re-joining the same records on every screen visit — the concrete "revisit trigger" already recorded against the state-management decision in `frontend_backlog.md` | M | Touches only Company/Contact/Lead/Discovery/Assessment CRUD endpoints |
| `[x]` Done | IS-7 | Frontend | Sidebar `.nav-footer` overflow fix (`overflow-y: auto` on `.sidebar`) — the minor gap noted after the auth sprint | XS | Pure CSS |
| `[x]` Done | IS-8 | Frontend | Recommendation detail screen gains real Submit/Approve actions | S | Depends on IS-4; still no AI call — these two actions don't generate anything |
| `[x]` Done (audit only) | IS-9 | Backend | Audit + document (or normalize) the per-router pagination/search param inconsistency (`skip`/`limit` vs `page`/`page_size`; `query`/`search_text`/`keyword` as three different search-param names) — flagged repeatedly across the frontend sprint history as a recurring "check each one, don't assume" friction point | M–L | Pure routing/query-param code across existing CRUD routers |
| `[x]` Done | IS-10 | Dev experience | CI + lint/pre-commit setup for both `Backend/` and `Frontend/` (neither has one today) | M | Tooling only |
| `[x]` Done | IS-11 | Dev experience | Richer seed-data script (extends `Backend/scripts/create_user.py`'s pattern) so demo/dev data doesn't require a live Tavily/Gemini research run to populate | S–M | Seeds directly via repositories, same as `create_user.py` already does |

**Total core scope (IS-1 through IS-8):** small-to-medium, roughly a
half-to-one normal backend sprint's worth of points, all independently
shippable and independently live-verifiable. IS-9/IS-10/IS-11 were marked
optional/stretch, pulled in only once the core list finished with room to
spare — all three are now also done (IS-9 as a documented audit rather
than a normalization, per its own "audit + document (or normalize)"
framing). **All 11 items in this sprint are complete.**

---

## Sequencing rationale

1. **IS-1 → IS-2** first: the exception-handling fix is the prerequisite that makes IS-2 (and any future "raise a clean error instead of a raw 500" fix) actually produce a clean response — do the general fix before the specific one.
2. **IS-3** next: independent, small, and unblocks a real frontend follow-up (dropping the hand-written Qualification DTO workaround) the moment it ships.
3. **IS-4 → IS-8**: wire the backend capability first, then the frontend screen that uses it — same order every prior module in this project followed.
4. **IS-5** (test stubs) can run in parallel with any of the above — it touches only test files, zero risk of colliding with the other backend changes.
5. **IS-6 → IS-7**: independent frontend items; no ordering dependency between them.
6. **IS-9/IS-10/IS-11**: explicitly last, explicitly optional — larger or lower-value-per-effort than the core list.

## Explicitly out of scope for this sprint

- Anything touching `company_research` (search/retry) or Recommendation
  "Generate" — the only three AI/Tavily-calling endpoints in the app.
- EPIC-16 (Human-in-the-loop review queue) and EPIC-11 (Deliverability &
  compliance) — both are genuinely AI/quota-safe in principle, but too
  large for an "intermediate" sprint; candidates for a dedicated future
  sprint of their own, not squeezed in here.
- `PARK-F-ACT`/`PARK-F-SEARCH` — still blocked on backend capability that
  doesn't exist yet; unrelated to the quota concern.
