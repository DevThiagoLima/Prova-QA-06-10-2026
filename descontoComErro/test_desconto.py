import pytest
from desconto import calcular_desconto


@pytest.mark.parametrize("valor, tipo, esperado", [
    (0, "COMUM", 0.0),
    (99.99, "COMUM", 0.0),
    (99.99, "VIP", 5.0),
    (50, "VIP", 2.5),
    (100, "COMUM", 10.0),        # fronteira (bug 1)
    (100, "VIP", 15.0),
    (100.01, "COMUM", 10.0),
    (300, "COMUM", 30.0),
    (300, "VIP", 45.0),
    (499.99, "COMUM", 50.0),
    (500, "COMUM", 100.0),
    (500, "VIP", 125.0),
    (500.01, "COMUM", 100.0),
    (1000, "COMUM", 200.0),      # teto exato
    (1000.01, "COMUM", 200.0),   # acima do teto
    (999, "VIP", 200.0),         # 249,75 limitado
    (1000000, "COMUM", 200.0),
])
def test_calculo(valor, tipo, esperado):
    assert calcular_desconto(valor, tipo) == pytest.approx(esperado)


@pytest.mark.parametrize("tipo", ["VIP", "vip", "Vip", " VIP "])
def test_vip_case_insensitive(tipo):          # bug 2
    assert calcular_desconto(300, tipo) == pytest.approx(45.0)


@pytest.mark.parametrize("valor", [-1, -0.01, float("nan"), float("inf")])
def test_valor_invalido(valor):
    with pytest.raises(ValueError):
        calcular_desconto(valor, "COMUM")


@pytest.mark.parametrize("valor", [None, "abc", "100", True, [100]])
def test_valor_tipo_invalido(valor):
    with pytest.raises(TypeError):
        calcular_desconto(valor, "COMUM")


@pytest.mark.parametrize("tipo", ["", "PREMIUM", "  "])
def test_tipo_invalido_valor(tipo):
    with pytest.raises(ValueError):
        calcular_desconto(300, tipo)


@pytest.mark.parametrize("tipo", [None, 123])
def test_tipo_invalido_tipo(tipo):
    with pytest.raises(TypeError):
        calcular_desconto(300, tipo)
