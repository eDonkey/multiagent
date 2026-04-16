from app.core.db import SessionLocal
from app.models.organization import Organization
from app.models.agent import Agent
from app.models.vehicle import Vehicle


def run():
    db = SessionLocal()

    existing = db.query(Organization).filter(Organization.slug == 'demo-motors').first()
    if existing:
        print('Seed already exists')
        db.close()
        return

    org = Organization(
        name='Demo Motors',
        slug='demo-motors',
        whatsapp_phone_number='1234567890',
        active=True,
    )
    db.add(org)
    db.commit()
    db.refresh(org)

    db.add_all([
        Agent(organization_id=org.id, name='Vendedor AI', type='seller', active=True),
        Agent(organization_id=org.id, name='Secretaria AI', type='secretary', active=True),
        Vehicle(organization_id=org.id, brand='Toyota', model='Hilux', version='SRV 4x4 AT', year=2021, mileage=45000, price=39500000, currency='ARS', status='available'),
        Vehicle(organization_id=org.id, brand='Ford', model='Ranger', version='XLT AT', year=2020, mileage=62000, price=34500000, currency='ARS', status='available'),
        Vehicle(organization_id=org.id, brand='Volkswagen', model='Amarok', version='Highline AT', year=2022, mileage=30000, price=45500000, currency='ARS', status='available'),
    ])
    db.commit()
    db.close()
    print('Seed created successfully')


if __name__ == '__main__':
    run()
