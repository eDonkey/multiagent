from app.crews.base import BaseCrewRunner, CrewResult


class TareasCrewRunner(BaseCrewRunner):
    route_name = "tareas"
    model = "claude-3-5-haiku-latest"
    goal = "Crear, asignar y completar tareas. Gestionar recordatorios y notas personales."
    backstory = (
        "Tareas del negocio: usar tareas_db con tipo, prioridad, asignado y vehicle_id. "
        "Prioridades: urgente/hoy alta, normal media, cuando puedas baja. Fechas ISO."
    )

    def fallback(self, message: str, context=None) -> CrewResult:
        lowered = message.lower()
        priority = "alta" if ("urgente" in lowered or "hoy" in lowered) else "baja" if "cuando puedas" in lowered else "media"
        self.tools.tareas_db("crear", tipo="otro", prioridad=priority, detalle=message)
        return CrewResult(route=self.route_name, message=f"Listo, dejé registrada la tarea con prioridad {priority}.")
