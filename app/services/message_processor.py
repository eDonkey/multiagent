from __future__ import annotations

import logging
from app.flows.agencia_flow import AgenciaFlow
from app.integrations.kapso_client import KapsoClient
from app.storage.conversation_store import ConversationStore

logger = logging.getLogger(__name__)


class MessageProcessor:
    def __init__(self) -> None:
        self.flow = AgenciaFlow()
        self.kapso = KapsoClient()
        self.conversations = ConversationStore()

    def run_agencia(self, phone: str, message: str, execution_id: str) -> None:
        self.conversations.append(phone, "user", message)
        context = self.conversations.get_recent_messages(phone)
        result = self.flow.run(phone=phone, message=message, context=context)
        self.conversations.append(phone, "assistant", result.message)

        logger.info("Resolved route=%s for phone=%s", result.route, phone)
        self.kapso.send_resume_execution(execution_id, result.message)

        if result.follow_up_message:
            self.conversations.append(phone, "assistant", result.follow_up_message)
            self.kapso.send_resume_execution(execution_id, result.follow_up_message)
