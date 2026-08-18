# Company Search & Prompt Fine-Tuning Plan

Originally planning-only; §6 steps 1-2 have since been implemented (see
status note below). Grounded throughout in a full read of the actual
current code (exact files/lines cited), not assumptions about what the
logic probably does.

## Status

- **`[x]` Done (2026-08-17), zero live API calls:** §6 step 1 — un-gated
  `enterprise_exclusion` in `search_companies_handler.py` (it now applies
  unconditionally instead of only when the caller supplies
  `company_size`), and removed `"enterprise"` from
  `EvidenceSignalExtractor.SCALE_STRONG_MARKERS` (§1a, §1c below). Two new
  regression tests added
  (`test_enterprise_marker_in_evidence_is_rejected_even_without_company_size_requested`,
  `test_large_employee_count_in_evidence_is_rejected_even_without_company_size_requested`
  in `tests/application/company_research/handlers/test_search_companies_handler.py`,
  plus `test_scale_signal_the_word_enterprise_alone_is_not_a_strong_marker`
  in `tests/domain/company_research/services/test_evidence_signal_extractor.py`)
  — all confirmed to fail against the pre-fix code and pass after. Full
  backend suite: 535 passing (up from 532), no regressions.
- **`[x]` Done (2026-08-18), zero live API calls:** §6 step 3 — §1b's
  continuous `size_score` curve. Added `IcpMatcher.size_score(employee_count)`
  implementing the exact point table (≤100→10, ≤200→9, ≤500→7, ≤1,000→5,
  >1,000→3, unknown→4), wired into `QualificationScorer.score()` as the
  `ability` sub-score, replacing `EvidenceSignalExtractor.scale_signal`'s
  keyword-presence heuristic entirely (now deleted, along with
  `SCALE_STRONG_MARKERS`/`SCALE_MODERATE_MARKERS` — no longer used
  anywhere). Also corrected a real mismatch this surfaced:
  `enterprise_exclusion`'s default threshold was `500`, silently hard-rejecting
  the entire 501-1,000 band the table itself scores as valid (5/10) —
  raised to `1000` in both `IcpMatcher` and `DomainProfile`'s default, so
  that band is actually reachable. `company_size_label` gained a matching
  "501-1,000"/"1,000+" split (was a single "500+" bucket). Backend suite:
  625 passing.
