import unittest
from decimal import Decimal as D

from rentsmart import TaxaContratual


class TestTaxaContratual(unittest.TestCase):
    def test_valor_total_2000(self):
        self.assertEqual(TaxaContratual.VALOR_TOTAL, D("2000.00"))

    def test_parcelas_somam_2000_em_todas_as_opcoes(self):
        for n in range(1, 6):
            with self.subTest(parcelas=n):
                valores = TaxaContratual(n).valores_das_parcelas()
                self.assertEqual(len(valores), n)
                self.assertEqual(sum(valores), D("2000.00"))

    def test_5x_de_400(self):
        self.assertEqual(TaxaContratual(5).valores_das_parcelas(), [D("400")] * 5)

    def test_3x_distribui_centavos(self):
        self.assertEqual(TaxaContratual(3).valores_das_parcelas(), [D("666.67"), D("666.67"), D("666.66")])

    def test_limite_de_parcelas(self):
        for invalido in (0, 6, -1, 2.5, "3", True):
            with self.subTest(invalido=invalido), self.assertRaises(ValueError):
                TaxaContratual(invalido)

    def test_parcela_do_mes(self):
        taxa = TaxaContratual(4)
        self.assertEqual(taxa.parcela_do_mes(1), D("500"))
        self.assertEqual(taxa.parcela_do_mes(4), D("500"))
        self.assertEqual(taxa.parcela_do_mes(5), D("0.00"))

    def test_descricao(self):
        self.assertEqual(TaxaContratual(1).descricao(), "À vista (1x)")
        self.assertEqual(TaxaContratual(5).descricao(), "5x de R$ 400,00 sem juros")


if __name__ == "__main__":
    unittest.main()
