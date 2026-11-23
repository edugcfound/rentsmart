"""Gera o arquivo CSV com a projeção dos 12 meses do orçamento."""

import csv
from pathlib import Path

from .dinheiro import formatar_decimal_csv
from .orcamento import Orcamento


class ExportadorCSV:
    """Grava a projeção em CSV no formato do Excel em português.

    - separador ``;`` e vírgula decimal (``1140,00``);
    - codificação UTF-8 com BOM, para os acentos abrirem certos no Excel.
    """

    CABECALHO = [
        "Mes",
        "Aluguel mensal (R$)",
        "Parcela da taxa contratual (R$)",
        "Parcela n.",
        "Total do mes (R$)",
        "Total acumulado (R$)",
    ]
    SEPARADOR = ";"

    def __init__(self, pasta_saida="saida"):
        self.pasta_saida = Path(pasta_saida)

    def nome_arquivo(self, orcamento: Orcamento) -> str:
        cliente = "".join(c if c.isalnum() else "_" for c in orcamento.cliente.lower()).strip("_")
        tipo = orcamento.imovel.NOME.lower().replace("ú", "u")
        return f"projecao_12_meses_{cliente or 'cliente'}_{tipo}.csv"

    def exportar(self, orcamento: Orcamento, caminho=None) -> Path:
        caminho = Path(caminho) if caminho else self.pasta_saida / self.nome_arquivo(orcamento)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        f = formatar_decimal_csv
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=self.SEPARADOR)
            escritor.writerow(self.CABECALHO)
            for l in orcamento.projecao_12_meses():
                escritor.writerow([l.mes, f(l.aluguel), f(l.parcela_taxa), l.numero_parcela,
                                   f(l.total_mes), f(l.total_acumulado)])
            escritor.writerow(["TOTAL", f(orcamento.total_aluguel_no_ano()),
                               f(orcamento.taxa.VALOR_TOTAL), "", f(orcamento.total_no_ano()), ""])
        return caminho
