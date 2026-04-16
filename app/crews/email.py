from app.crews.base import BaseCrewRunner, CrewResult


class EmailCrewRunner(BaseCrewRunner):
    route_name = "email"
    model = "claude-3-5-haiku-latest"
    goal = "Enviar emails a clientes y proveedores. Notificar equipo. Leer respuestas."
    backstory = (
        "Internos: solo a rena y fran. Asunto IMPORTANTE: [tema]. "
        "Externos: buscar email en clientes_db antes de enviar."
    )

    def fallback(self, message: str, context=None) -> CrewResult:
        return CrewResult(route=self.route_name, message="Necesito el destinatario o el cliente para buscar el email antes de enviarlo.")
