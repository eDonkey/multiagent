from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any


class JsonStorage:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def read(self) -> Any:
        with self._lock:
            raw = self.path.read_text(encoding="utf-8").strip() or "{}"
            return json.loads(raw)

    def write(self, payload: Any) -> None:
        with self._lock:
            self.path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
