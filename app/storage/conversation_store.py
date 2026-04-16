from __future__ import annotations

from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.utils.json_storage import JsonStorage

STORE = JsonStorage("storage/conversations.json")


class ConversationStore:
    def __init__(self):
        self._store = STORE

    def append(self, phone: str, role: str, content: str) -> None:
        data = self._store.read()
        record = data.get(phone, {"updated_at": None, "messages": []})

        updated_at = record.get("updated_at")
        if updated_at:
            last_dt = datetime.fromisoformat(updated_at)
            if datetime.now(timezone.utc) - last_dt > timedelta(minutes=settings.CONVERSATION_TIMEOUT_MINUTES):
                record["messages"] = []

        record["messages"].append({"role": role, "content": content})
        record["messages"] = record["messages"][-settings.CONVERSATION_WINDOW :]
        record["updated_at"] = datetime.now(timezone.utc).isoformat()
        data[phone] = record
        self._store.write(data)

    def get_recent_messages(self, phone: str, limit: int = 4, max_chars: int = 600) -> list[dict[str, str]]:
        data = self._store.read()
        record = data.get(phone, {"messages": []})
        messages = record.get("messages", [])[-limit:]
        return [
            {"role": item.get("role", "user"), "content": (item.get("content") or "")[:max_chars]}
            for item in messages
        ]
