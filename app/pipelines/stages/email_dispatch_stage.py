"""
Email Dispatch Stage

Sends the persisted email using the configured
email provider and updates the email status.
"""

from app.emails.services.email_dispatch_service import (
    EmailDispatchService,
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


class EmailDispatchStage(BasePipelineStage):
    """
    Sends an email using the configured provider.
    """

    stage_name = "Email Dispatch"

    def __init__(self):

        self.dispatch_service = EmailDispatchService()

        self.email_service = EmailService()

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

            context.email is not None

            and

            context.primary_contact is not None

        )

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        db = context.db

        email = context.email

        contact = context.primary_contact

        # mark sending

        self.email_service.mark_sending(
            db,
            email,
        )

        result = self.dispatch_service.dispatch(

            db,

            email,

            contact,

        )

        context.email_send_result = result

        if result.success:

            self.email_service.mark_sent(

                db,

                email,

                result.message_id or "",

            )

        else:

            self.email_service.mark_failed(

                db,

                email,

            )

            context.errors.append(

                result.error_message
                or "Unknown email error"

            )

        context.stage_results[
            self.stage_name
        ] = {

            "success": result.success,

            "provider": result.provider,

            "message_id": result.message_id,

        }

        return context