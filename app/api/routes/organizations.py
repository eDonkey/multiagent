from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.organization import Organization
from app.models.agent import Agent
from app.schemas.organization import OrganizationCreate

router = APIRouter(prefix='/api/v1/organizations', tags=['organizations'])


@router.post('')
def create_organization(payload: OrganizationCreate, db: Session = Depends(get_db)):
    existing = db.query(Organization).filter(Organization.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail='Slug already exists')

    org = Organization(**payload.model_dump())
    db.add(org)
    db.commit()
    db.refresh(org)

    db.add_all([
        Agent(organization_id=org.id, name='Vendedor AI', type='seller', active=True),
        Agent(organization_id=org.id, name='Secretaria AI', type='secretary', active=True),
    ])
    db.commit()
    return org


@router.get('')
def list_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()
