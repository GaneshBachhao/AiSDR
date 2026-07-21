from typing import List

from sqlalchemy.orm import Session

from app.outreach.models.outreach import Outreach
from app.outreach.schemas.outreach_schema import OutreachCreate


class OutreachRepository:
    """
    Repository for Outreach persistence.
    """

    def create(
        self,
        db: Session,
        outreach: OutreachCreate,
    ) -> Outreach:

        db_outreach = Outreach(
            **outreach.model_dump()
        )

        db.add(db_outreach)

        db.commit()

        db.refresh(db_outreach)

        return db_outreach

    def create_many(
        self,
        db: Session,
        outreach_list: List[Outreach],
    ) -> List[Outreach]:

        db.add_all(outreach_list)

        db.commit()

        for outreach in outreach_list:
            db.refresh(outreach)

        return outreach_list

    def get_by_id(
        self,
        db: Session,
        outreach_id: int,
    ) -> Outreach | None:

        return (
            db.query(Outreach)
            .filter(
                Outreach.id == outreach_id
            )
            .first()
        )

    def get_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> List[Outreach]:

        return (
            db.query(Outreach)
            .filter(
                Outreach.lead_id == lead_id
            )
            .order_by(
                Outreach.created_at.desc()
            )
            .all()
        )

    def get_latest(
        self,
        db: Session,
        lead_id: int,
    ) -> Outreach | None:

        return (
            db.query(Outreach)
            .filter(
                Outreach.lead_id == lead_id
            )
            .order_by(
                Outreach.created_at.desc()
            )
            .first()
        )

    def update_status(
        self,
        db: Session,
        outreach: Outreach,
        status: str,
    ) -> Outreach:

        outreach.status = status

        db.commit()

        db.refresh(outreach)

        return outreach