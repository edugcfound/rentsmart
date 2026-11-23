"""Imóveis da R.M Imóveis e as regras comerciais de cada um.

Hierarquia de classes:

    Imovel (abstrata)
    ├── ImovelComQuartos (abstrata)   -> regras comuns de casa e apartamento
    │   ├── Apartamento
    │   └── Casa
    └── Estudio

Cada classe guarda os próprios valores (constantes de classe) e decide quais
adicionais e descontos se aplicam a ela (polimorfismo). O cálculo final
(base + adicionais - descontos) fica em um único lugar: ``Imovel.valor_mensal``.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from .dinheiro import arredondar


@dataclass(frozen=True)
class ItemOrcamento:
    """Uma linha da composição do aluguel (ex.: 'Vaga de garagem', 300,00).

    Valores negativos representam descontos.
    """

    descricao: str
    valor: Decimal


class Imovel(ABC):
    """Base de todos os imóveis: sabe montar a composição e somar o aluguel."""

    NOME = "Imóvel"
    ALUGUEL_BASE = Decimal("0.00")

    @abstractmethod
    def descricao(self) -> str:
        """Descrição curta do imóvel escolhido (ex.: 'Casa com 2 quartos')."""

    @abstractmethod
    def _calcular_adicionais(self) -> list[ItemOrcamento]:
        """Adicionais mensais que se aplicam a este tipo de imóvel."""

    def _calcular_descontos(self, subtotal: Decimal) -> list[ItemOrcamento]:
        """Descontos sobre o subtotal. Por padrão, nenhum."""
        return []

    def item_base(self) -> ItemOrcamento:
        return ItemOrcamento(f"Aluguel-base ({self.NOME.lower()})", self.ALUGUEL_BASE)

    def adicionais(self) -> list[ItemOrcamento]:
        return self._calcular_adicionais()

    def subtotal(self) -> Decimal:
        """Aluguel-base + adicionais (antes dos descontos)."""
        return self.ALUGUEL_BASE + sum((i.valor for i in self.adicionais()), Decimal("0"))

    def descontos(self) -> list[ItemOrcamento]:
        return self._calcular_descontos(self.subtotal())

    def composicao(self) -> list[ItemOrcamento]:
        """Todas as linhas que formam o aluguel, na ordem em que são aplicadas."""
        return [self.item_base(), *self.adicionais(), *self.descontos()]

    def valor_mensal(self) -> Decimal:
        """Aluguel mensal final = soma de todas as linhas da composição."""
        return arredondar(sum((i.valor for i in self.composicao()), Decimal("0")))


class ImovelComQuartos(Imovel):
    """Regras comuns de casa e apartamento: 1 ou 2 quartos e vaga de garagem.

    As subclasses só informam quanto custa o 2º quarto.
    """

    QUARTOS_PERMITIDOS = (1, 2)
    ADICIONAL_SEGUNDO_QUARTO = Decimal("0.00")
    ADICIONAL_GARAGEM = Decimal("300.00")

    def __init__(self, quartos: int = 1, garagem: bool = False):
        self.quartos = quartos      # passa pela validação do setter
        self.garagem = garagem

    # --- encapsulamento: atributos protegidos com validação ---
    @property
    def quartos(self) -> int:
        return self._quartos

    @quartos.setter
    def quartos(self, valor: int) -> None:
        if isinstance(valor, bool) or valor not in self.QUARTOS_PERMITIDOS:
            raise ValueError(f"{self.NOME} aceita apenas 1 ou 2 quartos (recebido: {valor!r}).")
        self._quartos = valor

    @property
    def garagem(self) -> bool:
        return self._garagem

    @garagem.setter
    def garagem(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("Garagem deve ser True (sim) ou False (não).")
        self._garagem = valor

    def descricao(self) -> str:
        texto = f"{self.NOME} com {self.quartos} quarto{'s' if self.quartos > 1 else ''}"
        return texto + (", com vaga de garagem" if self.garagem else ", sem garagem")

    def _calcular_adicionais(self) -> list[ItemOrcamento]:
        itens = []
        if self.quartos == 2:
            itens.append(ItemOrcamento("Adicional: 2º quarto", self.ADICIONAL_SEGUNDO_QUARTO))
        if self.garagem:
            itens.append(ItemOrcamento("Adicional: 1 vaga de garagem", self.ADICIONAL_GARAGEM))
        return itens


class Apartamento(ImovelComQuartos):
    NOME = "Apartamento"
    ALUGUEL_BASE = Decimal("700.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("200.00")
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = Decimal("0.05")

    def __init__(self, quartos: int = 1, garagem: bool = False, possui_criancas: bool = True):
        super().__init__(quartos, garagem)
        self.possui_criancas = possui_criancas

    @property
    def possui_criancas(self) -> bool:
        return self._possui_criancas

    @possui_criancas.setter
    def possui_criancas(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("'Possui crianças' deve ser True (sim) ou False (não).")
        self._possui_criancas = valor

    def descricao(self) -> str:
        return super().descricao() + (", com crianças" if self.possui_criancas else ", sem crianças")

    def _calcular_descontos(self, subtotal: Decimal) -> list[ItemOrcamento]:
        # Regra da R.M Imóveis: 5% sobre o aluguel JÁ com os adicionais.
        if self.possui_criancas:
            return []
        desconto = arredondar(subtotal * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS)
        return [ItemOrcamento("Desconto: 5% (cliente sem crianças)", -desconto)]


class Casa(ImovelComQuartos):
    NOME = "Casa"
    ALUGUEL_BASE = Decimal("900.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("250.00")


class Estudio(Imovel):
    """Estúdio: não tem opção de 2 quartos; estacionamento é por pacote de vagas."""

    NOME = "Estúdio"
    ALUGUEL_BASE = Decimal("1200.00")
    VAGAS_NO_PACOTE = 2
    VALOR_PACOTE_ESTACIONAMENTO = Decimal("250.00")
    VALOR_VAGA_ADICIONAL = Decimal("60.00")

    def __init__(self, pacote_estacionamento: bool = False, vagas_adicionais: int = 0):
        self.pacote_estacionamento = pacote_estacionamento
        self.vagas_adicionais = vagas_adicionais

    @property
    def pacote_estacionamento(self) -> bool:
        return self._pacote_estacionamento

    @pacote_estacionamento.setter
    def pacote_estacionamento(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("Pacote de estacionamento deve ser True (sim) ou False (não).")
        self._pacote_estacionamento = valor
        if not valor:
            self._vagas_adicionais = 0  # sem pacote não existem vagas extras

    @property
    def vagas_adicionais(self) -> int:
        return self._vagas_adicionais

    @vagas_adicionais.setter
    def vagas_adicionais(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise ValueError("Vagas adicionais deve ser um número inteiro maior ou igual a zero.")
        if valor > 0 and not self.pacote_estacionamento:
            raise ValueError("Vagas adicionais só podem ser contratadas junto com o pacote inicial de 2 vagas.")
        self._vagas_adicionais = valor

    @property
    def total_vagas(self) -> int:
        if not self.pacote_estacionamento:
            return 0
        return self.VAGAS_NO_PACOTE + self.vagas_adicionais

    def descricao(self) -> str:
        if not self.pacote_estacionamento:
            return "Estúdio, sem estacionamento"
        return f"Estúdio com estacionamento ({self.total_vagas} vagas)"

    def _calcular_adicionais(self) -> list[ItemOrcamento]:
        if not self.pacote_estacionamento:
            return []
        itens = [ItemOrcamento("Adicional: pacote de estacionamento (2 vagas)",
                               self.VALOR_PACOTE_ESTACIONAMENTO)]
        if self.vagas_adicionais:
            itens.append(ItemOrcamento(
                f"Adicional: {self.vagas_adicionais} vaga(s) extra x R$ 60,00",
                self.VALOR_VAGA_ADICIONAL * self.vagas_adicionais,
            ))
        return itens
