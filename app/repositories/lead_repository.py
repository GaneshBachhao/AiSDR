"""
Lead Repository
"""

from typing import Optional

from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database.base_repository import (
    BaseRepository,
)

from app.core.database.query_builder import (
    QueryBuilder,
)

from app.models.lead import Lead
from app.schemas.lead_schema import (
    LeadCreate,
    LeadUpdate,
)


class LeadRepository(
    BaseRepository[Lead],
):
    """
    Repository responsible for Lead persistence.
    """

    def __init__(self):

        super().__init__(Lead)

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        db: Session,
        lead: LeadCreate,
    ) -> Lead:

        entity = Lead(
            **lead.model_dump()
        )

        return super().create(
            db,
            entity,
        )

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        db: Session,
        lead: Lead,
        updates: LeadUpdate,
    ) -> Lead:

        update_data = updates.model_dump(
            exclude_unset=True,
        )

        for key, value in update_data.items():

            setattr(
                lead,
                key,
                value,
            )

        return super().update(
            db,
            lead,
        )

    # =====================================================
    # Business Queries
    # =====================================================

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Optional[Lead]:

        return (
            db.query(Lead)
            .filter(
                func.lower(
                    Lead.email
                )
                == email.lower()
            )
            .first()
        )

    def get_by_company_name(
        self,
        db: Session,
        company_name: str,
    ) -> Optional[Lead]:

        return (
            db.query(Lead)
            .filter(
                func.lower(
                    Lead.company_name
                )
                == company_name.lower()
            )
            .first()
        )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        db: Session,
        search: str,
        page: int,
        size: int,
    ) -> list[Lead]:

        query = db.query(
            Lead,
        )

        query = QueryBuilder.search(
            query=query,
            search=search,
            columns=[
                Lead.company_name,
                Lead.contact_name,
                Lead.email,
                Lead.website,
            ],
        )

        query = QueryBuilder.paginate(
            query=query,
            page=page,
            size=size,
        )

        return query.all()

    def search_count(
        self,
        db: Session,
        search: str,
    ) -> int:

        return (
            db.query(Lead)
            .filter(
                or_(
                    Lead.company_name.ilike(
                        f"%{search}%"
                    ),
                    Lead.contact_name.ilike(
                        f"%{search}%"
                    ),
                    Lead.email.ilike(
                        f"%{search}%"
                    ),
                    Lead.website.ilike(
                        f"%{search}%"
                    ),
                )
            )
            .count()
        )