from __future__ import annotations

import re

TAREAS_INTENT_PREFIXES = ("agrega tarea", "agregá tarea", "nueva nota", "recordatorio:")
TRANSFERENCIA_KEYWORDS = ["iniciar transferencia", "transferencias activas", "ver transferencias", "transferencia"]
BIENVENIDA_KEYWORDS = ["hola", "buenas", "qué podés hacer", "que podes hacer"]
TAREAS_KEYWORDS = ["anotá", "anota", "recordatorio:", "tareas para", "no olvidar", "tarea"]
STOCK_KEYWORDS = ["en stock", "consignación", "consignacion", "el corolla", "modificar", "toyota", "ford", "volkswagen", "chevrolet", "peugeot", "renault", "fiat"]
RESEARCH_KEYWORDS = ["buscá", "busca", "googleá", "googlea", "averiguá", "averigua", "información sobre", "informacion sobre"]
EMAIL_KEYWORDS = ["mail", "email", "notificá", "notifica", "avisá al cliente", "avisa al cliente"]
DOCUMENTOS_KEYWORDS = ["cédula", "cedula", "checklist", "papeles", "tengo el", "tengo la", "formulario 08", "libre de deudas"]
FINANZAS_KEYWORDS = ["balance", "caja", "nexo", "plata", "/entra-dinero", "préstamo", "prestamo", "acreedor", "deuda", "vence", "devolver", "cuota"]


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(k in text for k in keywords)


def classify_message(message: str, has_transfer_in_progress: bool = False) -> str:
    text = re.sub(r"\s+", " ", message.strip().lower())

    if any(text.startswith(prefix) for prefix in TAREAS_INTENT_PREFIXES):
        return "tareas"
    if has_transfer_in_progress:
        return "transferencia"
    if _contains_any(text, TRANSFERENCIA_KEYWORDS):
        return "transferencia"
    if len(text) < 60 and _contains_any(text, BIENVENIDA_KEYWORDS):
        return "bienvenida"
    if _contains_any(text, TAREAS_KEYWORDS):
        return "tareas"
    if _contains_any(text, STOCK_KEYWORDS):
        return "stock"
    if _contains_any(text, RESEARCH_KEYWORDS):
        return "research"
    if _contains_any(text, EMAIL_KEYWORDS):
        return "email"
    if _contains_any(text, DOCUMENTOS_KEYWORDS):
        return "documentos"
    if _contains_any(text, FINANZAS_KEYWORDS):
        return "finanzas"
    return "completa"
