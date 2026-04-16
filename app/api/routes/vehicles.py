from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate

router = APIRouter(prefix='/api/v1/vehicles', tags=['vehicles'])


@router.post('')
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get('')
def list_vehicles(organization_id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.organization_id == organization_id).all()
