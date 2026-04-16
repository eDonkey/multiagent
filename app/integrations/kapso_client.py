from __future__ import annotations

import httpx
from typing import Any
from app.core.config import settings


class KapsoClient:
    def __init__(self) -> None:
        self.base_url = settings.KAPSO_DB_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.KAPSO_API_KEY}",
            "Content-Type": "application/json",
        }

    def request(self, method: str, path: str, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        with httpx.Client(timeout=30) as client:
            response = client.request(method, url, json=json, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json() if response.text else {}

    def health(self) -> dict[str, Any]:
        return {"kapso_db_url": self.base_url}

    def get_vehiculos_en_stock(self, query: str | None = None) -> dict[str, Any]:
        params = {"query": query} if query else None
        return self.request("GET", "/vehiculos/en-stock", params=params)

    def get_vehiculos_by_estado(self, estado: str) -> dict[str, Any]:
        return self.request("GET", f"/vehiculos/estado/{estado}")

    def create_tarea(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/tareas", json=payload)

    def create_checklist(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/checklists", json=payload)

    def create_transferencia(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/transferencias", json=payload)

    def get_clientes(self) -> dict[str, Any]:
        return self.request("GET", "/clientes")

    def send_resume_execution(self, execution_id: str, message: str) -> dict[str, Any]:
        return self.request("POST", "/resume_execution", json={"execution_id": execution_id, "message": message})
