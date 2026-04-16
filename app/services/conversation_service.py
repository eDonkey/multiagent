from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message


def get_or_create_conversation(db: Session, organization_id: int, lead_id: int | None, phone: str):
    conv = (
        db.query(Conversation)
        .filter(
            Conversation.organization_id == organization_id,
            Conversation.customer_phone == phone,
            Conversation.status == 'open',
        )
        .first()
    )
    if conv:
        return conv

    conv = Conversation(
        organization_id=organization_id,
        lead_id=lead_id,
        customer_phone=phone,
        current_agent_type='seller',
        status='open',
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def add_message(
    db: Session,
    conversation_id: int,
    sender_type: str,
    sender_name: str | None,
    message_text: str,
    raw_payload_json: str | None = None,
):
    msg = Message(
        conversation_id=conversation_id,
        sender_type=sender_type,
        sender_name=sender_name,
        message_text=message_text,
        raw_payload_json=raw_payload_json,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
