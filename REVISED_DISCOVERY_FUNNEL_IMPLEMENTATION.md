# Revised Discovery Funnel — Implementation Cycle

## Architectural decision

The discovery path is now an asymmetric funnel. Expensive verification and deep research are downstream of a deterministic candidate gate.

```text
Search / discovery sources
        |
        v
Raw result extraction
        |
        v
Canonical identity normalization
(name + root domain)
        |
        v
Deterministic hard gate
(blocked domains, documents, generic/list titles,
invalid names, duplicate identity)
        |
        v
Candidate verification + ICP hard gate
(industry, geography, explicit employee count,
SMB/mid-market range, enterprise exclusion)
        |
        v
Deep public-web research
        |
        v
Qualification / scoring
        |
        v
CRM persistence (Company -> Contact -> Lead)
```

### Cost boundary

Only the first two layers are allowed to handle the broad discovery pool. A candidate must pass the deterministic gate before `_research_candidate()` can perform verification/deeper searches.

### Persistence boundary

The company-research endpoint remains a research-only boundary. It does not create Company, Contact, Lead, Discovery, Recommendation, or Email records. Existing CRM modules therefore remain outside the new funnel's write path.

## Implementation cycle

1. **Discover** — query configured public discovery sources.
2. **Extract** — identify actual company candidates; directory pages are treated as source metadata, not companies.
3. **Normalize** — canonicalize company name and root domain.
4. **Gate** — reject non-company pages, blocked domains/documents, malformed identities, and duplicates without LLM calls.
5. **Verify + ICP gate** — verify identity/industry first; when `company_size` is requested, require explicit employee-count evidence, enforce the requested employee range, and reject obvious enterprise-scale companies before deep research. Unknown employee count does not pass a size-restricted ICP.
6. **Research** — collect company-specific evidence and trigger signals only for ICP-approved candidates.
7. **Qualify** — calculate deterministic qualification/priority signals from evidence.
8. **Persist later** — only a future explicit CRM stage should create Company/Contact/Lead records.

## Files added/changed

### Added
- `app/company_research/funnel/candidate.py`
- `app/company_research/funnel/normalizer.py`
- `app/company_research/funnel/gate.py`
- `app/company_research/funnel/pipeline.py`
- `tests/company_research/funnel/test_discovery_funnel.py`
- this document

### Changed
- `app/company_research/providers/tavily_provider.py` — invokes the deterministic gate before verification, then enforces the requested employee-size ICP and enterprise exclusion before deep research.
- `app/company_research/schemas/company_research.py` — adds backward-compatible research metadata for employee count, parent company, and ICP match reasoning.
- `app/company_research/funnel/gate.py` — blocks common job-board/document/search-content domains that were previously leaking into the candidate universe.
- `app/integrations/tavily/tavily_client.py` — treats the Tavily SDK as an optional integration dependency so application import and unit tests do not fail merely because the SDK is absent.

No existing CRM aggregate, repository, Unit of Work, database model, router contract, or persistence migration was changed by this implementation.

## Validation performed

- Python compilation: passed for `app` and `tests`.
- FastAPI application import: passed; `/company-research/search` is registered.
- Revised company-research suite: **13 passed**.
- Added regression coverage for large-company rejection and unknown employee-count rejection under a size-restricted request.

The repository also contains older, unrelated test suites that currently fail during collection/execution because of pre-existing architecture/test-contract inconsistencies (for example duplicate legacy SQLAlchemy models and stale UUID/test fixtures). Those were intentionally not rewritten because doing so would violate the requirement not to alter unrelated modules.
