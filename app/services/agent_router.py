def detect_agent_type(message_text: str) -> str:
    text = message_text.lower()

    secretary_keywords = [
        'horario',
        'direccion',
        'ubicacion',
        'donde estan',
        'abren',
        'cierran',
        'sucursal',
    ]

    for keyword in secretary_keywords:
        if keyword in text:
            return 'secretary'

    return 'seller'
