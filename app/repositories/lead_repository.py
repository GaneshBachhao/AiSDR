from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.schemas.lead_schema import LeadCreate, LeadUpdate


class LeadRepository:

    def create(self, db: Session, lead: LeadCreate) -> Lead:
        db_lead = Lead(**lead.model_dump())

        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

        return db_lead

    def get_all(self, db: Session) -> List[Lead]:
        return db.query(Lead).all()

    def get_by_id(self, db: Session, lead_id: int) -> Optional[Lead]:
        return db.query(Lead).filter(Lead.id == lead_id).first()

    def update(
        self,
        db: Session,
        lead: Lead,
        updates: LeadUpdate
    ) -> Lead:

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(lead, key, value)

        db.commit()
        db.refresh(lead)

        return lead

    def delete(self, db: Session, lead: Lead) -> None:
        db.delete(lead)
        db.commit()