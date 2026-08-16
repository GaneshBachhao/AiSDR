# AiSDR Frontend — Design System & Information Architecture

Companion to [`frontend_backlog.md`](frontend_backlog.md) and
[`frontend_sprint_plan.md`](frontend_sprint_plan.md). This is the design
reference the rest of the frontend builds against — component patterns,
tokens, and the corrected information architecture. Written 2026-08-16,
superseding EPIC-F01's original horizontal-nav shell (see that epic's
history in `frontend_backlog.md` for why).

---

## 1. Product framing

**AiSDR — AI Sales Intelligence.** Not a CRUD admin panel with an AI
feature bolted on — a system that carries a company from "discovered" to
"acted on," where every AI-generated claim traces back to evidence in the
underlying data.

## 2. Information architecture

The nav is organized around the pipeline, not a flat module list — but the
pipeline order below is the **real** one, verified against the backend's
actual aggregate dependencies (not assumed from the domain names alone):

```
Company → Contact → Lead → Discovery (needs) → Assessment → Qualification → Recommendation → (Act)
```

Verified 2026-08-16 by reading the domain code directly:
`Qualification.__init__` requires an `assessment_id` — a Qualification
literally cannot be created before its Assessment exists. So **Qualify
comes after Assess**, not before Discover Needs/Assess as a naive reading
of the stage names might suggest.

```
AiSDR
│
├── Command Center                 (landing page)
│
├── DISCOVER
│   ├── Company Research           (company_research_router — find candidates)
│   ├── Companies                  (company_router)
│   ├── Contacts                   (contact_router)
│   └── Leads                      (lead_router)
│
├── DISCOVER NEEDS
│   └── Discoveries                (discovery_router — problem/impact/success criteria per Lead)
│
├── ASSESS
│   └── Assessments                (assessment_router — maturity/readiness/strengths/weaknesses)
│
├── QUALIFY
│   └── Qualifications             (qualification_router — status/score/recommendation per Assessment)
│
├── RECOMMEND
│   └── Recommendations            (recommendation_router — AI-generated solutions, read-mostly)
│
├── ACT                            (no backend yet — see §7)
│   └── Actions
│
└── ADMIN
    └── Diagnostics                (admin_router)
```

Note there is **no separate "Research" top-level group** — company_research
lives under DISCOVER, since its job is finding and pre-qualifying
candidates before they become a Company record, not a distinct pipeline
stage from Discover.

### Two different "qualification" concepts — don't conflate them

- **Research-time fit score** — `CompanySearchResult.qualification_score`,
  computed instantly during `POST /company-research/search`, before
  anything is persisted. This is a research signal.
- **CRM Qualification aggregate** — a separate persisted record
  (`qualification_router`), created only after a Lead has gone through
  Discovery and Assessment. This is a decision, not a signal.
  Today's real DTO is intentionally simple:
  `{ status, score (0-100), recommendation (text) }` — no multi-dimension
  breakdown. Build the Qualification screen against this shape now (see
  `frontend_backlog.md` EPIC-F09); a richer dimensioned score is a
  possible *backend* feature request, not a frontend styling choice.

## 3. Shell layout

```
┌──────────────────────────────────────────────────────────────────┐
│ AiSDR                              Search…              🔔  User ▾│
├───────────────┬──────────────────────────────────────────────────┤
│ AiSDR         │                                                  │
│ AI Sales      │                                                  │
│ Intelligence  │                                                  │
│               │                                                  │
│ ⌂ Command     │                   WORKSPACE                      │
│   Center      │                                                  │
│               │                                                  │
│ DISCOVER      │                                                  │
│  Company      │                                                  │
│  Research     │                                                  │
│  Companies    │                                                  │
│  Contacts     │                                                  │
│  Leads        │                                                  │
│               │                                                  │
│ DISCOVER NEEDS│                                                  │
│  Discoveries  │                                                  │
│               │                                                  │
│ ASSESS        │                                                  │
│  Assessments  │                                                  │
│               │                                                  │
│ QUALIFY       │                                                  │
│  Qualifications│                                                 │
│               │                                                  │
│ RECOMMEND     │                                                  │
│  Recommend-   │                                                  │
│  ations       │                                                  │
│               │                                                  │
│ ACT           │                                                  │
│  Actions      │                                                  │
│ ────────────  │                                                  │
│ Admin         │                                                  │
└───────────────┴──────────────────────────────────────────────────┘
```

