from sqlalchemy.orm import Session
from app.models.lead import Lead


def get_or_create_lead(db: Session, organization_id: int, phone: str) -> Lead:
    lead = (
        db.query(Lead)
        .filter(Lead.organization_id == organization_id, Lead.phone == phone)
        .first()
    )
    if lead:
        return lead

    lead = Lead(
        organization_id=organization_id,
        phone=phone,
        source='whatsapp',
        status='new',
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
