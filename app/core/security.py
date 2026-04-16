from fastapi import Header, HTTPException, status
from app.core.config import settings


def verify_webhook_secret(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-API-Key",
        )
