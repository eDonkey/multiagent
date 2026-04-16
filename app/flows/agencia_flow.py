from __future__ import annotations

from dataclasses import dataclass

from app.crews.documentos import DocumentosCrewRunner
from app.crews.email import EmailCrewRunner
from app.crews.finanzas import FinanzasCrewRunner
from app.crews.research import ResearchCrewRunner
from app.crews.stock import StockCrewRunner
from app.crews.tareas import TareasCrewRunner
from app.crews.transferencia import TransferenciaCrewRunner
from app.services.classifier import classify_message
from app.storage.checklist_store import get_pending_events


@dataclass
class FlowResult:
    route: str
    message: str
    follow_up_message: str | None = None


class AgenciaFlow:
    def __init__(self) -> None:
        self.runners = {
            "stock": StockCrewRunner(),
            "completa": StockCrewRunner(),
            "transferencia": TransferenciaCrewRunner(),
            "tareas": TareasCrewRunner(),
            "email": EmailCrewRunner(),
            "documentos": DocumentosCrewRunner(),
            "finanzas": FinanzasCrewRunner(),
            "research": ResearchCrewRunner(),
        }

    def welcome_message(self) -> str:
        return "Hola. Puedo ayudarte con stock, tareas, documentación, transferencias, finanzas, emails y búsquedas web."

    def run(self, phone: str, message: str, context: list[dict[str, str]], has_transfer_in_progress: bool = False) -> FlowResult:
        route = classify_message(message, has_transfer_in_progress=has_transfer_in_progress)

        if route == "bienvenida":
            return FlowResult(route=route, message=self.welcome_message())

        runner = self.runners[route]
        result = runner.run(message, context)

        follow_up = None
        if route in {"stock", "completa"} and get_pending_events():
            docs_result = DocumentosCrewRunner().run("Informame el estado del checklist recién creado.", context=context)
            follow_up = docs_result.message

        return FlowResult(route=route, message=result.message, follow_up_message=follow_up)
