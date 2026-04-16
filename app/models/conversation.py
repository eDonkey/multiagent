from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey('leads.id'), nullable=True)

    channel: Mapped[str] = mapped_column(String(30), default='whatsapp')
    customer_phone: Mapped[str] = mapped_column(String(40), index=True)
    current_agent_type: Mapped[str] = mapped_column(String(30), default='seller')
    status: Mapped[str] = mapped_column(String(30), default='open')
