from app.crews.base import BaseCrewRunner, CrewResult
from app.core.config import settings


class ResearchCrewRunner(BaseCrewRunner):
    route_name = "research"
    model = "claude-3-5-haiku-latest"
    goal = "Buscar información externa en internet."
    backstory = "Buscar en español y resumir en máximo 5 líneas con fuente."

    def fallback(self, message: str, context=None) -> CrewResult:
        if not settings.SERPER_API_KEY:
            return CrewResult(route=self.route_name, message="La búsqueda web no está habilitada porque falta SERPER_API_KEY.")
        result = self.tools.web_search(message)
        return CrewResult(route=self.route_name, message=f"Resultado de investigación: {result}")
