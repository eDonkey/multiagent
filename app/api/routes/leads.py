from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadCreate

router = APIRouter(prefix='/api/v1/leads', tags=['leads'])


@router.post('')
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get('')
def list_leads(organization_id: int, db: Session = Depends(get_db)):
    return db.query(Lead).filter(Lead.organization_id == organization_id).all()
