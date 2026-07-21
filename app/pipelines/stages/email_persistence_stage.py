"""
Email Persistence Stage

Creates an outbound email draft in the database.
"""

from app.emails.schemas.email_schema import (
    EmailCreate,
)

from app.emails.services.email_service import (
    EmailService,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class EmailPersistenceStage(BasePipelineStage):
    """
    Persists generated email as a draft.
    """

    stage_name = "Email Persistence"

    def __init__(self):

        self.service = EmailService()

    # ======================================================
    # Can Execute
    # ======================================================

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        return (

            context.db is not None

            and

            context.lead is not None

            and

            context.primary_contact is not None

            and

            context.generated_email is not None

        )

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        request = EmailCreate(

            lead_id=context.lead.id,

            contact_id=context.primary_contact.id,

            subject=context.generated_email.subject,

            body=context.generated_email.body,

        )

        email = self.service.create_draft(

            context.db,

            request,

        )

        context.email = email

        context.stage_results[
            self.stage_name
        ] = {

            "email_id": email.id,

            "subject": email.subject,

        }

        return context