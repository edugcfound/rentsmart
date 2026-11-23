"""Funções de apoio para trabalhar com valores em reais.

Usamos ``Decimal`` em vez de ``float`` porque ``float`` não representa
centavos com exatidão (ex.: 0.1 + 0.2 != 0.3). Em dinheiro isso vira erro.
"""

from decimal import ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")


def arredondar(valor) -> Decimal:
    """Arredonda para 2 casas decimais (regra comercial: 0,005 sobe)."""
    return Decimal(valor).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def formatar_brl(valor) -> str:
    """Formata no padrão brasileiro: ``R$ 1.234,56`` (negativo: ``-R$ 60,00``)."""
    valor = arredondar(valor)
    sinal = "-" if valor < 0 else ""
    texto = f"{abs(valor):,.2f}"  # 1,234.56 (padrão americano)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}R$ {texto}"


def formatar_decimal_csv(valor) -> str:
    """Formata para o CSV: vírgula decimal e sem separador de milhar (``1234,56``)."""
    return f"{arredondar(valor):.2f}".replace(".", ",")
