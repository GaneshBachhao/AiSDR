"""
Enrich Company Handler

Coordinates validation, mapping and execution of
the Company Intelligence Service.
"""

from app.application.common.operation_result import (
    OperationResult,
)

from app.application.company_intelligence.commands.enrich_company import (
    EnrichCompanyCommand,
)

from app.application.company_intelligence.dto.enrich_company_response_dto import (
    EnrichCompanyResponseDTO,
)

from app.application.company_intelligence.mappers.company_profile_mapper import (
    CompanyProfileMapper,
)

from app.application.company_intelligence.validators.enrich_company_validator import (
    EnrichCompanyValidator,
)

from app.company_intelligence.services.company_intelligence_service import (
    CompanyIntelligenceService,
)

from app.core.logger import logger


class EnrichCompanyHandler:
    """
    Handles company enrichment requests.
    """

    def __init__(
        self,
        company_service: CompanyIntelligenceService | None = None,
        validator: EnrichCompanyValidator | None = None,
    ) -> None:

        self.company_service = (
            company_service
            if company_service is not None
            else CompanyIntelligenceService()
        )

        self.validator = (
            validator
            if validator is not None
            else EnrichCompanyValidator()
        )

    def handle(
        self,
        command: EnrichCompanyCommand,
    ) -> OperationResult[
        EnrichCompanyResponseDTO
    ]:
        """
        Execute company enrichment.
        """

        validation = self.validator.validate(
            command,
        )

        if not validation.success:

            return OperationResult.fail(

                message=(
                    "Company enrichment validation failed."
                ),

                errors=validation.errors,
            )

        try:

            request = (
                CompanyProfileMapper.command_to_dto(
                    command,
                )
            )

            candidate = (
                CompanyProfileMapper.dto_to_candidate(
                    request,
                )
            )

            profile = (
                self.company_service.enrich(
                    candidate,
                )
            )

            response = (
                CompanyProfileMapper.profile_to_response(
                    profile,
                )
            )

            logger.info(

                "Company enrichment completed: %s",

                response.company_name,
            )

            return OperationResult.ok(

                data=response,

                message=(
                    "Company enriched successfully."
                ),
            )

        except Exception as ex:

            logger.exception(
                "Company enrichment failed."
            )

            return OperationResult.fail(

                message=(
                    "Company enrichment failed."
                ),

                errors=[str(ex)],
            )