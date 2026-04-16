from app.crews.base import BaseCrewRunner, CrewResult


class StockCrewRunner(BaseCrewRunner):
    route_name = "stock"
    model = "claude-3-5-haiku-latest"
    goal = "Registrar y gestionar vehículos, visitas, ofertas y ventas."
    backstory = (
        "AL ENTRAR EN STOCK: checklist_docs(crear) + tarea lavado + tarea fotos + tarea publicación. "
        "Consultas por estado: vehiculos_db(get_by_estado). Nunca pedir un ID al usuario. "
        "Nunca expliques lo que vas a hacer antes de hacerlo."
    )

    def fallback(self, message: str, context=None) -> CrewResult:
        stock = self.tools.vehiculos_db("get_en_stock", query=message)
        items = stock.get("items") or stock.get("results") or []
        if items:
            lines = []
            for item in items[:3]:
                brand = item.get("marca") or item.get("brand") or ""
                model = item.get("modelo") or item.get("model") or ""
                year = item.get("anio") or item.get("year") or ""
                price = item.get("precio") or item.get("price") or "Consultar"
                lines.append(f"- {brand} {model} {year} · {price}")
            msg = "Encontré estas opciones en stock:\n" + "\n".join(lines)
        else:
            msg = "No encontré coincidencias exactas en stock. Si querés, decime marca, modelo o patente y lo reviso."
        return CrewResult(route=self.route_name, message=msg, raw=stock)
