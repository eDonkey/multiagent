from pydantic import BaseModel


class LeadCreate(BaseModel):
    organization_id: int
    full_name: str | None = None
    phone: str
    email: str | None = None
    source: str = 'whatsapp'
    status: str = 'new'
    interest_notes: str | None = None
