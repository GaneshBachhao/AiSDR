"""
API handler dependencies.

Provides application handlers to FastAPI presentation layer.
"""

 
from __future__ import annotations

from typing import Annotated, Any, Callable, TypeVar

from fastapi import Depends
from pydantic import validator


from app.application.company.company_mapper import (
    CompanyMapper,
)

from app.application.company.company_validator import (
    CompanyValidator,
)

from app.application.contact.contact_validator import (
    ContactValidator,
)

from app.application.contact.contact_mapper import (
    ContactMapper,
)

from app.application.discovery.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.discovery_validator import (
    DiscoveryValidator,
)

from app.presentation.api.dependencies.persistence import (
    get_unit_of_work,
)

from app.application.company.handlers.create_company_handler import (
    CreateCompanyHandler,
)
from app.application.company.handlers.get_company_handler import (
    GetCompanyHandler,
)
from app.application.company.handlers.search_company_handler import (
    SearchCompanyHandler,
)
from app.application.company.handlers.list_company_handler import (
    ListCompanyHandler,
)
from app.application.company.handlers.update_company_handler import (
    UpdateCompanyHandler,
)
from app.application.company.handlers.delete_company_handler import (
    DeleteCompanyHandler,
)

from app.application.contact.handlers.create_contact_handler import (
    CreateContactHandler,
)
from app.application.contact.handlers.get_contact_handler import (
    GetContactHandler,
)
from app.application.contact.handlers.list_contact_handler import (
    ListContactHandler,
)
from app.application.contact.handlers.update_contact_handler import (
    UpdateContactHandler,
)
from app.application.contact.handlers.search_contact_handler import (
    SearchContactHandler,
)
from app.application.contact.handlers.delete_contact_handler import (
    DeleteContactHandler,
)

from app.application.lead.handlers.create_lead_handler import (
    CreateLeadHandler,
)
from app.application.lead.handlers.get_lead_handler import (
    GetLeadHandler,
)
from app.application.lead.handlers.list_lead_handler import (
    ListLeadHandler,
)
from app.application.lead.handlers.search_lead_handler import (
    SearchLeadHandler,
)
from app.application.lead.handlers.update_lead_handler import (
    UpdateLeadHandler,
)
from app.application.lead.handlers.delete_lead_handler import (
    DeleteLeadHandler,
)

from app.application.assessment.handlers.create_assessment_handler import (
    CreateAssessmentHandler,
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
from app.application.assessment.handlers.delete_assessment_handler import (
    DeleteAssessmentHandler,
)

from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)

from app.application.qualification.handlers.create_qualification_handler import (
    CreateQualificationHandler,
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
from app.application.qualification.handlers.delete_qualification_handler import (
    DeleteQualificationHandler,
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

from app.application.discovery.handlers.create_discovery_handler import (
    CreateDiscoveryHandler,
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

from app.application.discovery.handlers.delete_discovery_handler import (
    DeleteDiscoveryHandler,
)

from app.application.qualification.qualification_commands import (
    CreateQualificationCommand,
    UpdateQualificationCommand,
    DeleteQualificationCommand,
)
from app.application.qualification.qualification_queries import (
    GetQualificationQuery,
    ListQualificationsQuery,
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

def get_create_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CreateRecommendationHandler:
    return CreateRecommendationHandler(unit_of_work=uow)


def get_get_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> GetRecommendationHandler:
    return GetRecommendationHandler(unit_of_work=uow)


def get_list_recommendation_handler(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> ListRecommendationHandler:
    return ListRecommendationHandler(unit_of_work=uow)


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
