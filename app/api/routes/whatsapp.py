import json
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.models.organization import Organization
from app.services.agent_router import detect_agent_type
from app.services.lead_service import get_or_create_lead
from app.services.conversation_service import get_or_create_conversation, add_message
from app.services.seller_agent import build_seller_response
from app.services.secretary_agent import build_secretary_response
from app.services.whatsapp_service import send_whatsapp_text

router = APIRouter(prefix='/api/v1/webhooks/whatsapp', tags=['whatsapp'])


@router.get('')
def verify_whatsapp_webhook(
    hub_mode: str = Query(alias='hub.mode'),
    hub_verify_token: str = Query(alias='hub.verify_token'),
    hub_challenge: str = Query(alias='hub.challenge'),
):
    if hub_mode == 'subscribe' and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail='Invalid verify token')


@router.post('')
async def receive_whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    try:
        entry = payload['entry'][0]
        change = entry['changes'][0]
        value = change['value']
        metadata = value['metadata']
        phone_number_id = metadata['phone_number_id']

        message = value['messages'][0]
        customer_phone = message['from']
        text = message['text']['body']
    except Exception:
        return {'status': 'ignored'}

    organization = (
        db.query(Organization)
        .filter(Organization.whatsapp_phone_number == phone_number_id, Organization.active == True)
        .first()
    )

    if not organization:
        return {'status': 'organization_not_found'}

    lead = get_or_create_lead(db, organization.id, customer_phone)
    conv = get_or_create_conversation(db, organization.id, lead.id, customer_phone)

    add_message(
        db,
        conversation_id=conv.id,
        sender_type='customer',
        sender_name=customer_phone,
        message_text=text,
        raw_payload_json=json.dumps(payload),
    )

    agent_type = detect_agent_type(text)

    if agent_type == 'secretary':
        response_text = build_secretary_response()
    else:
        response_text = build_seller_response(db, organization.id, text)

    add_message(
        db,
        conversation_id=conv.id,
        sender_type='agent',
        sender_name=agent_type,
        message_text=response_text,
    )

    send_whatsapp_text(customer_phone, response_text)

    return {'status': 'ok'}
