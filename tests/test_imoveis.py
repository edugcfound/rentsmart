import unittest
from decimal import Decimal as D

from rentsmart import Apartamento, Casa, Estudio, Imovel


class TestApartamento(unittest.TestCase):
    def test_base_1_quarto_com_criancas(self):
        self.assertEqual(Apartamento(1, False, True).valor_mensal(), D("700.00"))

    def test_2_quartos_soma_200(self):
        self.assertEqual(Apartamento(2, False, True).valor_mensal(), D("900.00"))

    def test_garagem_soma_300(self):
        self.assertEqual(Apartamento(1, True, True).valor_mensal(), D("1000.00"))

    def test_desconto_5_porcento_sem_criancas_so_base(self):
        self.assertEqual(Apartamento(1, False, False).valor_mensal(), D("665.00"))

    def test_desconto_aplicado_depois_dos_adicionais(self):
        # (700 + 200 + 300) = 1200 -> 5% = 60 -> 1140
        ap = Apartamento(2, True, False)
        self.assertEqual(ap.subtotal(), D("1200.00"))
        self.assertEqual(ap.descontos()[0].valor, D("-60.00"))
        self.assertEqual(ap.valor_mensal(), D("1140.00"))

    def test_com_criancas_nao_tem_desconto(self):
        self.assertEqual(Apartamento(2, True, True).descontos(), [])
        self.assertEqual(Apartamento(2, True, True).valor_mensal(), D("1200.00"))

    def test_quartos_invalidos(self):
        for invalido in (0, 3, -1, "2", True, 1.5):
            with self.subTest(invalido=invalido), self.assertRaises(ValueError):
                Apartamento(quartos=invalido)

    def test_flags_precisam_ser_bool(self):
        with self.assertRaises(ValueError):
            Apartamento(garagem="S")
        with self.assertRaises(ValueError):
            Apartamento(possui_criancas="nao")


class TestCasa(unittest.TestCase):
    def test_base(self):
        self.assertEqual(Casa(1, False).valor_mensal(), D("900.00"))

    def test_2_quartos_soma_250(self):
        self.assertEqual(Casa(2, False).valor_mensal(), D("1150.00"))

    def test_2_quartos_e_garagem(self):
        self.assertEqual(Casa(2, True).valor_mensal(), D("1450.00"))

    def test_casa_nao_tem_desconto_por_criancas(self):
        self.assertEqual(Casa(2, True).descontos(), [])
        self.assertFalse(hasattr(Casa(), "possui_criancas"))

    def test_composicao_lista_cada_linha(self):
        descricoes = [i.descricao for i in Casa(2, True).composicao()]
        self.assertEqual(len(descricoes), 3)
        self.assertIn("2º quarto", descricoes[1])
        self.assertIn("garagem", descricoes[2])


class TestEstudio(unittest.TestCase):
    def test_base_sem_estacionamento(self):
        self.assertEqual(Estudio().valor_mensal(), D("1200.00"))

    def test_pacote_2_vagas(self):
        e = Estudio(pacote_estacionamento=True)
        self.assertEqual(e.valor_mensal(), D("1450.00"))
        self.assertEqual(e.total_vagas, 2)

    def test_vagas_adicionais_60_cada(self):
        e = Estudio(pacote_estacionamento=True, vagas_adicionais=3)
        self.assertEqual(e.valor_mensal(), D("1630.00"))  # 1200 + 250 + 3*60
        self.assertEqual(e.total_vagas, 5)

    def test_vagas_adicionais_exigem_pacote(self):
        with self.assertRaises(ValueError):
            Estudio(pacote_estacionamento=False, vagas_adicionais=1)

    def test_vagas_negativas_ou_nao_inteiras(self):
        for invalido in (-1, 1.5, "2", True):
            with self.subTest(invalido=invalido), self.assertRaises(ValueError):
                Estudio(pacote_estacionamento=True, vagas_adicionais=invalido)

    def test_desligar_pacote_zera_vagas_extras(self):
        e = Estudio(True, 2)
        e.pacote_estacionamento = False
        self.assertEqual(e.vagas_adicionais, 0)
        self.assertEqual(e.valor_mensal(), D("1200.00"))

    def test_estudio_nao_tem_quartos_nem_garagem(self):
        self.assertFalse(hasattr(Estudio(), "quartos"))
        self.assertFalse(hasattr(Estudio(), "garagem"))


class TestHierarquia(unittest.TestCase):
    def test_imovel_e_abstrato(self):
        with self.assertRaises(TypeError):
            Imovel()

    def test_polimorfismo_mesmo_metodo_resultados_diferentes(self):
        imoveis = [Apartamento(), Casa(), Estudio()]
        self.assertEqual([i.valor_mensal() for i in imoveis], [D("700.00"), D("900.00"), D("1200.00")])
        self.assertTrue(all(isinstance(i, Imovel) for i in imoveis))


if __name__ == "__main__":
    unittest.main()
