from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.executor import executor
from app.core.security import verify_webhook_secret
from app.services.message_processor import MessageProcessor

router = APIRouter(tags=["message"])


class MessageRequest(BaseModel):
    phone: str = Field(..., examples=["5492216699450"])
    message: str
    execution_id: str


@router.post("/message", dependencies=[Depends(verify_webhook_secret)])
def receive_message(payload: MessageRequest):
    executor.submit(MessageProcessor().run_agencia, payload.phone, payload.message, payload.execution_id)
    return {"status": "accepted", "queued": True}
