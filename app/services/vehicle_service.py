from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle


def search_vehicles(
    db: Session,
    organization_id: int,
    brand: str | None = None,
    model: str | None = None,
    year_min: int | None = None,
    price_max: float | None = None,
):
    query = db.query(Vehicle).filter(
        Vehicle.organization_id == organization_id,
        Vehicle.status == 'available',
    )

    if brand:
        query = query.filter(Vehicle.brand.ilike(f'%{brand}%'))
    if model:
        query = query.filter(Vehicle.model.ilike(f'%{model}%'))
    if year_min:
        query = query.filter(Vehicle.year >= year_min)
    if price_max:
        query = query.filter(Vehicle.price <= price_max)

    return query.limit(5).all()
