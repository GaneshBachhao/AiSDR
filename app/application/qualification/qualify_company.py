"""
Qualify Company Use Case

Application use case responsible for qualifying a company
against the Ideal Customer Profile (ICP).
"""

from app.application.common.operation_result import (
    OperationResult,
)
from app.application.common.use_case import (
    UseCase,
)
from app.company_intelligence.schemas.company_profile_schema import (
    CompanyProfile,
)
from app.core.logger import logger
from app.lead_intelligence.qualification.schemas.qualification_result_schema import (
    QualificationResult,
)
from app.lead_intelligence.qualification.services.qualification_service import (
    QualificationService,
)


class QualifyCompany(
    UseCase[
        CompanyProfile,
        QualificationResult,
    ]
):
    """
    Qualify a company against the ICP.
    """

    def __init__(
        self,
        qualification_service: QualificationService | None = None,
    ) -> None:

        self.qualification_service = (
            qualification_service
            if qualification_service is not None
            else QualificationService()
        )

    def execute(
        self,
        request: CompanyProfile,
    ) -> OperationResult[
        QualificationResult
    ]:

        logger.info(
            "Qualifying company: %s",
            request.company_name,
        )

        try:

            result = (
                self.qualification_service.qualify(
                    request,
                )
            )

            logger.info(
                "Qualification completed | "
                "Qualified=%s | Score=%s",
                result.qualified,
                result.score,
            )

            return OperationResult.ok(
                data=result,
                message="Company qualification completed.",
            )

        except Exception as ex:

            logger.exception(
                "Company qualification failed."
            )

            return OperationResult.fail(
                message="Company qualification failed.",
                errors=[str(ex)],
            )