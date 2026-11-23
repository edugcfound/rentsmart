import csv
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

from rentsmart import Apartamento, Casa, Estudio, ExportadorCSV, Orcamento, TaxaContratual
from rentsmart.dinheiro import formatar_brl


class TestFormatacao(unittest.TestCase):
    def test_formatar_brl(self):
        self.assertEqual(formatar_brl(D("1234.5")), "R$ 1.234,50")
        self.assertEqual(formatar_brl(D("-60")), "-R$ 60,00")
        self.assertEqual(formatar_brl(D("700")), "R$ 700,00")


class TestOrcamento(unittest.TestCase):
    def setUp(self):
        self.orc = Orcamento("Ana", Apartamento(2, True, False), TaxaContratual(5))

    def test_aluguel_separado_da_taxa(self):
        self.assertEqual(self.orc.aluguel_mensal, D("1140.00"))
        self.assertEqual(self.orc.taxa.VALOR_TOTAL, D("2000.00"))

    def test_projecao_tem_12_meses(self):
        linhas = self.orc.projecao_12_meses()
        self.assertEqual([l.mes for l in linhas], list(range(1, 13)))

    def test_taxa_so_nos_meses_parcelados(self):
        linhas = self.orc.projecao_12_meses()
        self.assertTrue(all(l.parcela_taxa == D("400") for l in linhas[:5]))
        self.assertTrue(all(l.parcela_taxa == 0 for l in linhas[5:]))
        self.assertEqual(linhas[0].numero_parcela, "1/5")
        self.assertEqual(linhas[5].numero_parcela, "-")

    def test_totais(self):
        linhas = self.orc.projecao_12_meses()
        self.assertEqual(linhas[0].total_mes, D("1540.00"))
        self.assertEqual(linhas[-1].total_acumulado, D("15680.00"))
        self.assertEqual(self.orc.total_aluguel_no_ano(), D("13680.00"))
        self.assertEqual(self.orc.total_no_ano(), D("15680.00"))

    def test_resumo_mostra_composicao_e_taxa_separada(self):
        texto = self.orc.resumo()
        for trecho in ("Aluguel-base", "2º quarto", "garagem", "Desconto: 5%",
                       "ALUGUEL MENSAL", "R$ 1.140,00", "TAXA CONTRATUAL", "5x de R$ 400,00"):
            self.assertIn(trecho, texto)
        self.assertLess(texto.index("ALUGUEL MENSAL"), texto.index("TAXA CONTRATUAL"))

    def test_validacoes(self):
        with self.assertRaises(ValueError):
            Orcamento("   ", Casa(), TaxaContratual())
        with self.assertRaises(ValueError):
            Orcamento("Ana", "casa", TaxaContratual())
        with self.assertRaises(ValueError):
            Orcamento("Ana", Casa(), 3)


class TestExportadorCSV(unittest.TestCase):
    def _ler(self, caminho):
        with open(caminho, encoding="utf-8-sig", newline="") as f:
            return list(csv.reader(f, delimiter=";"))

    def test_csv_com_cabecalho_12_meses_e_total(self):
        orc = Orcamento("Bruno Lima", Estudio(True, 1), TaxaContratual(3))
        with tempfile.TemporaryDirectory() as pasta:
            caminho = ExportadorCSV(pasta).exportar(orc)
            self.assertTrue(caminho.exists())
            self.assertEqual(caminho.name, "projecao_12_meses_bruno_lima_estudio.csv")
            linhas = self._ler(caminho)
        self.assertEqual(linhas[0], ExportadorCSV.CABECALHO)
        meses = linhas[1:13]
        self.assertEqual([l[0] for l in meses], [str(m) for m in range(1, 13)])
        self.assertEqual(meses[0], ["1", "1510,00", "666,67", "1/3", "2176,67", "2176,67"])
        self.assertEqual(meses[2][2], "666,66")
        self.assertEqual(meses[3][2], "0,00")
        self.assertEqual(linhas[13][0], "TOTAL")
        self.assertEqual(linhas[13][2], "2000,00")
        self.assertEqual(linhas[13][4], "20120,00")   # 1510*12 + 2000
        self.assertEqual(len(linhas), 14)

    def test_caminho_personalizado(self):
        orc = Orcamento("Ana", Casa(), TaxaContratual(1))
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / "sub" / "meu.csv"
            self.assertEqual(ExportadorCSV().exportar(orc, destino), destino)
            self.assertTrue(destino.exists())


if __name__ == "__main__":
    unittest.main()
