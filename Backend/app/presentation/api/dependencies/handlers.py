"""
API handler dependencies.

Provides application handlers to FastAPI presentation layer.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, TypeVar

from fastapi import Depends

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.assessment.handlers.complete_assessment_handler import (
    CompleteAssessmentHandler,
)
from app.application.assessment.handlers.create_assessment_handler import (
    CreateAssessmentHandler,
)
from app.application.assessment.handlers.delete_assessment_handler import (
    DeleteAssessmentHandler,
)
from app.application.assessment.handlers.get_assessment_handler import (
    GetAssessmentHandler,
)
from app.application.assessment.handlers.list_assessment_handler import (
    ListAssessmentHandler,
)
from app.application.assessment.handlers.start_assessment_handler import (
    StartAssessmentHandler,
)
from app.application.assessment.handlers.update_assessment_handler import (
    UpdateAssessmentHandler,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.application.company.company_mapper import (
    CompanyMapper,
)
from app.application.company.company_validator import (
    CompanyValidator,
)
from app.application.company.handlers.create_company_handler import (
    CreateCompanyHandler,
)
from app.application.company.handlers.delete_company_handler import (
    DeleteCompanyHandler,
)
from app.application.company.handlers.get_company_handler import (
    GetCompanyHandler,
)
from app.application.company.handlers.list_company_handler import (
    ListCompanyHandler,
)
from app.application.company.handlers.search_company_handler import (
    SearchCompanyHandler,
)
from app.application.company.handlers.update_company_handler import (
    UpdateCompanyHandler,
)
from app.application.compliance.handlers.get_lead_compliance_ruleset_handler import (
    GetLeadComplianceRulesetHandler,
)
from app.application.compliance.handlers.list_compliance_rulesets_handler import (
    ListComplianceRulesetsHandler,
)
from app.application.contact.contact_mapper import (
    ContactMapper,
)
from app.application.contact.contact_validator import (
    ContactValidator,
)
from app.application.contact.handlers.create_contact_handler import (
    CreateContactHandler,
)
from app.application.contact.handlers.delete_contact_handler import (
    DeleteContactHandler,
)
from app.application.contact.handlers.get_contact_handler import (
    GetContactHandler,
)
from app.application.contact.handlers.list_contact_handler import (
    ListContactHandler,
)
from app.application.contact.handlers.search_contact_handler import (
    SearchContactHandler,
)
from app.application.contact.handlers.update_contact_handler import (
    UpdateContactHandler,
)
from app.application.discovery.discovery_mapper import (
    DiscoveryMapper,
)
from app.application.discovery.discovery_validator import (
    DiscoveryValidator,
)
from app.application.discovery.handlers.create_discovery_handler import (
    CreateDiscoveryHandler,
)
from app.application.discovery.handlers.delete_discovery_handler import (
    DeleteDiscoveryHandler,
)
from app.application.discovery.handlers.get_discovery_handler import (
    GetDiscoveryHandler,
)
from app.application.discovery.handlers.list_discovery_handler import (
    ListDiscoveryHandler,
)
from app.application.discovery.handlers.search_discovery_handler import (
    SearchDiscoveryHandler,
)
from app.application.discovery.handlers.update_discovery_handler import (
    UpdateDiscoveryHandler,
)
from app.application.lead.handlers.approve_lead_handler import (
    ApproveLeadHandler,
)
from app.application.lead.handlers.create_lead_handler import (
    CreateLeadHandler,
)
from app.application.lead.handlers.delete_lead_handler import (
    DeleteLeadHandler,
)
from app.application.lead.handlers.get_lead_handler import (
    GetLeadHandler,
)
from app.application.lead.handlers.get_lead_review_chain_handler import (
    GetLeadReviewChainHandler,
)
from app.application.lead.handlers.list_lead_handler import (
    ListLeadHandler,
)
from app.application.lead.handlers.reject_lead_handler import (
    RejectLeadHandler,
)
from app.application.lead.handlers.search_lead_handler import (
    SearchLeadHandler,
)
from app.application.lead.handlers.submit_lead_for_review_handler import (
    SubmitLeadForReviewHandler,
)
from app.application.lead.handlers.update_lead_handler import (
    UpdateLeadHandler,
)
from app.application.outcome.handlers.create_outcome_event_handler import (
    CreateOutcomeEventHandler,
)
from app.application.outcome.handlers.delete_outcome_event_handler import (
    DeleteOutcomeEventHandler,
)
from app.application.outcome.handlers.list_outcome_events_handler import (
    ListOutcomeEventsHandler,
)
from app.application.qualification.handlers.create_qualification_handler import (
    CreateQualificationHandler,
)
from app.application.qualification.handlers.delete_qualification_handler import (
    DeleteQualificationHandler,
)
from app.application.qualification.handlers.get_qualification_handler import (
    GetQualificationHandler,
)
from app.application.qualification.handlers.list_qualification_handler import (
    ListQualificationHandler,
)
from app.application.qualification.handlers.update_qualification_handler import (
    UpdateQualificationHandler,
)
from app.application.qualification.qualification_commands import (
    CreateQualificationCommand,
    DeleteQualificationCommand,
    UpdateQualificationCommand,
)
from app.application.qualification.qualification_queries import (
    GetQualificationQuery,
    ListQualificationsQuery,
)
from app.application.recommendation.handlers.approve_recommendation_handler import (
    ApproveRecommendationHandler,
)
from app.application.recommendation.handlers.create_recommendation_handler import (
    CreateRecommendationHandler,
)
from app.application.recommendation.handlers.get_recommendation_handler import (
    GetRecommendationHandler,
)
from app.application.recommendation.handlers.list_recommendation_handler import (
    ListRecommendationHandler,
)
from app.application.recommendation.handlers.reject_recommendation_handler import (
    RejectRecommendationHandler,
)
from app.application.recommendation.handlers.submit_recommendation_handler import (
    SubmitRecommendationHandler,
)
from app.application.sequence.handlers.advance_sequence_handler import (
    AdvanceSequenceHandler,
)
from app.application.sequence.handlers.create_sequence_handler import (
    CreateSequenceHandler,
)
from app.application.sequence.handlers.get_sequence_handler import (
    GetSequenceHandler,
)
from app.application.sequence.handlers.list_sequences_handler import (
    ListSequencesHandler,
)
from app.application.sequence.handlers.record_sequence_bounce_handler import (
    RecordSequenceBounceHandler,
)
from app.application.sequence.handlers.record_sequence_reply_handler import (
    RecordSequenceReplyHandler,
)
from app.application.sequence.handlers.start_sequence_handler import (
    StartSequenceHandler,
)
from app.application.suppression.handlers.check_suppression_handler import (
    CheckSuppressionHandler,
)
from app.application.suppression.handlers.create_suppression_handler import (
    CreateSuppressionHandler,
)
from app.application.suppression.handlers.delete_suppression_handler import (
    DeleteSuppressionHandler,
)
from app.application.suppression.handlers.list_suppressions_handler import (
    ListSuppressionsHandler,
)
from app.application.suppression.handlers.record_email_event_handler import (
    RecordEmailEventHandler,
)
from app.application.user.handlers.login_handler import LoginHandler
from app.domain.compliance.services.jurisdiction_resolver import JurisdictionResolver
from app.domain.compliance.value_objects.compliance_ruleset import ComplianceRuleset
from app.infrastructure.ai.composition import build_ai_execution_service, default_ai_provider
from app.infrastructure.configuration.compliance_rulesets import load_all_compliance_rulesets
from app.infrastructure.configuration.jwt_settings import JWTSettings
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_hasher import PasswordHasher
from app.presentation.api.dependencies.persistence import (
    get_unit_of_work,
)

# -------------------------
# Company
# -------------------------


def get_company_mapper() -> CompanyMapper:
    return CompanyMapper()


def get_company_validator() -> CompanyValidator:
    return CompanyValidator()


def get_create_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: CompanyValidator = Depends(get_company_validator),
    mapper: CompanyMapper = Depends(get_company_mapper),
) -> CreateCompanyHandler:

    return CreateCompanyHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_get_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: CompanyMapper = Depends(get_company_mapper),
) -> GetCompanyHandler:

    return GetCompanyHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_list_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: CompanyMapper = Depends(get_company_mapper),
) -> ListCompanyHandler:

    return ListCompanyHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_search_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: CompanyMapper = Depends(get_company_mapper),
) -> SearchCompanyHandler:

    return SearchCompanyHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_update_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: CompanyValidator = Depends(get_company_validator),
    mapper: CompanyMapper = Depends(get_company_mapper),
) -> UpdateCompanyHandler:

    return UpdateCompanyHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_delete_company_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteCompanyHandler:

    return DeleteCompanyHandler(
        unit_of_work=uow,
    )


# -------------------------
# Contact
# -------------------------


def get_contact_mapper() -> ContactMapper:
    return ContactMapper()


def get_contact_validator() -> ContactValidator:
    return ContactValidator()


def get_create_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: ContactValidator = Depends(get_contact_validator),
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> CreateContactHandler:

    return CreateContactHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_get_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> GetContactHandler:

    return GetContactHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_list_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> ListContactHandler:

    return ListContactHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_search_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> SearchContactHandler:

    return SearchContactHandler(
        unit_of_work=uow,
        mapper=mapper,
    )


def get_update_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: ContactValidator = Depends(get_contact_validator),
    mapper: ContactMapper = Depends(get_contact_mapper),
) -> UpdateContactHandler:

    return UpdateContactHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_delete_contact_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteContactHandler:

    return DeleteContactHandler(
        unit_of_work=uow,
    )


# -------------------------
# Lead
# -------------------------


def get_create_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateLeadHandler:

    return CreateLeadHandler(
        unit_of_work=uow,
    )


def get_get_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetLeadHandler:

    return GetLeadHandler(
        unit_of_work=uow,
    )


def get_list_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListLeadHandler:

    return ListLeadHandler(
        unit_of_work=uow,
    )


def get_search_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SearchLeadHandler:

    return SearchLeadHandler(
        unit_of_work=uow,
    )


def get_update_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> UpdateLeadHandler:

    return UpdateLeadHandler(
        unit_of_work=uow,
    )


def get_delete_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteLeadHandler:

    return DeleteLeadHandler(
        unit_of_work=uow,
    )


def get_submit_lead_for_review_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SubmitLeadForReviewHandler:

    return SubmitLeadForReviewHandler(
        unit_of_work=uow,
    )


def get_approve_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ApproveLeadHandler:

    return ApproveLeadHandler(
        unit_of_work=uow,
    )


def get_reject_lead_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RejectLeadHandler:

    return RejectLeadHandler(
        unit_of_work=uow,
    )


def get_lead_review_chain_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetLeadReviewChainHandler:

    return GetLeadReviewChainHandler(
        unit_of_work=uow,
    )


# -------------------------
# Discovery
# -------------------------


def get_discovery_mapper() -> DiscoveryMapper:
    return DiscoveryMapper()


def get_discovery_validator() -> DiscoveryValidator:
    return DiscoveryValidator()


def get_create_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: DiscoveryValidator = Depends(
        get_discovery_validator,
    ),
    mapper: DiscoveryMapper = Depends(
        get_discovery_mapper,
    ),
) -> CreateDiscoveryHandler:

    return CreateDiscoveryHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_get_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: DiscoveryValidator = Depends(
        get_discovery_validator,
    ),
    mapper: DiscoveryMapper = Depends(
        get_discovery_mapper,
    ),
) -> GetDiscoveryHandler:

    return GetDiscoveryHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_list_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    mapper: DiscoveryMapper = Depends(get_discovery_mapper),
    validator: DiscoveryValidator = Depends(get_discovery_validator),
) -> ListDiscoveryHandler:

    return ListDiscoveryHandler(
        unit_of_work=uow,
        mapper=mapper,
        validator=validator,
    )


def get_search_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: DiscoveryValidator = Depends(
        get_discovery_validator,
    ),
    mapper: DiscoveryMapper = Depends(
        get_discovery_mapper,
    ),
) -> SearchDiscoveryHandler:

    return SearchDiscoveryHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_update_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: DiscoveryValidator = Depends(
        get_discovery_validator,
    ),
    mapper: DiscoveryMapper = Depends(
        get_discovery_mapper,
    ),
) -> UpdateDiscoveryHandler:

    return UpdateDiscoveryHandler(
        unit_of_work=uow,
        validator=validator,
        mapper=mapper,
    )


def get_delete_discovery_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    validator: DiscoveryValidator = Depends(
        get_discovery_validator,
    ),
) -> DeleteDiscoveryHandler:

    return DeleteDiscoveryHandler(
        unit_of_work=uow,
        validator=validator,
    )


# -------------------------
# Assessment
# -------------------------


def get_create_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateAssessmentHandler:

    return CreateAssessmentHandler(
        unit_of_work=uow,
    )


def get_get_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetAssessmentHandler:

    return GetAssessmentHandler(
        unit_of_work=uow,
    )


def get_list_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListAssessmentHandler:

    return ListAssessmentHandler(
        unit_of_work=uow,
    )


def get_start_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> StartAssessmentHandler:

    return StartAssessmentHandler(
        unit_of_work=uow,
    )


def get_complete_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CompleteAssessmentHandler:

    return CompleteAssessmentHandler(
        unit_of_work=uow,
    )


def get_update_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> UpdateAssessmentHandler:

    return UpdateAssessmentHandler(
        unit_of_work=uow,
    )


def get_delete_assessment_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteAssessmentHandler:

    return DeleteAssessmentHandler(
        unit_of_work=uow,
    )


# -------------------------
# Qualification
# -------------------------


def get_create_qualification_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateQualificationHandler:

    return CreateQualificationHandler(
        unit_of_work=uow,
    )


def get_get_qualification_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetQualificationHandler:

    return GetQualificationHandler(
        unit_of_work=uow,
    )


def get_list_qualification_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListQualificationHandler:

    return ListQualificationHandler(
        unit_of_work=uow,
    )


def get_update_qualification_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> UpdateQualificationHandler:

    return UpdateQualificationHandler(
        unit_of_work=uow,
    )


def get_delete_qualification_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteQualificationHandler:

    return DeleteQualificationHandler(
        unit_of_work=uow,
    )


# -------------------------
# Recommendation
# -------------------------


def get_ai_execution_service_for_recommendation() -> AIExecutionService:
    return build_ai_execution_service()


def get_create_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    ai_execution_service: AIExecutionService = Depends(get_ai_execution_service_for_recommendation),
) -> CreateRecommendationHandler:
    return CreateRecommendationHandler(
        unit_of_work=uow,
        ai_execution_service=ai_execution_service,
        ai_provider_name=default_ai_provider(),
    )


def get_get_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetRecommendationHandler:
    return GetRecommendationHandler(unit_of_work=uow)


def get_list_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListRecommendationHandler:
    return ListRecommendationHandler(unit_of_work=uow)


def get_submit_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SubmitRecommendationHandler:
    return SubmitRecommendationHandler(unit_of_work=uow)


def get_approve_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ApproveRecommendationHandler:
    return ApproveRecommendationHandler(unit_of_work=uow)


def get_reject_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RejectRecommendationHandler:
    return RejectRecommendationHandler(unit_of_work=uow)


CreateCompanyHandlerDependency = Annotated[
    CreateCompanyHandler,
    Depends(get_create_company_handler),
]


GetCompanyHandlerDependency = Annotated[
    GetCompanyHandler,
    Depends(get_get_company_handler),
]


ListCompanyHandlerDependency = Annotated[
    ListCompanyHandler,
    Depends(get_list_company_handler),
]


UpdateCompanyHandlerDependency = Annotated[
    UpdateCompanyHandler,
    Depends(get_update_company_handler),
]


DeleteCompanyHandlerDependency = Annotated[
    DeleteCompanyHandler,
    Depends(get_delete_company_handler),
]

SearchCompanyHandlerDependency = Annotated[
    SearchCompanyHandler,
    Depends(get_search_company_handler),
]

CreateContactHandlerDependency = Annotated[
    CreateContactHandler,
    Depends(get_create_contact_handler),
]


GetContactHandlerDependency = Annotated[
    GetContactHandler,
    Depends(get_get_contact_handler),
]


ListContactHandlerDependency = Annotated[
    ListContactHandler,
    Depends(get_list_contact_handler),
]


UpdateContactHandlerDependency = Annotated[
    UpdateContactHandler,
    Depends(get_update_contact_handler),
]


DeleteContactHandlerDependency = Annotated[
    DeleteContactHandler,
    Depends(get_delete_contact_handler),
]

SearchContactHandlerDependency = Annotated[
    SearchContactHandler,
    Depends(get_search_contact_handler),
]


CreateLeadHandlerDependency = Annotated[
    CreateLeadHandler,
    Depends(get_create_lead_handler),
]


GetLeadHandlerDependency = Annotated[
    GetLeadHandler,
    Depends(get_get_lead_handler),
]


ListLeadHandlerDependency = Annotated[
    ListLeadHandler,
    Depends(get_list_lead_handler),
]


UpdateLeadHandlerDependency = Annotated[
    UpdateLeadHandler,
    Depends(get_update_lead_handler),
]


DeleteLeadHandlerDependency = Annotated[
    DeleteLeadHandler,
    Depends(get_delete_lead_handler),
]


SubmitLeadForReviewHandlerDependency = Annotated[
    SubmitLeadForReviewHandler,
    Depends(get_submit_lead_for_review_handler),
]


ApproveLeadHandlerDependency = Annotated[
    ApproveLeadHandler,
    Depends(get_approve_lead_handler),
]


RejectLeadHandlerDependency = Annotated[
    RejectLeadHandler,
    Depends(get_reject_lead_handler),
]


GetLeadReviewChainHandlerDependency = Annotated[
    GetLeadReviewChainHandler,
    Depends(get_lead_review_chain_handler),
]


CreateAssessmentHandlerDependency = Annotated[
    CreateAssessmentHandler,
    Depends(get_create_assessment_handler),
]


GetAssessmentHandlerDependency = Annotated[
    GetAssessmentHandler,
    Depends(get_get_assessment_handler),
]


ListAssessmentHandlerDependency = Annotated[
    ListAssessmentHandler,
    Depends(get_list_assessment_handler),
]

CompleteAssessmentHandlerDependency = Annotated[
    CompleteAssessmentHandler,
    Depends(get_complete_assessment_handler),
]

StartAssessmentHandlerDependency = Annotated[
    StartAssessmentHandler,
    Depends(get_start_assessment_handler),
]

UpdateAssessmentHandlerDependency = Annotated[
    UpdateAssessmentHandler,
    Depends(get_update_assessment_handler),
]


DeleteAssessmentHandlerDependency = Annotated[
    DeleteAssessmentHandler,
    Depends(get_delete_assessment_handler),
]

SearchLeadHandlerDependency = Annotated[
    SearchLeadHandler,
    Depends(get_search_lead_handler),
]

CreateQualificationHandlerDependency = Annotated[
    CreateQualificationHandler,
    Depends(get_create_qualification_handler),
]


GetQualificationHandlerDependency = Annotated[
    GetQualificationHandler,
    Depends(get_get_qualification_handler),
]


ListQualificationHandlerDependency = Annotated[
    ListQualificationHandler,
    Depends(get_list_qualification_handler),
]


UpdateQualificationHandlerDependency = Annotated[
    UpdateQualificationHandler,
    Depends(get_update_qualification_handler),
]


DeleteQualificationHandlerDependency = Annotated[
    DeleteQualificationHandler,
    Depends(get_delete_qualification_handler),
]

TCommand = TypeVar("TCommand")
TQuery = TypeVar("TQuery")


def get_command_handler(command_type: type[TCommand]) -> Callable[..., Any]:
    """
    Compatibility helper used by routers that expect a generic command handler dependency.
    """

    def _dependency(
        uow: UnitOfWork = Depends(get_unit_of_work),
    ) -> Any:
        if command_type is CreateQualificationCommand:
            return CreateQualificationHandler(unit_of_work=uow)

        if command_type is UpdateQualificationCommand:
            return UpdateQualificationHandler(unit_of_work=uow)

        if command_type is DeleteQualificationCommand:
            return DeleteQualificationHandler(unit_of_work=uow)

        raise ValueError(f"No handler registered for {command_type}")

    return _dependency


def get_query_handler(query_type: type[TQuery]) -> Callable[..., Any]:
    """
    Compatibility helper used by routers that expect a generic query handler dependency.
    """

    def _dependency(
        uow: UnitOfWork = Depends(get_unit_of_work),
    ) -> Any:
        if query_type is GetQualificationQuery:
            return GetQualificationHandler(unit_of_work=uow)

        if query_type is ListQualificationsQuery:
            return ListQualificationHandler(unit_of_work=uow)

        raise ValueError(f"No handler registered for {query_type}")

    return _dependency


CreateDiscoveryHandlerDependency = Annotated[
    CreateDiscoveryHandler,
    Depends(get_create_discovery_handler),
]

GetDiscoveryHandlerDependency = Annotated[
    GetDiscoveryHandler,
    Depends(get_get_discovery_handler),
]

ListDiscoveryHandlerDependency = Annotated[
    ListDiscoveryHandler,
    Depends(get_list_discovery_handler),
]

SearchDiscoveryHandlerDependency = Annotated[
    SearchDiscoveryHandler,
    Depends(get_search_discovery_handler),
]

UpdateDiscoveryHandlerDependency = Annotated[
    UpdateDiscoveryHandler,
    Depends(get_update_discovery_handler),
]

DeleteDiscoveryHandlerDependency = Annotated[
    DeleteDiscoveryHandler,
    Depends(get_delete_discovery_handler),
]
CreateRecommendationHandlerDependency = Annotated[
    CreateRecommendationHandler,
    Depends(get_create_recommendation_handler),
]

GetRecommendationHandlerDependency = Annotated[
    GetRecommendationHandler,
    Depends(get_get_recommendation_handler),
]

ListRecommendationHandlerDependency = Annotated[
    ListRecommendationHandler,
    Depends(get_list_recommendation_handler),
]

SubmitRecommendationHandlerDependency = Annotated[
    SubmitRecommendationHandler,
    Depends(get_submit_recommendation_handler),
]

ApproveRecommendationHandlerDependency = Annotated[
    ApproveRecommendationHandler,
    Depends(get_approve_recommendation_handler),
]

RejectRecommendationHandlerDependency = Annotated[
    RejectRecommendationHandler,
    Depends(get_reject_recommendation_handler),
]


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_service() -> JWTService:
    return JWTService(JWTSettings())


def get_login_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> LoginHandler:

    return LoginHandler(
        unit_of_work=uow,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )


LoginHandlerDependency = Annotated[
    LoginHandler,
    Depends(get_login_handler),
]


# -------------------------
# Suppression (EPIC-11)
# -------------------------


def get_create_suppression_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateSuppressionHandler:

    return CreateSuppressionHandler(unit_of_work=uow)


def get_delete_suppression_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteSuppressionHandler:

    return DeleteSuppressionHandler(unit_of_work=uow)


def get_list_suppressions_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListSuppressionsHandler:

    return ListSuppressionsHandler(unit_of_work=uow)


def get_check_suppression_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CheckSuppressionHandler:

    return CheckSuppressionHandler(unit_of_work=uow)


def get_record_email_event_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RecordEmailEventHandler:

    return RecordEmailEventHandler(unit_of_work=uow)


CreateSuppressionHandlerDependency = Annotated[
    CreateSuppressionHandler,
    Depends(get_create_suppression_handler),
]

DeleteSuppressionHandlerDependency = Annotated[
    DeleteSuppressionHandler,
    Depends(get_delete_suppression_handler),
]

ListSuppressionsHandlerDependency = Annotated[
    ListSuppressionsHandler,
    Depends(get_list_suppressions_handler),
]

CheckSuppressionHandlerDependency = Annotated[
    CheckSuppressionHandler,
    Depends(get_check_suppression_handler),
]

RecordEmailEventHandlerDependency = Annotated[
    RecordEmailEventHandler,
    Depends(get_record_email_event_handler),
]


# -------------------------
# Compliance (EPIC-11)
# -------------------------

# Loaded once, at process scope, same singleton pattern as
# get_directory_adapter (app/presentation/api/dependencies/company_research.py)
# -- the ruleset files never change at runtime, so re-reading them from
# disk on every request would be pure waste.
_compliance_rulesets: dict[str, ComplianceRuleset] | None = None


def get_compliance_rulesets() -> dict[str, ComplianceRuleset]:
    global _compliance_rulesets
    if _compliance_rulesets is None:
        _compliance_rulesets = load_all_compliance_rulesets()
    return _compliance_rulesets


def get_jurisdiction_resolver(
    rulesets: dict[str, ComplianceRuleset] = Depends(get_compliance_rulesets),
) -> JurisdictionResolver:

    return JurisdictionResolver(rulesets)


def get_lead_compliance_ruleset_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
    jurisdiction_resolver: JurisdictionResolver = Depends(get_jurisdiction_resolver),
) -> GetLeadComplianceRulesetHandler:

    return GetLeadComplianceRulesetHandler(
        unit_of_work=uow,
        jurisdiction_resolver=jurisdiction_resolver,
    )


def get_list_compliance_rulesets_handler(
    rulesets: dict[str, ComplianceRuleset] = Depends(get_compliance_rulesets),
) -> ListComplianceRulesetsHandler:

    return ListComplianceRulesetsHandler(rulesets)


GetLeadComplianceRulesetHandlerDependency = Annotated[
    GetLeadComplianceRulesetHandler,
    Depends(get_lead_compliance_ruleset_handler),
]

ListComplianceRulesetsHandlerDependency = Annotated[
    ListComplianceRulesetsHandler,
    Depends(get_list_compliance_rulesets_handler),
]


# -------------------------
# Outcome (EPIC-12)
# -------------------------


def get_create_outcome_event_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateOutcomeEventHandler:

    return CreateOutcomeEventHandler(unit_of_work=uow)


def get_delete_outcome_event_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> DeleteOutcomeEventHandler:

    return DeleteOutcomeEventHandler(unit_of_work=uow)


def get_list_outcome_events_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListOutcomeEventsHandler:

    return ListOutcomeEventsHandler(unit_of_work=uow)


CreateOutcomeEventHandlerDependency = Annotated[
    CreateOutcomeEventHandler,
    Depends(get_create_outcome_event_handler),
]

DeleteOutcomeEventHandlerDependency = Annotated[
    DeleteOutcomeEventHandler,
    Depends(get_delete_outcome_event_handler),
]

ListOutcomeEventsHandlerDependency = Annotated[
    ListOutcomeEventsHandler,
    Depends(get_list_outcome_events_handler),
]


# -------------------------
# Sequence (EPIC-09.1)
# -------------------------


def get_create_sequence_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateSequenceHandler:

    return CreateSequenceHandler(unit_of_work=uow)


def get_start_sequence_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> StartSequenceHandler:

    return StartSequenceHandler(unit_of_work=uow)


def get_advance_sequence_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> AdvanceSequenceHandler:

    return AdvanceSequenceHandler(unit_of_work=uow)


def get_record_sequence_reply_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RecordSequenceReplyHandler:

    return RecordSequenceReplyHandler(unit_of_work=uow)


def get_record_sequence_bounce_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> RecordSequenceBounceHandler:

    return RecordSequenceBounceHandler(unit_of_work=uow)


def get_sequence_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetSequenceHandler:

    return GetSequenceHandler(unit_of_work=uow)


def get_list_sequences_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListSequencesHandler:

    return ListSequencesHandler(unit_of_work=uow)


CreateSequenceHandlerDependency = Annotated[
    CreateSequenceHandler,
    Depends(get_create_sequence_handler),
]

StartSequenceHandlerDependency = Annotated[
    StartSequenceHandler,
    Depends(get_start_sequence_handler),
]

AdvanceSequenceHandlerDependency = Annotated[
    AdvanceSequenceHandler,
    Depends(get_advance_sequence_handler),
]

RecordSequenceReplyHandlerDependency = Annotated[
    RecordSequenceReplyHandler,
    Depends(get_record_sequence_reply_handler),
]

RecordSequenceBounceHandlerDependency = Annotated[
    RecordSequenceBounceHandler,
    Depends(get_record_sequence_bounce_handler),
]

GetSequenceHandlerDependency = Annotated[
    GetSequenceHandler,
    Depends(get_sequence_handler),
]

ListSequencesHandlerDependency = Annotated[
    ListSequencesHandler,
    Depends(get_list_sequences_handler),
]
