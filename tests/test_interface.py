import tempfile
import unittest
from decimal import Decimal as D

from rentsmart import Apartamento, Casa, Estudio, ExportadorCSV, InterfaceConsole


class EntradaSimulada:
    """Faz o papel do teclado nos testes: devolve as respostas em ordem."""

    def __init__(self, respostas):
        self.respostas = list(respostas)
        self.perguntas = []

    def __call__(self, pergunta):
        self.perguntas.append(pergunta)
        return self.respostas.pop(0)


class TestInterfaceConsole(unittest.TestCase):
    def _interface(self, respostas, pasta="saida"):
        self.saidas = []
        self.entrada = EntradaSimulada(respostas)
        return InterfaceConsole(self.entrada, self.saidas.append, ExportadorCSV(pasta))

    def _erros(self):
        return [s for s in self.saidas if s.startswith("  [!]")]

    def test_apartamento_completo(self):
        orc = self._interface(["Ana", "1", "2", "s", "n", "5"]).coletar_orcamento()
        self.assertIsInstance(orc.imovel, Apartamento)
        self.assertEqual(orc.aluguel_mensal, D("1140.00"))
        self.assertEqual(orc.taxa.parcelas, 5)

    def test_casa_nao_pergunta_sobre_criancas(self):
        orc = self._interface(["Bia", "2", "1", "S", "1"]).coletar_orcamento()
        self.assertIsInstance(orc.imovel, Casa)
        self.assertEqual(orc.aluguel_mensal, D("1200.00"))
        self.assertFalse(any("crianças" in p for p in self.entrada.perguntas))

    def test_estudio_nao_pergunta_quartos(self):
        orc = self._interface(["Caio", "3", "sim", "2", "2"]).coletar_orcamento()
        self.assertIsInstance(orc.imovel, Estudio)
        self.assertEqual(orc.aluguel_mensal, D("1570.00"))
        self.assertFalse(any("quartos" in p for p in self.entrada.perguntas))

    def test_estudio_sem_pacote_nao_pergunta_vagas_extras(self):
        orc = self._interface(["Caio", "3", "N", "1"]).coletar_orcamento()
        self.assertEqual(orc.aluguel_mensal, D("1200.00"))
        self.assertFalse(any("adicionais" in p for p in self.entrada.perguntas))

    def test_entradas_invalidas_sao_repetidas(self):
        respostas = ["", "Ana",          # nome vazio
                     "4", "x", "1",      # tipo inválido
                     "3", "dois", "2",   # quartos inválidos
                     "talvez", "n",      # garagem inválida
                     "s",                # crianças
                     "0", "6", "2,5", "2"]  # parcelas inválidas
        orc = self._interface(respostas).coletar_orcamento()
        self.assertEqual(orc.aluguel_mensal, D("900.00"))
        self.assertEqual(orc.taxa.parcelas, 2)
        self.assertEqual(len(self._erros()), 9)

    def test_executar_gera_csv_e_pode_repetir(self):
        with tempfile.TemporaryDirectory() as pasta:
            interface = self._interface(
                ["Ana", "2", "2", "n", "1", "s",     # 1º orçamento, depois "outro? s"
                 "Bia", "3", "n", "4", "n"], pasta)  # 2º orçamento, depois "outro? n"
            arquivos = interface.executar()
            self.assertEqual(len(arquivos), 2)
            self.assertTrue(all(a.exists() for a in arquivos))
        self.assertTrue(any("ORÇAMENTO DE LOCAÇÃO" in s for s in self.saidas))


if __name__ == "__main__":
    unittest.main()
