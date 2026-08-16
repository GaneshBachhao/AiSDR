# AiSDR Frontend

Angular frontend for the [Backend](../Backend) (Pamacore / opportunity
discovery platform). Standalone components, signals, no NgModules — Angular
22 defaults. Lives in the same repo as the backend
(`AiSDR/Backend` + `AiSDR/Frontend`, one git history), but is currently
**exploratory/untracked** in project planning terms — not part of the
backend's formal `Backend/docs/product_backlog.md` sprint plan.

Frontend has its own roadmap instead: [`docs/frontend_backlog.md`](docs/frontend_backlog.md)
(epics/scope) and [`docs/frontend_sprint_plan.md`](docs/frontend_sprint_plan.md)
(sequencing). Kept separate on purpose — see either doc's header for why.

## First vertical slice: company_research search + retry

The only screen today is `src/app/company-research` — a search form against
`POST /company-research/search` plus a results table and a separate
failures table with a retry action against `POST /company-research/retry`.
Chosen as the first slice because it's the backend's most complete,
most live-verified flow (Sprints 4-10), and its `{results, failures}`
response shape (added in Sprint 10) maps naturally onto real UI states —
a qualified-result row vs. a crashed-but-retryable row.

## Running locally

Two servers, both need to be up:

```bash
# Terminal 1 — backend, from AiSDR/Backend
uvicorn main:app --reload

# Terminal 2 — frontend, from AiSDR/Frontend
npm start   # ng serve, http://localhost:4200
```

`src/environments/environment.ts` points at `http://127.0.0.1:8000` (the
backend's default `uvicorn` bind address). The backend already has
permissive CORS (`allow_origins=["*"]` in
`app/presentation/configuration/cors.py`) so no backend change was needed
for local dev — tighten this before any real deployment.

## API types

`src/app/api/schema.d.ts` is generated from the backend's live
`/openapi.json` via `openapi-typescript` (see `docs/frontend_backlog.md`
EPIC-F02 for why that tool over a full Angular service generator).
Regenerate after any backend DTO/route change:

```bash
npm run generate:api   # requires the backend running on 127.0.0.1:8000
```

Module DTOs (`company-research.models.ts` and future modules) are type
aliases onto `components['schemas'][...]` from that generated file, not
hand-written interfaces — drift is caught by TypeScript at build time, not
missed silently.

## Deliberate simplifications (not final decisions)

- **Template-driven forms** (`FormsModule` + `ngModel`), not reactive forms
  — fine for one form with a handful of fields; revisit if forms grow
  complex validation needs.
- **No auth** — the backend has none either yet. Don't build a login screen
  before the backend has something to log into.

## Testing

```bash
npm test   # Vitest, Angular 22's default test runner (not Karma)
```
