"""
Discover Companies Validator

Validates the incoming DiscoveryRequest before
executing the discovery use case.
"""

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
)

from app.application.common.operation_result import (
    OperationResult,
)


class DiscoverCompaniesValidator:
    """
    Validates DiscoveryRequest.
    """

    def validate(
        self,
        request: DiscoveryRequest,
    ) -> OperationResult[None]:
        """
        Validate discovery request.
        """

        result = OperationResult[None](success=True)

        if not request.industry.strip():

            result.add_error(
                "Industry is required."
            )

        if not request.location.strip():

            result.add_error(
                "Location is required."
            )

        if request.max_results < 1:

            result.add_error(
                "max_results must be greater than zero."
            )

        if request.max_results > 100:

            result.add_error(
                "max_results cannot exceed 100."
            )

        return result