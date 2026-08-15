"""
Bridges a qualified research result into the CRM's canonical Company
aggregate -- the "Entity Resolution" step from
docs/pamacore_aisdr_summary.md §5/§9 (Track 1 Phase 3).

Only invoked when a caller explicitly opts in via
``CompanyResearchRequest.persist_as_companies`` (see the architecture doc's
§11 decision #1) -- company_research's "research-only, no side effects"
contract is preserved by default.

Entity resolution order: match by website first (a more reliable identity
key than name -- names vary across sources, domains usually don't), then
fall back to ``CreateCompanyHandler``'s own existing name-based duplicate
check. A new ``Company`` is created only when neither matches.
"""

from __future__ import annotations

from app.application.common.exceptions.conflict_exception import ConflictException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_commands import CreateCompanyCommand
from app.application.company.handlers.create_company_handler import CreateCompanyHandler
from app.application.company_research.dto.company_research_response import (
    CompanySearchResult,
)
from app.domain.company_research.services.candidate_normalizer import (
    CandidateNormalizer,
)


class PromoteCandidateToCompanyHandler:
    """Resolves or creates the CRM ``Company`` for one research result."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        create_company_handler: CreateCompanyHandler,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._create_company_handler = create_company_handler

    async def handle(self, result: CompanySearchResult) -> str:
        """Return the id of the matched or newly-created Company."""

        website = (
            CandidateNormalizer.normalize_root_url(str(result.website))
            if result.website
            else None
        )

        if website:
            existing = await self._unit_of_work.company_repository.find_by_website(
                website
            )
            if existing is not None:
                return str(existing.id.value)

        command = CreateCompanyCommand(
            name=result.company_name,
            website=website,
            industry=result.industry,
            company_size=result.company_size,
            employee_count=result.employee_count,
            country=result.location,
        )

        try:
            response = await self._create_company_handler.handle(command)
        except ConflictException:
            # Name-based duplicate, caught by CreateCompanyHandler's own
            # check -- not a new-name-with-matching-website case, since
            # that was already ruled out above. Resolve to the existing row.
            existing = await self._unit_of_work.company_repository.find_by_name(
                result.company_name
            )
            if existing is not None:
                return str(existing.id.value)
            raise

        return response.id
