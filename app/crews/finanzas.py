from app.crews.base import BaseCrewRunner, CrewResult


class FinanzasCrewRunner(BaseCrewRunner):
    route_name = "finanzas"
    model = "claude-3-5-haiku-latest"
    goal = "Balances, movimientos y P&L por vehículo. Alertar cash bajo."
    backstory = "Cuentas: cash, nexo, fiwind. Moneda USD."

    def fallback(self, message: str, context=None) -> CrewResult:
        return CrewResult(route=self.route_name, message="Decime si querés balance, caja, movimiento, préstamo o vencimiento.")