- **`[x]` Done (2026-08-18), zero live API calls — related but out-of-plan:**
  Gemini/Tavily rate-limit observability. Live-testing this plan's pending
  final verification step (below) surfaced that a real Gemini `429
  RESOURCE_EXHAUSTED` during identity verification was being silently
  swallowed — `AiIdentityVerificationAdapter.verify()` caught every
  exception (a real rate limit included) and returned
  `confidence="LOW"`, making a rate-limited candidate indistinguishable
  from one that was genuinely checked and didn't match; it just vanished
  from the response with no visible signal. Same problem existed for
  Tavily (`AgneticTavilyClient.search()` caught everything, including its
  own SDK's `UsageLimitExceededError`, and returned `[]`). Fixed by adding
  `AIRateLimitException`/`TavilyRateLimitException` (both distinguishable
  via the real SDKs' own exception types — `google.genai.errors.ClientError`
  with `.code == 429`, `tavily.UsageLimitExceededError` — no guessing)
  and threading them through: identity-verification rate limits now
  propagate as a real `CandidateResearchFailure` with a new
  `is_rate_limited: bool` field (visible in the API response's `failures`
  list, not silently dropped), rolled up into a new
  `CompanyResearchBatchResult.rate_limited_count`; discovery/evidence-gathering
  rate limits degrade gracefully (as before) but are now always logged
  with a greppable `RATE_LIMIT` prefix. Frontend: a rate-limited failure
  gets a distinct "Rate limited" badge instead of the generic failure
  badge, plus a banner when `rate_limited_count > 0`. 13 new backend tests
  (against the real SDK exception shapes, not stand-ins) — backend suite:
  **625 passing**. Full detail in this session's own record; not
  duplicated here.
- **`[ ]` Not started:** §1a's new job-posting/freelance-marketplace/
  anonymous-buyer rejects, §1a's UN/government-procurement language
  detection, §2's `DomainProfile` wiring, §3 (discovery query tuning), §4
  (identity-prompt enrichment), §1d (tier tagging), §5
  (recommendation-prompt review).
- **Still pending, costs real quota:** a real `/company-research/search`
  call to confirm §6 steps 1-3 behave correctly against real Tavily/Gemini
  results — attempted 2026-08-18 but blocked by the app's own internal
  daily Gemini budget (20/day, already spent down to 1 remaining by
  earlier live-testing that same day) and, before that, by the
  free-tier per-minute rate limit. Whenever you're ready to spend it
  again (after the daily reset), keep `number_of_companies` low (2-3) to
  fit inside the free-tier per-minute limit.

## Context: why giant companies show up in results today

You shared two tables (a prospecting-priority hierarchy and a company-size
point scale) that describe the *intended* ICP: 5–500 employees is the
target band, 1,000+/government-giant/enterprise-procurement should be
rejected outright. The current code doesn't implement that — six
independent, compounding bugs let large companies through:

1. **The size filter and enterprise-exclusion filter are opt-in, not
   default.** `search_companies_handler.py` (around lines 318–324) only
   calls `IcpMatcher.matches_size(...)` and `IcpMatcher.enterprise_exclusion(...)`
   **inside `if request.company_size:`** blocks. `CompanyResearchRequest.company_size`
   defaults to `[]` (empty list). So unless the API caller explicitly
   passes a `company_size` value on every single request, **zero size
   filtering happens at all** — any size company can appear.
2. **No server-side default encodes the ICP.** The request DTO has no
   `["small","medium"]`-style default, and no numeric min/max employee
   fields exist at all — only free-text strings like `"small"`/`"51-200"`
   that the caller has to know to supply.
3. **Discovery queries are size-agnostic.** `TavilyDiscoveryAdapter`'s
   query templates (`app/infrastructure/company_research/tavily_discovery_adapter.py`,
   `_discover_candidates`) are generic `"{industry} companies in
   {geography} official company website"` — no SMB-biasing terms, no
   `-enterprise`/`-multinational` exclusions. Even when `company_size`
   *is* supplied, it's appended as raw tokens to only 1 of the 4 query
   variants generated per industry.
4. **Scoring actively rewards "enterprise" language.** In
   `EvidenceSignalExtractor.scale_signal` (`app/domain/company_research/services/evidence_signal_extractor.py`,
   lines ~24–51), `SCALE_STRONG_MARKERS` literally includes the word
   `"enterprise"` (plus `"million"`, `"billion"`) — finding that word in a
   candidate's evidence text scores the **highest** `ability` sub-score
   (12/12 in `qualification_scorer.py`). This is backwards for your ICP:
   evidence that a company is enterprise-scale should count *against* it,
   not for it.
5. **Nothing rejects job postings / freelance-marketplace / anonymous
   listings.** There's no candidate-source classifier anywhere in the
   funnel that recognizes "this is a LinkedIn/Indeed job posting" or "this
   is an Upwork/Fiverr gig listing" and excludes it — your hierarchy table
   explicitly calls these out as auto-reject categories.
6. **Per-sector size overrides are dead code at the call site.**
   `DomainProfile.enterprise_exclusion_threshold`/`enterprise_exclusion_markers`
   exist as a mechanism, but `enterprise_exclusion(...)` is always called
   with `profile=None` in the handler, so sector-specific thresholds never
   actually apply even where the profile system would otherwise let a
   Manufacturing profile use a different cutoff than a Financial Services
   one.

None of this involves the identity-verification AI prompt — it only
checks "is this the exact company/website, not a same-word different
company or unrelated parent" (`app/infrastructure/company_research/ai_identity_verification_adapter.py`,
`_build_prompt`). It never asks about size at all, so it can't be the
source of the leak.

**The practical implication: every fix below except one (§3) is pure
deterministic Python — regex, thresholds, list membership. Zero new
Gemini/Tavily calls required to fix the actual bug**, which fits neatly
alongside the zero-quota-risk intermediate sprint already planned.

