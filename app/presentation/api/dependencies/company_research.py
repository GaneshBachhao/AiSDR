"""
API dependencies for the company_research module.

Provides the application handler to the presentation layer, following the
same ``Depends`` chain pattern as ``app.presentation.api.dependencies.handlers``.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.handlers.create_company_handler import CreateCompanyHandler
from app.application.company_research.handlers.promote_candidate_to_company_handler import (
    PromoteCandidateToCompanyHandler,
)
from app.application.company_research.handlers.search_companies_handler import (
    SearchCompaniesHandler,
)
from app.application.ai.ports.ai_budget_port import AIBudgetPort
from app.infrastructure.ai.composition import (
    build_ai_budget_guard,
    build_ai_execution_service,
    default_ai_provider,
)
from app.infrastructure.company_research.ai_identity_verification_adapter import (
    AiIdentityVerificationAdapter,
)
from app.infrastructure.company_research.tavily_contact_discovery_adapter import (
    TavilyContactDiscoveryAdapter,
)
from app.infrastructure.company_research.tavily_directory_adapter import (
    TavilyDirectoryAdapter,
)
from app.infrastructure.company_research.tavily_discovery_adapter import (
    TavilyDiscoveryAdapter,
)
from app.infrastructure.company_research.tavily_evidence_adapter import (
    TavilyEvidenceAdapter,
)
from app.domain.recommendation.value_objects.solution_catalog_entry import (
    SolutionCatalogEntry,
)
from app.infrastructure.configuration.solution_catalog import load_existing_offerings
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.tavily_client import AgneticTavilyClient
from app.presentation.api.dependencies.handlers import get_create_company_handler
from app.presentation.api.dependencies.persistence import get_unit_of_work


def get_company_research_settings() -> CompanyResearchSettings:
    return CompanyResearchSettings()


def get_tavily_client() -> AgneticTavilyClient:
    return AgneticTavilyClient()


def get_ai_execution_service() -> AIExecutionService:
    return build_ai_execution_service()


def get_ai_budget_guard() -> AIBudgetPort:
    return build_ai_budget_guard()


def get_discovery_adapter(
    client: AgneticTavilyClient = Depends(get_tavily_client),
    settings: CompanyResearchSettings = Depends(get_company_research_settings),
) -> TavilyDiscoveryAdapter:
    return TavilyDiscoveryAdapter(client=client, settings=settings)


_directory_adapter: TavilyDirectoryAdapter | None = None


def get_directory_adapter(
    client: AgneticTavilyClient = Depends(get_tavily_client),
    settings: CompanyResearchSettings = Depends(get_company_research_settings),
) -> TavilyDirectoryAdapter:
    """Singleton, like ``get_database_engine`` -- the adapter's in-memory
    cache only saves anything if the same instance persists across requests."""
    global _directory_adapter
    if _directory_adapter is None:
        _directory_adapter = TavilyDirectoryAdapter(client=client, settings=settings)
    return _directory_adapter


def get_evidence_adapter(
    client: AgneticTavilyClient = Depends(get_tavily_client),
    settings: CompanyResearchSettings = Depends(get_company_research_settings),
) -> TavilyEvidenceAdapter:
    return TavilyEvidenceAdapter(client=client, settings=settings)


def get_identity_adapter(
    client: AgneticTavilyClient = Depends(get_tavily_client),
    ai_service: AIExecutionService = Depends(get_ai_execution_service),
) -> AiIdentityVerificationAdapter:
    return AiIdentityVerificationAdapter(
        ai_service=ai_service,
        tavily_client=client,
        provider_name=default_ai_provider(),
    )


def get_candidate_promoter(
    uow: UnitOfWork = Depends(get_unit_of_work),
    create_company_handler: CreateCompanyHandler = Depends(get_create_company_handler),
) -> PromoteCandidateToCompanyHandler:
    return PromoteCandidateToCompanyHandler(
        unit_of_work=uow,
        create_company_handler=create_company_handler,
    )


def get_solution_catalog() -> list[SolutionCatalogEntry]:
    return load_existing_offerings()


def get_contact_discovery_adapter(
    client: AgneticTavilyClient = Depends(get_tavily_client),
    settings: CompanyResearchSettings = Depends(get_company_research_settings),
) -> TavilyContactDiscoveryAdapter:
    return TavilyContactDiscoveryAdapter(client=client, settings=settings)


def get_search_companies_handler(
    discovery: TavilyDiscoveryAdapter = Depends(get_discovery_adapter),
    directory: TavilyDirectoryAdapter = Depends(get_directory_adapter),
    identity: AiIdentityVerificationAdapter = Depends(get_identity_adapter),
    evidence: TavilyEvidenceAdapter = Depends(get_evidence_adapter),
    settings: CompanyResearchSettings = Depends(get_company_research_settings),
    budget_guard: AIBudgetPort = Depends(get_ai_budget_guard),
    candidate_promoter: PromoteCandidateToCompanyHandler = Depends(get_candidate_promoter),
    solution_catalog: list[SolutionCatalogEntry] = Depends(get_solution_catalog),
    contact_discovery: TavilyContactDiscoveryAdapter = Depends(get_contact_discovery_adapter),
) -> SearchCompaniesHandler:
    return SearchCompaniesHandler(
        discovery_port=discovery,
        identity_port=identity,
        evidence_port=evidence,
        max_concurrent_research=settings.max_concurrent_research,
        min_identity_confidence=settings.min_identity_confidence,
        budget_port=budget_guard,
        ai_provider_name=default_ai_provider(),
        directory_port=directory,
        candidate_promoter=candidate_promoter,
        solution_catalog=solution_catalog,
        contact_port=contact_discovery,
    )


SearchCompaniesHandlerDependency = Annotated[
    SearchCompaniesHandler,
    Depends(get_search_companies_handler),
]
