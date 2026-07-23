from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.prompts.general import HELLO_PROMPT
from app.ai.services.ai_service import AIService

from app.database.database import get_db
from app.services.research_service import ResearchService


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI"]
)

service = AIService()
research_service = ResearchService()


@router.get("/hello")
def hello():

    result = service.generate(
        HELLO_PROMPT
    )

    return {
        "response": result
    }


@router.post("/research/{lead_id}")
def research_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """
    Research a lead by Lead ID and save the result.
    """

    try:

        research = research_service.research_lead(
            db=db,
            lead_id=lead_id
        )

        return research

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )