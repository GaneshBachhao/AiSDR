from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database.database import SessionLocal
from app.services.research_service import ResearchService


def research_lead_task(lead_id: int):
    """
    Background task to research a lead.
    """

    db: Session = SessionLocal()

    try:
        logger.info("=" * 60)
        logger.info(f"Background Research Started | Lead ID: {lead_id}")

        service = ResearchService()

        service.research_lead(
            db=db,
            lead_id=lead_id
        )

        logger.info(f"Background Research Completed | Lead ID: {lead_id}")
        logger.info("=" * 60)

    except Exception as ex:

        logger.exception(
            f"Background Research Failed | Lead ID: {lead_id} | {ex}"
        )

    finally:
        db.close()