from decimal import Decimal, ROUND_HALF_UP

TETO_DESCONTO = Decimal("200.00")


def calcular_desconto(valor_compra, tipo_cliente):
    # Validação de entrada
    if isinstance(valor_compra, bool) or not isinstance(valor_compra, (int, float, Decimal)):
        raise TypeError("valor_compra deve ser numérico")
    if not isinstance(tipo_cliente, str):
        raise TypeError("tipo_cliente deve ser texto")

    valor = Decimal(str(valor_compra))
    if valor.is_nan() or valor.is_infinite() or valor < 0:
        raise ValueError("valor_compra inválido")

    tipo = tipo_cliente.strip().upper()
    if tipo not in ("VIP", "COMUM"):
        raise ValueError("tipo_cliente deve ser 'VIP' ou 'COMUM'")

    # Desconto base
    if valor >= 500:
        percentual = Decimal("0.20")
    elif valor >= 100:                 # BUG corrigido: era > 100
        percentual = Decimal("0.10")
    else:
        percentual = Decimal("0")

    # Acréscimo VIP (case-insensitive)
    if tipo == "VIP":                  # BUG corrigido: antes só aceitava "VIP"
        percentual += Decimal("0.05")

    valor_desconto = valor * percentual

    # Teto de R$ 200,00
    if valor_desconto > TETO_DESCONTO:
        valor_desconto = TETO_DESCONTO

    return float(valor_desconto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
