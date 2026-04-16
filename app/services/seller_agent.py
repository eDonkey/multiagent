from sqlalchemy.orm import Session
from app.services.vehicle_service import search_vehicles


def build_seller_response(db: Session, organization_id: int, message_text: str) -> str:
    text = message_text.lower()

    brand = None
    known_brands = ['toyota', 'ford', 'volkswagen', 'chevrolet', 'fiat', 'peugeot', 'renault']
    for b in known_brands:
        if b in text:
            brand = b
            break

    vehicles = search_vehicles(db, organization_id=organization_id, brand=brand)

    if vehicles:
        lines = ['Te comparto algunas opciones disponibles:']
        for v in vehicles[:3]:
            price = f"{float(v.price):,.0f}" if v.price else 'Consultar'
            lines.append(f"- {v.brand} {v.model} {v.year} | {v.mileage} km | {v.currency} {price}")
        lines.append('Si querés, te pido algunos datos y coordinamos una visita o te paso más opciones.')
        return '\n'.join(lines)

    return (
        'Gracias por tu consulta. En este momento no encontré una unidad exacta con esos criterios. '
        'Si querés, decime marca, modelo, año aproximado y presupuesto, y te ayudo a buscar alternativas.'
    )
