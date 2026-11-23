"""Taxa contratual: cobrada à parte do aluguel, em até 5 parcelas."""

from decimal import Decimal

from .dinheiro import formatar_brl


class TaxaContratual:
    VALOR_TOTAL = Decimal("2000.00")
    MAXIMO_PARCELAS = 5

    def __init__(self, parcelas: int = 1):
        self.parcelas = parcelas

    @property
    def parcelas(self) -> int:
        return self._parcelas

    @parcelas.setter
    def parcelas(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or not 1 <= valor <= self.MAXIMO_PARCELAS:
            raise ValueError(f"A taxa contratual pode ser paga de 1 a {self.MAXIMO_PARCELAS} parcelas.")
        self._parcelas = valor

    def valores_das_parcelas(self) -> list[Decimal]:
        """Divide a taxa em parcelas sem perder centavos.

        Trabalha em centavos inteiros. Se a divisão não for exata, o centavo que
        sobra vai para as primeiras parcelas. Ex.: 3x -> 666,67 + 666,67 + 666,66.
        """
        total_centavos = int(self.VALOR_TOTAL * 100)
        base, resto = divmod(total_centavos, self.parcelas)
        centavos = [base + (1 if i < resto else 0) for i in range(self.parcelas)]
        return [Decimal(c) / 100 for c in centavos]

    def parcela_do_mes(self, mes: int) -> Decimal:
        """Valor da taxa cobrado no mês ``mes`` (1 = primeiro mês do contrato)."""
        if 1 <= mes <= self.parcelas:
            return self.valores_das_parcelas()[mes - 1]
        return Decimal("0.00")

    def descricao(self) -> str:
        valores = self.valores_das_parcelas()
        if self.parcelas == 1:
            return "À vista (1x)"
        if len(set(valores)) == 1:
            return f"{self.parcelas}x de {formatar_brl(valores[0])} sem juros"
        partes = " + ".join(formatar_brl(v) for v in valores)
        return f"{self.parcelas}x sem juros ({partes})"
