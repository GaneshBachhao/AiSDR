from typing import List

from sqlalchemy.orm import Session

from app.models.lead_research import LeadResearch
from app.schemas.lead_research_schema import LeadResearchCreate


class LeadResearchRepository:

    def create(
        self,
        db: Session,
        research: LeadResearchCreate
    ) -> LeadResearch:

        db_research = LeadResearch(**research.model_dump())

        db.add(db_research)

        db.commit()

        db.refresh(db_research)

        return db_research

    def get_by_id(
        self,
        db: Session,
        research_id: int
    ) -> LeadResearch | None:

        return (
            db.query(LeadResearch)
            .filter(LeadResearch.id == research_id)
            .first()
        )

    def get_by_lead(
        self,
        db: Session,
        lead_id: int
    ) -> List[LeadResearch]:

        return (
            db.query(LeadResearch)
            .filter(LeadResearch.lead_id == lead_id)
            .order_by(LeadResearch.created_at.desc())
            .all()
        )

    def get_latest(
        self,
        db: Session,
        lead_id: int
    ) -> LeadResearch | None:

        return (
            db.query(LeadResearch)
            .filter(LeadResearch.lead_id == lead_id)
            .order_by(LeadResearch.created_at.desc())
            .first()
        )

    def delete(
        self,
        db: Session,
        research: LeadResearch
    ):

        db.delete(research)

        db.commit()