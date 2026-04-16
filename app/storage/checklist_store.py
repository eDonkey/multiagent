from app.utils.json_storage import JsonStorage

STORE = JsonStorage("storage/checklists.json")


def record_checklist_event(vehicle_ref: str, status: str = "created") -> None:
    payload = STORE.read()
    payload[vehicle_ref] = {"status": status}
    STORE.write(payload)


def get_pending_events() -> dict:
    return STORE.read()
