from typing import List
from typing import Optional 

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from app.tasks.research_task import research_lead_task
from app.common.response import ApiResponse
from sqlalchemy.orm import Session
from fastapi import Query 
from app.database.database import get_db
from app.schemas.lead_schema import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
)
from app.services.lead_service import LeadService

router = APIRouter(
    prefix="/api/v1/leads",
    tags=["Leads"]
)

service = LeadService()


@router.post("", status_code=201)
def create_lead(
    lead: LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    created = service.create_lead(
        db,
        lead
    )

    background_tasks.add_task(
        research_lead_task,
        created.id
    )

    return ApiResponse.success(
        data=created,
        message="Lead created successfully. Background research started."
    )


@router.get("")
def get_all_leads(
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if search:
        result = service.search_leads(
            db,
            search,
            page,
            size
        )
    else:
        result = service.get_paginated_leads(
            db,
            page,
            size
        )

    return ApiResponse.success(
        data=result,
        message="Leads retrieved successfully"
    )


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    return service.get_lead(db, lead_id)


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    updates: LeadUpdate,
    db: Session = Depends(get_db)
):
    lead = service.get_lead(db, lead_id)
    return service.update_lead(db, lead, updates)


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = service.get_lead(db, lead_id)

    service.delete_lead(db, lead)

    return {
        "message": "Lead deleted successfully"
    }