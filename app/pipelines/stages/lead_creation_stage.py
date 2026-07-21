"""
Lead Creation Pipeline Stage

Creates a Lead from a qualified company.
"""

from datetime import UTC, datetime

from app.core.logger import logger

from app.exceptions.custom_exceptions import (
    DuplicateLeadException,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)

from app.schemas.lead_schema import (
    LeadCreate,
)

from app.services.lead_service import (
    LeadService,
)


class LeadCreationStage(BasePipelineStage):
    """
    Creates a Lead for qualified companies.
    """

    @property
    def stage_name(self) -> str:
        return "Lead Creation"

    def __init__(
        self,
        lead_service: LeadService | None = None,
    ):

        self.lead_service = (
            lead_service
            if lead_service is not None
            else LeadService()
        )

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        if context.company_profile is None:

            reason = "Company profile missing"

        elif context.qualification is None:

            reason = "Qualification missing"

        elif not context.qualification.qualified:

            reason = "Company not qualified"

        else:

            return True

        context.stage_results[self.stage_name] = {

            "status": "SKIPPED",

            "reason": reason,

        }

        logger.info(
            f"[{context.execution_id}] "
            f"Skipping {self.stage_name}: {reason}"
        )

        return False

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        if context.db is None:

            raise ValueError(
                "PipelineContext.db is required."
            )

        if context.company_profile is None:

            raise ValueError(
                "PipelineContext.company_profile is required."
            )

        logger.info(
            f"[{context.execution_id}] "
            f"Creating Lead: "
            f"{context.company_profile.company_name}"
        )

        try:

            lead = LeadCreate(

                company_name=context.company_profile.company_name,

                website=context.company_profile.website,

            )

            created = self.lead_service.create_lead(

                db=context.db,

                lead=lead,

            )

            context.lead = created

            context.stage_results[self.stage_name] = {

                "status": "SUCCESS",

                "company_name": created.company_name,

                "website": created.website,

                "lead_id": created.id,

                "qualified": (
                    context.qualification.qualified
                    if context.qualification
                    else None
                ),

                "qualification_score": (
                    context.qualification.score
                    if context.qualification
                    else None
                ),

                "completed_at": datetime.now(UTC),

            }

            logger.info(
                f"[{context.execution_id}] "
                f"Lead Created: "
                f"{created.company_name}"
            )

        except DuplicateLeadException:

            warning = (
                f"Lead already exists: "
                f"{context.company_profile.company_name}"
            )

            logger.info(
                f"[{context.execution_id}] "
                f"{warning}"
            )

            context.warnings.append(
                warning
            )

            context.stage_results[self.stage_name] = {

                "status": "WARNING",

                "reason": "Duplicate Lead",

                "company_name": (
                    context.company_profile.company_name
                ),

                "completed_at": datetime.now(UTC),

            }

        except Exception as ex:

            logger.exception(
                f"[{context.execution_id}] "
                "Lead Creation Failed"
            )

            context.errors.append(
                str(ex)
            )

            context.stage_results[self.stage_name] = {

                "status": "FAILED",

                "reason": str(ex),

                "company_name": (
                    context.company_profile.company_name
                ),

                "completed_at": datetime.now(UTC),

            }

            raise

        return context