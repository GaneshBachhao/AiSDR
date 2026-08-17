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
| `[ ]` Planned | IS-1 | Backend | Fix `ExceptionMiddleware`'s dead catch-and-format block (currently commented out) so non-`ApplicationException` failures (e.g. `IntegrityError`, `AIProviderException`) return a clean structured error instead of a raw 500 | S | Pure exception-handling code; testable by triggering the *already-known* duplicate-Assessment 500 (a DB constraint violation), not by calling AI |
| `[ ]` Planned | IS-2 | Backend | Give Assessment a clean 409 on a duplicate `discovery_id` (pre-check-then-raise, mirroring Discovery's own one-per-Lead check) instead of letting the unique constraint throw | S | Same DB-constraint scenario as IS-1, no AI involved |
| `[ ]` Planned | IS-3 | Backend | Add `response_model=` to every `qualification_router.py` endpoint (currently the only router missing it, which is why the generated OpenAPI schema types its responses as `unknown` and the frontend had to hand-write `QualificationResponseDTO`) | S | Pure FastAPI/Pydantic typing change; verified via `GET /openapi.json` + `npm run generate:api`, no AI call |
| `[ ]` Planned | IS-4 | Backend | Wire Recommendation's existing, tested Submit/Approve handlers into `recommendation_router.py` (real application-layer code today, unreachable from any endpoint) | M | Submit/Approve only move a status field — no AI generation involved, unlike Create/"Generate" |
| `[ ]` Planned | IS-5 | Backend | Fill in the empty backend test stub files (`tests/domain/company/*`, `tests/domain/lead/*`, `tests/domain/qualification/test_qualification.py`, and siblings — currently placeholder files with no content) | M | Pure unit tests against domain entities/value objects, no I/O at all |
| `[ ]` Planned | IS-6 | Frontend | Give `LeadDisplayService`/`AssessmentDisplayService` a signal-backed cache instead of re-fetching and re-joining the same records on every screen visit — the concrete "revisit trigger" already recorded against the state-management decision in `frontend_backlog.md` | M | Touches only Company/Contact/Lead/Discovery/Assessment CRUD endpoints |
| `[ ]` Planned | IS-7 | Frontend | Sidebar `.nav-footer` overflow fix (`overflow-y: auto` on `.sidebar`) — the minor gap noted after the auth sprint | XS | Pure CSS |
| `[ ]` Planned | IS-8 | Frontend | Recommendation detail screen gains real Submit/Approve actions | S | Depends on IS-4; still no AI call — these two actions don't generate anything |
| `[ ]` Optional | IS-9 | Backend | Audit + document (or normalize) the per-router pagination/search param inconsistency (`skip`/`limit` vs `page`/`page_size`; `query`/`search_text`/`keyword` as three different search-param names) — flagged repeatedly across the frontend sprint history as a recurring "check each one, don't assume" friction point | M–L | Pure routing/query-param code across existing CRUD routers |
| `[ ]` Optional | IS-10 | Dev experience | CI + lint/pre-commit setup for both `Backend/` and `Frontend/` (neither has one today) | M | Tooling only |
| `[ ]` Optional | IS-11 | Dev experience | Richer seed-data script (extends `Backend/scripts/create_user.py`'s pattern) so demo/dev data doesn't require a live Tavily/Gemini research run to populate | S–M | Seeds directly via repositories, same as `create_user.py` already does |

**Total core scope (IS-1 through IS-8):** small-to-medium, roughly a
half-to-one normal backend sprint's worth of points, all independently
shippable and independently live-verifiable. IS-9/IS-10/IS-11 are marked
optional/stretch — pull in only if the core list finishes with room to
spare.

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
