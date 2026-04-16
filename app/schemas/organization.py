from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str
    slug: str
    whatsapp_phone_number: str | None = None
    active: bool = True
