from __future__ import annotations

from app.integrations.kapso_client import KapsoClient
from app.storage.checklist_store import record_checklist_event


class Tools:
    def __init__(self):
        self.kapso = KapsoClient()

    def vehiculos_db(self, action: str, **kwargs):
        if action == "get_en_stock":
            return self.kapso.get_vehiculos_en_stock(query=kwargs.get("query"))
        if action == "get_by_estado":
            return self.kapso.get_vehiculos_by_estado(kwargs["estado"])
        return {"error": f"Unsupported vehiculos_db action: {action}"}

    def checklist_docs(self, action: str, **kwargs):
        if action == "crear":
            payload = self.kapso.create_checklist(kwargs)
            vehicle_ref = str(kwargs.get("vehicle_id") or kwargs.get("vehicle_ref") or "unknown")
            record_checklist_event(vehicle_ref, "created")
            return payload
        return {"note": "checklist_docs stub; adapt to your Kapso DB API"}

    def tareas_db(self, action: str, **kwargs):
        if action == "crear":
            return self.kapso.create_tarea(kwargs)
        return {"note": "tareas_db stub; adapt to your Kapso DB API"}

    def transferencias_db(self, action: str, **kwargs):
        if action == "iniciar":
            return self.kapso.create_transferencia(kwargs)
        return {"note": "transferencias_db stub; adapt to your Kapso DB API"}

    def clientes_db(self, action: str, **kwargs):
        if action == "get_all":
            return self.kapso.get_clientes()
        return {"note": "clientes_db stub; adapt to your Kapso DB API"}

    def contabilidad_db(self, action: str, **kwargs):
        return {"note": f"contabilidad_db stub for action={action}"}

    def prestamos_db(self, action: str, **kwargs):
        return {"note": f"prestamos_db stub for action={action}"}

    def visitas_db(self, action: str, **kwargs):
        return {"note": f"visitas_db stub for action={action}"}

    def ofertas_db(self, action: str, **kwargs):
        return {"note": f"ofertas_db stub for action={action}"}

    def tramites_automotor(self, action: str, **kwargs):
        return {"note": f"tramites_automotor stub for action={action}"}

    def gmail(self, action: str, **kwargs):
        return {"note": f"gmail stub for action={action}"}

    def notas(self, action: str, **kwargs):
        return {"note": f"notas stub for action={action}"}

    def cron_jobs(self, action: str, **kwargs):
        return {"note": f"cron_jobs stub for action={action}"}

    def web_search(self, query: str):
        return {"note": "web_search stub. Plug Serper here.", "query": query}
