from pydantic import BaseModel


class VehicleCreate(BaseModel):
    organization_id: int
    brand: str
    model: str
    version: str | None = None
    year: int
    mileage: int = 0
    fuel_type: str | None = None
    transmission: str | None = None
    price: float | None = None
    currency: str = 'ARS'
    status: str = 'available'
    description: str | None = None
    photos_json: str | None = None
