# Company Research Rebuild + Multi-Provider AI Pipeline — Phased Plan

This documents the rebuild of `company_research` into the same
domain/application/infrastructure/presentation shape as the rest of the app,
and the parallel work that made `app/infrastructure/ai` a real, centralized,
multi-provider AI client (Gemini, OpenAI, Azure OpenAI) instead of stub code.

Status legend: ✅ done and verified · 🟡 done in code, pending external
action (credentials/billing) · ⬜ not started.

## Phase 0 — Architecture review & decision

- Reviewed the pre-refactor `app/company_research/` module and the partially
  migrated `app/domain/company_research/`, `app/application/company_research/ports/`.
- Identified the core defect: identity resolution used substring/token
  matching, so e.g. "Lathangi Motors Private Limited" could resolve to
  `tatamotors.com` on the word "Motors" alone.
- Decision (user-confirmed): fix identity verification with **AI-assisted
  verification** rather than a fully deterministic ruleset.
- Discovered `app/infrastructure/ai/*` (the shared AI client stack) was
  non-functional stub code. Decision (user-confirmed): implement it for real,
  as centralized infrastructure reusable by any module — not a
  company_research-only hack.

**Status: ✅ Done**

## Phase 1 — Real, centralized Gemini AI client

- `app/infrastructure/configuration/gemini_settings.py` — `GeminiSettings`
  (`gemini_api_key`, `gemini_model`, `.env`-backed).
- `app/infrastructure/ai/clients/gemini_client.py` — real implementation on
  `google-genai`, including the `thinking_budget=0` fix (Gemini 2.5 was
  silently consuming the token budget on "thinking" and truncating output).
- `app/infrastructure/ai/providers/gemini_provider.py` — builds a real
  `AIResponse` domain entity (was previously returning a raw dict).
- `app/infrastructure/ai/composition.py` — factory wiring settings → client →
  provider → `AIExecutionService`.
- Live-verified against the real `GEMINI_API_KEY` in `.env`.

**Status: ✅ Done and live-verified**

## Phase 2 — Company research domain layer

Pure, network-free domain services under `app/domain/company_research/`,
ported out of the old monolithic Tavily provider and made independently
unit-testable:

- `value_objects/qualification_score.py` — business_fit / evidence /
  buying_signal / ability / accessibility breakdown, total (0–100), tier.
- `services/industry_classifier.py` — industry keyword matching.
- `services/icp_matcher.py` — employee-count extraction, size matching,
  enterprise/parent-company exclusion.
- `services/evidence_signal_extractor.py` — hiring/growth/tech/funding signal
  detection, 4-tier evidence classification (Confirmed Need / Strong
  Opportunity Signal / Reasonable Business Hypothesis / Unverified
  Assumption).
- `services/opportunity_mapper.py`, `services/qualification_scorer.py` —
  weighted scoring from signals + evidence + request.

**Status: ✅ Done, unit-tested**

## Phase 3 — Application layer rebuild

- `dto/company_research_request.py`, `dto/company_research_response.py` —
  moved from the old `app/company_research/schemas/`, field-identical (no
  API contract change).
- `ports/evidence_research_port.py` (new) alongside the existing
  `company_discovery_port.py` / `identity_verification_port.py`.
- `company_research_mapper.py` — assembles the response DTO from candidate +
  identity result + evidence + score + signals.
- `handlers/search_companies_handler.py` — orchestrates discovery → funnel
  gating → bounded-concurrency identity/evidence fan-out → domain scoring →
  mapping → filter/sort/truncate. Replaces the old `CompanyResearchService`.

**Status: ✅ Done, unit-tested**

## Phase 4 — Infrastructure adapters, configuration, presentation cutover

- `app/infrastructure/company_research/tavily_discovery_adapter.py`,
  `tavily_evidence_adapter.py` — implement the discovery/evidence ports on
  top of the existing Tavily client.
- `app/infrastructure/company_research/ai_identity_verification_adapter.py`
  — implements identity verification via the Gemini/AI pipeline, with an
  explicit prompt guarding against same-word/wrong-parent matches (the
  Lathangi Motors vs Tata Motors case), and safe fallbacks (never silently
  upgrades to a match on error/ambiguity).
- `app/infrastructure/configuration/company_research_settings.py` — centralized
  tunables (candidate pool sizing, concurrency, evidence limits, minimum
  identity confidence, AI provider).
- `app/infrastructure/configuration/tavily_settings.py` — moved here from
  `app/integrations/tavily/` for one single settings home.
- `app/presentation/api/dependencies/company_research.py`,
  `routers/company_research_router.py` — DI-wired handler, same route/contract.
- Deleted the entire legacy `app/company_research/` module and
  `tests/company_research/`; corrected the stale path reference in `README.md`.

**Status: ✅ Done, unit-tested (330/330 passing)**

## Phase 5 — Multi-provider AI support (OpenAI + Azure OpenAI)

- `app/infrastructure/configuration/openai_settings.py`,
  `azure_openai_settings.py` — new settings classes.
- `app/infrastructure/ai/clients/openai_client.py`,
  `azure_openai_client.py` — real implementations on `openai`'s
  `AsyncOpenAI` / `AsyncAzureOpenAI`.
- `app/infrastructure/ai/providers/openai_finish_reason.py` — shared
  finish-reason mapper used by both OpenAI-family providers.
- `app/infrastructure/ai/composition.py` — extended to
  `build_ai_providers()` returning `{"gemini", "openai", "azure_openai"}`,
  plus `default_model_for_provider()`.
- `CompanyResearchSettings.ai_provider` — single `.env` switch
  (`AI_PROVIDER=gemini|openai|azure_openai`) controlling which provider the
  identity-verification adapter uses. Confirmed via live settings resolution.

**Status: ✅ Code done, unit-tested. Gemini and OpenAI live-verified
end-to-end (see Phase 6). Azure OpenAI wired but 🟡 blocked on credentials.**

## Phase 6 — Live verification & environment issues

- Gemini: live call verified working end-to-end against the real API key.
- OpenAI: found and resolved a stale Windows **User**-scope
  `OPENAI_API_KEY` environment variable shadowing the `.env` value (removed
  with explicit user confirmation). Authentication now succeeds.
- 🟡 OpenAI account currently has **no billing credits** — `429
  insufficient_quota` on live calls. Needs credits added at
  platform.openai.com before OpenAI live calls will succeed.
- 🟡 Gemini free tier is capped at 20 requests/day; may need the daily quota
  to reset for further live testing.
- ⬜ Azure OpenAI: no `AZURE_OPENAI_API_KEY` / endpoint / deployment name
  configured yet — nothing further to do until provided.

**Status: 🟡 Partially blocked on external account/credential state, not code**

---

## Current overall status

Phases 0–5 are complete in code and covered by the full test suite
(`330 passed`). Phase 6 is code-complete but two items are blocked on
external account state (OpenAI billing, Azure OpenAI credentials) rather
than anything in this repo.

**Not yet done:** none of the above is committed to git — everything is
still uncommitted working-tree changes (see `git status`).
