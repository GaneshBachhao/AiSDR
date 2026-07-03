from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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


@router.post("", response_model=LeadResponse, status_code=201)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):
    return service.create_lead(db, lead)


@router.get("", response_model=List[LeadResponse])
def get_all_leads(
    db: Session = Depends(get_db)
):
    return service.get_all_leads(db)


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = service.get_lead(db, lead_id)

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    updates: LeadUpdate,
    db: Session = Depends(get_db)
):
    lead = service.get_lead(db, lead_id)

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return service.update_lead(db, lead, updates)


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = service.get_lead(db, lead_id)

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    service.delete_lead(db, lead)

    return {
        "message": "Lead deleted successfully"
    }