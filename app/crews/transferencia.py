from app.crews.base import BaseCrewRunner, CrewResult


class TransferenciaCrewRunner(BaseCrewRunner):
    route_name = "transferencia"
    model = "claude-3-5-sonnet-latest"
    goal = "Gestionar el proceso completo de transferencia de dominio vehicular."
    backstory = (
        "Flujo: identificar vehículo, identificar comprador, pedir datos faltantes, iniciar transferencia, "
        "checklist docs y actualizar docs confirmados. Prohibido: no actualizar estado del vehículo."
    )

    def fallback(self, message: str, context=None) -> CrewResult:
        return CrewResult(
            route=self.route_name,
            message="Para avanzar con la transferencia necesito: vehículo, comprador, registro, pago, precarga y turno.",
        )
