"""
AI Email Generation Stage

Generates a personalized outreach email
using Gemini.
"""

from app.ai.services.email_generation_service import (
    EmailGenerationService,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class AIEmailGenerationStage(BasePipelineStage):
    """
    Generates an AI email.
    """

    stage_name = "AI Email Generation"

    def __init__(self):

        self.service = EmailGenerationService()

    # ======================================================
    # Can Execute
    # ======================================================

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        return (

            context.company_profile is not None

            and

            context.primary_contact is not None

            and

            context.recommendations is not None

        )

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        generated = self.service.generate(

            company=context.company_profile,

            contact=context.primary_contact,

            recommendations=context.recommendations,

        )

        context.generated_email = generated

        context.stage_results[
            self.stage_name
        ] = {

            "subject": generated.subject,

            "body_length": len(
                generated.body,
            ),
        }

        return context