"""
Enrich Company Validator

Validates the incoming LeadCandidate before
executing company intelligence.
"""

from app.application.common.operation_result import (
    OperationResult,
)

from app.lead_intelligence.schemas.lead_candidate_schema import (
    LeadCandidate,
)


class EnrichCompanyValidator:
    """
    Validates LeadCandidate.
    """

    def validate(
        self,
        request: LeadCandidate,
    ) -> OperationResult[None]:

        result = OperationResult[None]()

        if not request.company_name.strip():

            result.add_error(
                "Company name is required."
            )

        if request.website is None:

            result.add_error(
                "Website is required."
            )

        return result