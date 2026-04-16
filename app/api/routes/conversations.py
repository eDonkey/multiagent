from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.conversation import Conversation
from app.models.message import Message

router = APIRouter(prefix='/api/v1/conversations', tags=['conversations'])


@router.get('')
def list_conversations(organization_id: int, db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.organization_id == organization_id).all()


@router.get('/{conversation_id}/messages')
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()


@router.post('/{conversation_id}/handoff')
def handoff_to_human(conversation_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')

    conv.status = 'waiting_human'
    conv.current_agent_type = 'human'
    db.commit()
    db.refresh(conv)
    return conv
