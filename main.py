"""Ponto de entrada do RentSmart.

Como rodar (na pasta do projeto):
    python main.py
"""

import sys

from rentsmart import InterfaceConsole


def main() -> int:
    try:
        InterfaceConsole().executar()
    except (KeyboardInterrupt, EOFError):
        print("\n\nAtendimento cancelado pelo usuário. Nenhum orçamento pendente foi salvo.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
