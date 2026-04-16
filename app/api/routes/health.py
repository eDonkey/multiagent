from fastapi import APIRouter
from app.integrations.kapso_client import KapsoClient

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "kapso": KapsoClient().health()}
