"""
Contact Discovery Stage

Loads contacts associated with the lead
and selects the primary contact.
"""

from app.contacts.services.contact_service import (
    ContactService,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.base_stage import (
    BasePipelineStage,
)


class ContactDiscoveryStage(BasePipelineStage):
    """
    Loads contacts for a Lead.
    """

    stage_name = "Contact Discovery"

    def __init__(self):

        self.contact_service = ContactService()

    # ======================================================
    # Can Execute
    # ======================================================

    def can_execute(
        self,
        context: PipelineContext,
    ) -> bool:

        return (
            context.db is not None
            and context.lead is not None
        )

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        contacts = self.contact_service.list_by_lead(
            context.db,
            context.lead.id,
        )

        context.contacts = contacts

        context.primary_contact = (
            self.contact_service.get_primary(
                context.db,
                context.lead.id,
            )
        )

        if context.primary_contact is None:

            context.warnings.append(
                "No primary contact found."
            )

        context.stage_results[
            self.stage_name
        ] = {

            "contacts_found": len(
                contacts,
            ),

            "primary_contact": (
                context.primary_contact.email
                if context.primary_contact
                else None
            ),
        }

        return context