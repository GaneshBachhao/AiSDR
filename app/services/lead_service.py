
from typing import List

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    DuplicateLeadException,
    LeadNotFoundException,
)

from app.leads.enums.lead_status import (
    LeadStatus,
)

from app.models.lead import Lead

from app.repositories.lead_repository import (
    LeadRepository,
)

from app.schemas.common_schema import (
    PaginatedResponse,
)

from app.schemas.lead_schema import (
    LeadCreate,
    LeadUpdate,
)


class LeadService:
    """
    Business service for Lead lifecycle.

    Exposes both CRUD operations and
    business-oriented status transitions.
    """

    def __init__(self):

        self.repository = LeadRepository()

    # ======================================================
    # Create
    # ======================================================

    def create_lead(
        self,
        db: Session,
        lead: LeadCreate,
    ) -> Lead:
        """
        Create a new lead after validating
        business rules.
        """

        if lead.email:

            existing_email = (
                self.repository.get_by_email(
                    db,
                    lead.email,
                )
            )

            if existing_email:

                raise DuplicateLeadException(
                    f"Email '{lead.email}'"
                )

        existing_company = (
            self.repository.get_by_company_name(
                db,
                lead.company_name,
            )
        )

        if existing_company:

            raise DuplicateLeadException(
                f"Company '{lead.company_name}'"
            )

        return self.repository.create(
            db,
            lead,
        )

    # ======================================================
    # Read
    # ======================================================

    def get_all_leads(
        self,
        db: Session,
    ) -> List[Lead]:

        return self.repository.get_all(
            db,
        )

    def get_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        lead = self.repository.get_by_id(
            db,
            lead_id,
        )

        if not lead:

            raise LeadNotFoundException(
                lead_id,
            )

        return lead

    # ======================================================
    # Update
    # ======================================================

    def update_lead(
        self,
        db: Session,
        lead: Lead,
        updates: LeadUpdate,
    ) -> Lead:

        return self.repository.update(
            db,
            lead,
            updates,
        )

    # ======================================================
    # Business Status Updates
    # ======================================================

    def _update_status(
        self,
        db: Session,
        lead_id: int,
        status: LeadStatus,
    ) -> Lead:
        """
        Internal helper for updating
        lead status.
        """

        lead = self.get_lead(
            db,
            lead_id,
        )

        return self.update_lead(
            db,
            lead,
            LeadUpdate(
                status=status,
            ),
        )

    def qualify(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.QUALIFIED,
        )

    def mark_contacted(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.CONTACTED,
        )

    def schedule_meeting(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.MEETING_SCHEDULED,
        )

    def mark_proposal_sent(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.PROPOSAL_SENT,
        )

    def mark_negotiation(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.NEGOTIATION,
        )

    def mark_won(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.WON,
        )

    def mark_lost(
        self,
        db: Session,
        lead_id: int,
    ) -> Lead:

        return self._update_status(
            db,
            lead_id,
            LeadStatus.LOST,
        )

    # ======================================================
    # Delete
    # ======================================================

    def delete_lead(
        self,
        db: Session,
        lead: Lead,
    ) -> None:

        self.repository.delete(
            db,
            lead,
        )

    # ======================================================
    # Pagination
    # ======================================================

    def get_paginated_leads(
        self,
        db: Session,
        page: int,
        size: int,
    ):

        leads = self.repository.get_paginated(
            db,
            page,
            size,
        )

        total_records = (
            self.repository.count(
                db,
            )
        )

        return PaginatedResponse.create(
            items=leads,
            page=page,
            size=size,
            total_records=total_records,
        )

    # ======================================================
    # Search
    # ======================================================

    def search_leads(
        self,
        db: Session,
        search: str,
        page: int,
        size: int,
    ):

        leads = self.repository.search(
            db,
            search,
            page,
            size,
        )

        total_records = (
            self.repository.search_count(
                db,
                search,
            )
        )

        return PaginatedResponse.create(
            items=leads,
            page=page,
            size=size,
            total_records=total_records,
        )
