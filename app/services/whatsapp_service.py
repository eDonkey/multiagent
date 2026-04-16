import httpx
from app.core.config import settings


def send_whatsapp_text(to_phone: str, body: str):
    url = f'https://graph.facebook.com/v20.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages'
    headers = {
        'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging_product': 'whatsapp',
        'to': to_phone,
        'type': 'text',
        'text': {'body': body},
    }

    with httpx.Client(timeout=20) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