- Sidebar: 248px expanded. Collapse to ~64px is a later refinement, not
  in scope for the first shell pass.
- Active route: light blue background, blue left border (`border-left:
  3px solid var(--accent)`), no filled block — mirrors the corrected
  design over the plain filled-orange treatment EPIC-F01 shipped.

## 4. Design tokens

Light-first — this is a data-dense B2B tool used for hours at a stretch,
not a demo surface. Implemented as CSS custom properties on `:root` in
`src/styles.scss` so every component reads the same source of truth.

```css
--color-bg: #f8fafc;          /* app background, Slate 50 */
--color-surface: #ffffff;     /* cards, panels */
--color-ink: #0f172a;         /* primary text, Deep Navy */
--color-ink-soft: #64748b;    /* secondary text */
--color-border: #e2e8f0;

--color-accent: #2563eb;      /* Electric Blue — primary actions, active nav */
--color-ai: #0891b2;          /* Cyan-leaning teal — AI-generated content marker */

--color-success: #16a34a;
--color-warning: #d97706;
--color-danger: #dc2626;

--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--radius: 10px;
```

Type weights: 400 body, 500 labels, 600 headings, 700 for large numeric
KPIs. No custom heading font — Inter everywhere, per the proposal's own
"implementation simplicity" fallback.

## 5. Component patterns

- **Cards**: `background: var(--color-surface); border: 1px solid
  var(--color-border); border-radius: var(--radius);` — flat, no heavy
  shadow. Elevation only where something is genuinely floating (menus,
  modals).
- **Status badges**: color + text together, never color alone (existing
  `.badge` classes in `company-research.scss` already follow this —
  extend, don't replace).
- **AI marker**: a single `✦` prefix on any AI-sourced label ("✦ AI
  Summary"). One glyph, used consistently, no icon library needed for it.
- **Buttons**: 8–10px radius, not pill-shaped. Primary = filled accent,
  secondary = outline, destructive = danger-colored outline.

## 6. Command Center — what's real vs. deferred

The proposal's Command Center mockup includes KPI trend deltas ("+12%"),
an "AI Intelligence" opportunity card, and a "Needs Your Attention" feed.
None of those are backed by real data yet:

- **KPI counts** (companies/contacts/leads totals) — buildable now, from
  the existing list endpoints (`GET /companies`, `/contacts`, `/leads`).
  No trend deltas though — there's no historical snapshot data to compute
  a real "+12%" against; showing one would be fabricated. Add a real trend
  once there's something to diff against (e.g. a periodic snapshot job).
- **Pipeline stage counts** (Discovered → Researched → Qualified → ...) —
  same constraint: real counts per stage are buildable from existing
  list/filter endpoints, but this may require several separate requests
  until there's a dedicated aggregate endpoint. Fine for now at expected
  dev data volumes; revisit if it gets slow.
- **"AI Intelligence" opportunity card** and **"Needs Your Attention"
  feed** — both need cross-entity synthesis logic that doesn't exist
  anywhere in the backend today (e.g. "14 companies show automation
  signals" is a real query someone has to write). Deferred as their own
  future story once there's a concrete data source to build them from —
  not stubbed with fake numbers now.

## 7. "Act" stage — no backend today

No task/action router exists, nothing is registered in `api_router`, no
persistence. Until a backend epic adds one, the ACT screen can only
present **suggested next actions computed client-side from existing data**
(e.g. Qualification status = "Qualified" + no linked Recommendation yet →
suggest "Generate Recommendation"). Nothing is savable/dismissable across
sessions until a real Action entity exists server-side. Label this
honestly in the UI, don't imply persistence that isn't there.
