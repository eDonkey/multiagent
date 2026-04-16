from app.services.classifier import classify_message


def test_transferencia_priority():
    assert classify_message("iniciar transferencia del corolla") == "transferencia"


def test_bienvenida_short_message():
    assert classify_message("hola") == "bienvenida"


def test_stock_fallback():
    assert classify_message("quiero ver el corolla") == "stock"
