from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversations.id'), index=True)

    sender_type: Mapped[str] = mapped_column(String(20))
    sender_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    raw_payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
