"""Interface de terminal: pergunta, valida as respostas e mostra o orçamento.

A entrada e a saída são recebidas no construtor (``entrada=input``,
``saida=print``). Assim os testes automatizados conseguem "digitar" respostas
sem precisar de um usuário.
"""

from .exportador_csv import ExportadorCSV
from .imoveis import Apartamento, Casa, Estudio, Imovel
from .orcamento import Orcamento
from .taxa_contratual import TaxaContratual

SIM = {"s", "sim"}
NAO = {"n", "nao", "não"}


class InterfaceConsole:
    TIPOS_DE_IMOVEL = {"1": "Apartamento", "2": "Casa", "3": "Estúdio"}

    def __init__(self, entrada=input, saida=print, exportador=None):
        self._entrada = entrada
        self._saida = saida
        self._exportador = exportador or ExportadorCSV()

    # ------------------------------------------------ leitura com validação
    def _perguntar(self, mensagem: str) -> str:
        return self._entrada(mensagem).strip()

    def _erro(self, mensagem: str) -> None:
        self._saida(f"  [!] {mensagem}")

    def ler_texto(self, mensagem: str) -> str:
        while True:
            resposta = self._perguntar(mensagem)
            if resposta:
                return resposta
            self._erro("Este campo não pode ficar vazio.")

    def ler_opcao(self, mensagem: str, opcoes: dict) -> str:
        """Repete a pergunta até a resposta ser uma das chaves de ``opcoes``."""
        while True:
            resposta = self._perguntar(mensagem)
            if resposta in opcoes:
                return resposta
            self._erro(f"Opção inválida. Digite uma destas: {', '.join(opcoes)}.")

    def ler_sim_nao(self, mensagem: str) -> bool:
        while True:
            resposta = self._perguntar(mensagem).lower()
            if resposta in SIM:
                return True
            if resposta in NAO:
                return False
            self._erro("Responda S (sim) ou N (não).")

    def ler_inteiro(self, mensagem: str, minimo: int, maximo=None) -> int:
        while True:
            resposta = self._perguntar(mensagem)
            try:
                numero = int(resposta)
            except ValueError:
                self._erro("Digite um número inteiro (sem letras, vírgula ou ponto).")
                continue
            if numero < minimo or (maximo is not None and numero > maximo):
                faixa = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
                self._erro(f"O número deve ser {faixa}.")
                continue
            return numero

    # ------------------------------------------------ montagem do orçamento
    def _coletar_imovel(self) -> Imovel:
        self._saida("\nTipos de imóvel:")
        self._saida("  1 - Apartamento (base R$ 700,00)")
        self._saida("  2 - Casa        (base R$ 900,00)")
        self._saida("  3 - Estúdio     (base R$ 1.200,00)")
        tipo = self.ler_opcao("Escolha o tipo de imóvel (1, 2 ou 3): ", self.TIPOS_DE_IMOVEL)

        if tipo == "3":
            pacote = self.ler_sim_nao("Deseja o pacote de estacionamento com 2 vagas (R$ 250,00)? (S/N): ")
            extras = 0
            if pacote:
                extras = self.ler_inteiro("Quantas vagas adicionais (R$ 60,00 cada)? (0 = nenhuma): ", 0)
            return Estudio(pacote_estacionamento=pacote, vagas_adicionais=extras)

        quartos = self.ler_inteiro("Quantos quartos? (1 ou 2): ", 1, 2)
        garagem = self.ler_sim_nao("Deseja vaga de garagem (R$ 300,00)? (S/N): ")
        if tipo == "1":
            criancas = self.ler_sim_nao("O cliente possui crianças? (S/N): ")
            return Apartamento(quartos=quartos, garagem=garagem, possui_criancas=criancas)
        return Casa(quartos=quartos, garagem=garagem)

    def coletar_orcamento(self) -> Orcamento:
        cliente = self.ler_texto("Nome do cliente: ")
        imovel = self._coletar_imovel()
        parcelas = self.ler_inteiro(
            f"\nTaxa contratual de R$ 2.000,00. Em quantas parcelas? (1 a {TaxaContratual.MAXIMO_PARCELAS}): ",
            1, TaxaContratual.MAXIMO_PARCELAS,
        )
        return Orcamento(cliente, imovel, TaxaContratual(parcelas))

    # ------------------------------------------------ fluxo principal
    def executar(self) -> list:
        """Roda o atendimento; devolve a lista de CSVs gerados."""
        self._saida("=" * 64)
        self._saida("RentSmart | Sistema de Orçamento de Locação | R.M Imóveis".center(64))
        self._saida("=" * 64)
        arquivos = []
        while True:
            orcamento = self.coletar_orcamento()
            self._saida("\n" + orcamento.resumo())
            caminho = self._exportador.exportar(orcamento)
            arquivos.append(caminho)
            self._saida(f"\nProjeção de 12 meses salva em: {caminho}")
            if not self.ler_sim_nao("\nDeseja fazer outro orçamento? (S/N): "):
                self._saida("Obrigado por usar o RentSmart!")
                return arquivos
            self._saida("")
