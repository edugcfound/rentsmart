"""Orçamento de locação: junta o imóvel, a taxa contratual e a projeção anual."""

from dataclasses import dataclass
from decimal import Decimal

from .dinheiro import formatar_brl
from .imoveis import Imovel
from .taxa_contratual import TaxaContratual

LARGURA = 64


@dataclass(frozen=True)
class LinhaProjecao:
    """Um mês da projeção: aluguel e parcela da taxa ficam em campos separados."""

    mes: int
    aluguel: Decimal
    parcela_taxa: Decimal
    numero_parcela: str      # ex.: "2/5" ou "-" quando não há parcela no mês
    total_mes: Decimal
    total_acumulado: Decimal


class Orcamento:
    MESES_PROJECAO = 12

    def __init__(self, cliente: str, imovel: Imovel, taxa: TaxaContratual):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    @property
    def cliente(self) -> str:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: str) -> None:
        valor = (valor or "").strip()
        if not valor:
            raise ValueError("O nome do cliente não pode ficar vazio.")
        self._cliente = valor

    @property
    def imovel(self) -> Imovel:
        return self._imovel

    @imovel.setter
    def imovel(self, valor: Imovel) -> None:
        if not isinstance(valor, Imovel):
            raise ValueError("O orçamento precisa de um imóvel (Apartamento, Casa ou Estudio).")
        self._imovel = valor

    @property
    def taxa(self) -> TaxaContratual:
        return self._taxa

    @taxa.setter
    def taxa(self, valor: TaxaContratual) -> None:
        if not isinstance(valor, TaxaContratual):
            raise ValueError("O orçamento precisa de uma TaxaContratual.")
        self._taxa = valor

    @property
    def aluguel_mensal(self) -> Decimal:
        return self.imovel.valor_mensal()

    def projecao_12_meses(self) -> list[LinhaProjecao]:
        linhas = []
        acumulado = Decimal("0.00")
        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            numero = f"{mes}/{self.taxa.parcelas}" if parcela > 0 else "-"
            total = self.aluguel_mensal + parcela
            acumulado += total
            linhas.append(LinhaProjecao(mes, self.aluguel_mensal, parcela, numero, total, acumulado))
        return linhas

    def total_aluguel_no_ano(self) -> Decimal:
        return self.aluguel_mensal * self.MESES_PROJECAO

    def total_no_ano(self) -> Decimal:
        return self.total_aluguel_no_ano() + self.taxa.VALOR_TOTAL

    # ------------------------------------------------------------ exibição
    @staticmethod
    def _linha(descricao: str, valor) -> str:
        texto_valor = formatar_brl(valor)
        return f"  {descricao:<{LARGURA - len(texto_valor) - 3}} {texto_valor}"

    def resumo(self) -> str:
        """Texto do orçamento mostrando como cada valor foi formado."""
        im = self.imovel
        sep = "-" * LARGURA
        out = [
            "=" * LARGURA,
            "RentSmart | R.M Imóveis | ORÇAMENTO DE LOCAÇÃO".center(LARGURA),
            "=" * LARGURA,
            f"Cliente: {self.cliente}",
            f"Imóvel : {im.descricao()}",
            sep,
            "1) COMPOSIÇÃO DO ALUGUEL MENSAL",
            self._linha(im.item_base().descricao, im.item_base().valor),
        ]
        out += [self._linha("(+) " + i.descricao, i.valor) for i in im.adicionais()]
        if im.adicionais() or im.descontos():
            out.append(self._linha("= Subtotal (base + adicionais)", im.subtotal()))
        out += [self._linha("(-) " + i.descricao, i.valor) for i in im.descontos()]
        out += [
            self._linha("ALUGUEL MENSAL", self.aluguel_mensal),
            sep,
            "2) TAXA CONTRATUAL (cobrada à parte, NÃO faz parte do aluguel)",
            self._linha("Valor total da taxa", self.taxa.VALOR_TOTAL),
            f"  Parcelamento escolhido: {self.taxa.descricao()}",
            f"  Cobrança: do mês 1 ao mês {self.taxa.parcelas} do contrato"
            if self.taxa.parcelas > 1 else "  Cobrança: no mês 1 do contrato",
            sep,
            "3) PROJEÇÃO DOS 12 PRIMEIROS MESES",
            f"  {'Mês':>3}  {'Aluguel':>13}  {'Taxa (parc.)':>19}  {'Total do mês':>14}",
        ]
        for l in self.projecao_12_meses():
            taxa = f"{formatar_brl(l.parcela_taxa)} {l.numero_parcela:>3}" if l.parcela_taxa else "-"
            out.append(f"  {l.mes:>3}  {formatar_brl(l.aluguel):>13}  {taxa:>19}  {formatar_brl(l.total_mes):>14}")
        out += [
            sep,
            self._linha("Total de aluguel em 12 meses", self.total_aluguel_no_ano()),
            self._linha("Total da taxa contratual", self.taxa.VALOR_TOTAL),
            self._linha("TOTAL PREVISTO NO 1º ANO", self.total_no_ano()),
            "=" * LARGURA,
        ]
        return "\n".join(out)
