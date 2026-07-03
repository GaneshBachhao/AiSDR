from typing import List

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead_schema import LeadCreate, LeadUpdate


class LeadService:

    def __init__(self):
        self.repository = LeadRepository()

    def create_lead(
        self,
        db: Session,
        lead: LeadCreate
    ) -> Lead:

        # Future business rules can go here:
        # - Check duplicate email
        # - Normalize website
        # - Validate domain
        # - AI enrichment

        return self.repository.create(db, lead)

    def get_all_leads(
        self,
        db: Session
    ) -> List[Lead]:

        return self.repository.get_all(db)

    def get_lead(
        self,
        db: Session,
        lead_id: int
    ) -> Lead | None:

        return self.repository.get_by_id(db, lead_id)

    def update_lead(
        self,
        db: Session,
        lead: Lead,
        updates: LeadUpdate
    ) -> Lead:

        return self.repository.update(db, lead, updates)

    def delete_lead(
        self,
        db: Session,
        lead: Lead
    ):

        self.repository.delete(db, lead)