---

## 1. Encode your two tables as the real scoring/gating rules

### 1a. Hard reject list (replaces/extends `enterprise_exclusion`)

Make these an unconditional reject — not gated behind `request.company_size`
being non-empty, and not overridable by a high qualification score:

- Employee count `> 1,000` (was: only checked when `company_size` supplied; threshold already defaulted to 500 in code, but never reached due to bug #1)
- `_DEFAULT_ENTERPRISE_MARKERS` text hits (already-correct list: `"fortune 500"`, `"global 2000"`, `"multinational corporation"`, `"conglomerate"`, etc.) — keep, just make it unconditional
- **New:** UN / government-giant / large-institution procurement language (e.g. `"united nations"`, `"ministry of"`, `"government of"`, `"public procurement"`, `"tender notice"` combined with a large-scale marker) — your table treats plain "Government/local authority" as C-tier (conditional), but "UN / multinational / Government / giant enterprise procurement" as reject; the distinguishing signal is scale + procurement-process language, not "government" alone
- **New:** job-posting source — evidence/candidate page host matches known job boards (`indeed.`, `linkedin.com/jobs`, `glassdoor.`, `naukri.`) or page title matches job-posting patterns
- **New:** freelance-marketplace source — host matches `upwork.com`, `fiverr.com`, `freelancer.com`, etc.
- **New:** anonymous-buyer signal — no identifiable company name/domain resolvable at all (this may already partially happen via the identity-verification gate, worth confirming rather than assuming)

### 1b. Replace the bucket-boolean size check with your continuous curve

Today `IcpMatcher.matches_size` is a pass/fail against a caller-supplied
band. Your table wants a **score**, not a boolean, so a company that's
technically outside a requested band but close doesn't get treated
identically to one that's wildly oversized:

| Employees | Points (your table) |
|---|---|
| 5–25 | 10/10 |
| 26–100 | 10/10 |
| 101–200 | 9/10 |
| 201–500 | 7/10 |
| 501–1,000 | 5/10 |
| 1,000+ | 3/10 → **reject** (per your "Reject" annotation) |
| Government/large institution | 2/10 → **reject** unless exceptional |
| Enterprise procurement | 1/10 → **reject** |

Proposal: add a new `IcpMatcher.size_score(employee_count: int | None) -> int`
pure function implementing this exact table, feed it into
`QualificationScore` as (or alongside) the `ability` dimension instead of
`EvidenceSignalExtractor.scale_signal`'s crude 3-bucket heuristic. When
`employee_count` is `None` (couldn't be extracted from evidence), fall
back to today's moderate/no-evidence handling rather than guessing.

### 1c. Fix the inverted "enterprise" signal

Remove `"enterprise"` (and reconsider `"million"`/`"billion"` — these
often describe *funding raised*, a genuinely good buying signal for a
startup, not company size) from `SCALE_STRONG_MARKERS`. If scale language
should influence scoring at all, it should feed the new `size_score`
(§1b) in the *penalizing* direction, not reward `ability`.

### 1d. Priority-tier tag on the response (optional, matches your 🟢🟡🟠🔴 table)

Your prospecting hierarchy is richer than a single score — it
distinguishes *why* something is A-tier (SME with a project vs.
startup-needing-MVP vs. clinic-needing-automation). Full semantic
classification of "what kind of buyer is this" would need an LLM read of
the evidence (a real prompt-design task, see §3) — but a cheap
deterministic approximation (size band + presence of a services/industry
match + presence of a named decision-maker contact) could tag results
`A`/`B`/`C` today with zero extra AI calls, then be refined later once
you're ready to spend a Gemini call per candidate on it.

---

## 2. Make the ICP the default, not an opt-in

- Give `CompanyResearchRequest.company_size` a real default (e.g.
  `["startup", "small", "medium"]` covering your 5–500 band) instead of
  `[]`, **or** — cleaner — decouple the reject rules in §1a/§1b from
  `request.company_size` entirely so they always apply, and keep
  `company_size` purely as an optional *narrowing* filter on top (e.g.
  caller wants only 26–100, a subset of the always-applied 5–500 ceiling).
  The second option is more robust: it means a caller can never
  accidentally get enterprise results just by omitting a field.
- Wire the real `DomainProfile` into `enterprise_exclusion(...)` at the
  call site instead of always passing `profile=None`, so sector-specific
  thresholds (if any sector genuinely needs a different cutoff) actually
  take effect.

## 3. Discovery query tuning (still zero AI calls — Tavily search, not generation)

- Add a default negative/positive bias to every query template, not just
  one of four: e.g. append `-"fortune 500" -multinational -conglomerate`
  or `small business OR SME OR "mid-size company"` depending on which
  Tavily responds better to (worth a **single manual comparison test**
  once you're ready to spend a small Tavily budget on it — not required
  to ship the deterministic fixes first).
- Consider a dedicated query variant seeded from the 🟢A row language
  itself (e.g. `"{industry} SME {geography} looking for automation OR
  MVP OR dashboard"`) to directly surface the buyer intent your hierarchy
  describes, rather than only filtering after the fact.

## 4. Identity-verification prompt (Gemini) — optional enrichment, not a fix

This prompt isn't the cause of the bug, but since you asked about "all
prompts": it currently only decides identity match. Two low-risk additions
that reuse the *same* call (no new quota spent, since this candidate is
already being verified) rather than adding a new one:

- Ask the model to also return a `scale_hint: "small" | "medium" |
  "large" | "unknown"` field based on the evidence block it already
  receives, as a *secondary* signal alongside the deterministic
  `size_score` (§1b) — never the sole gate, since deterministic
  employee-count extraction should remain the primary, free, always-on
  check.
- Keep the existing identity-disambiguation instructions untouched
  (the Lathangi-Motors-vs-Tata-Motors rule is unrelated and working as
  designed) — this would be an additive field, not a rewrite.

## 5. Recommendation-generation prompt (Gemini) — unrelated to this bug, brief note

The `create_recommendation_handler.py` prompt is unrelated to company
size (it operates on already-qualified Assessment findings, not raw
search candidates) and already has solid guardrails (explicit
catalog-vs-generic-idea rules, strict JSON-only output, real solution
types/priorities enumerated). No changes proposed here unless you've
observed a specific problem with its output — flagging only because you
asked about "all... prompts."

---

## 6. Suggested implementation order (all deterministic, zero quota risk)

1. Un-gate §1a/§2 (hard rejects apply unconditionally) — highest-impact, smallest change, directly stops the leak you're seeing.
2. Fix §1c (remove "enterprise" from strong-scale markers) — one-line-ish change, stops the inverted-reward bug.
3. Add §1b's `size_score` curve, wire into `QualificationScore.ability` (or a new dimension) — the biggest single piece of new logic, but pure math over an already-extracted employee count.
4. Wire real `DomainProfile` into `enterprise_exclusion` instead of `None` (§2).
5. Add the job-posting/freelance-marketplace/anonymous-buyer reject checks (§1a new items) — needs a small new classifier function, still pure string/host matching.
6. Discovery query tuning (§3) — lowest priority; the size gate fix alone should already remove most giant companies even with today's generic queries, since discovery casts a wide net *on purpose* and filtering is supposed to narrow it.
7. §4 (AI prompt enrichment) and §1d (tier tagging) — genuine nice-to-haves, explicitly last, and the only items that touch an AI prompt at all.

Every item through step 6 is testable with synthetic evidence strings and
fixture `CompanyResearchRequest`s against the existing pure functions
(`IcpMatcher`, `EvidenceSignalExtractor`, `QualificationScorer` are all
unit-testable in isolation already) — this can be fully built and
regression-tested **without spending a single Gemini or Tavily call**,
consistent with the intermediate no-quota-risk sprint. Only a final
spot-check (one real `/company-research/search` call) would need live
API budget, and only once, at the very end, to confirm the fix behaves
the same way against real Tavily results as it does in unit tests.
