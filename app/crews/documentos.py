from app.crews.base import BaseCrewRunner, CrewResult


class DocumentosCrewRunner(BaseCrewRunner):
    route_name = "documentos"
    model = "claude-3-5-haiku-latest"
    goal = "Gestionar checklists de papeles. Actualizar según respuesta del usuario."
    backstory = (
        "IDs válidos: formulario_08, cedula_titular, titulo, informe_dominio, verificacion_policial, libre_deudas."
    )

    def fallback(self, message: str, context=None) -> CrewResult:
        return CrewResult(route=self.route_name, message="Tomé nota de la documentación. Si me decís el vehículo, te devuelvo el checklist actualizado.")
