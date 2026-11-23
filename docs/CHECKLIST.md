# Checklist de conformidade — RentSmart

Fonte única: `TRABALHO - AT & IOOP.docx` (lido por inteiro: 4 quadros de texto — Título, Desafio,
Fonte de pesquisa, Entregável — e 1 imagem de fundo com o cabeçalho "Orientações — Entrega de
Trabalho" da UniFECAF, sem requisitos). O documento **não informa prazo de entrega** nem o
**formato exato do CSV**.

Legenda: ✅ feito e verificado · 🟡 preparado, depende do Eduardo · ⬜ pendente

## A. Regras de negócio (quadro "Desafio")

| # | Regra literal do documento | Onde está no código | Teste | Status |
|---|---|---|---|---|
| RN01 | Apartamento 1 quarto: aluguel-base R$ 700,00 | `Apartamento.ALUGUEL_BASE` | `test_imoveis` | ✅ |
| RN02 | Casa 1 quarto: aluguel-base R$ 900,00 | `Casa.ALUGUEL_BASE` | `test_imoveis` | ✅ |
| RN03 | Estúdio: aluguel-base R$ 1.200,00 | `Estudio.ALUGUEL_BASE` | `test_imoveis` | ✅ |
| RN04 | Taxa contratual R$ 2.000,00, paga em até 5 parcelas | `TaxaContratual` | `test_taxa_contratual` | ✅ |
| RN05 | Apartamento 2 quartos: + R$ 200,00 no aluguel mensal | `Apartamento.ADICIONAL_SEGUNDO_QUARTO` | `test_imoveis` | ✅ |
| RN06 | Casa 2 quartos: + R$ 250,00 | `Casa.ADICIONAL_SEGUNDO_QUARTO` | `test_imoveis` | ✅ |
| RN07 | Casa e apartamento: vaga de garagem + R$ 300,00 | `ImovelComQuartos.ADICIONAL_GARAGEM` | `test_imoveis` | ✅ |
| RN08 | Estúdio: pacote inicial de 2 vagas R$ 250,00 | `Estudio.VALOR_PACOTE_ESTACIONAMENTO` | `test_imoveis` | ✅ |
| RN09 | Estúdio: + R$ 60,00 por vaga adicional | `Estudio.VALOR_VAGA_ADICIONAL` | `test_imoveis` | ✅ |
| RN10 | Apartamento sem crianças: 5% de desconto **após** os adicionais | `Apartamento._calcular_descontos` | `test_imoveis` | ✅ |

## B. Comportamento do sistema (quadro "Desafio")

| # | Requisito | Onde | Status |
|---|---|---|---|
| S01 | Solicitar ao usuário as informações necessárias | `InterfaceConsole.coletar_orcamento` | ✅ |
| S02 | Validar as escolhas realizadas | `InterfaceConsole.ler_*` + setters das classes | ✅ |
| S03 | Calcular corretamente o valor mensal | `Imovel.valor_mensal` | ✅ |
| S04 | Resumo detalhado mostrando como o valor foi formado | `Orcamento.resumo` | ✅ |
| S05 | Taxa contratual e parcelamento apresentados **separadamente** do aluguel | `Orcamento.resumo` (bloco próprio) + colunas separadas no CSV | ✅ |
| S06 | Gerar CSV com a projeção dos 12 meses | `ExportadorCSV` | ✅ |
| S07 | Usar classes, objetos, atributos e métodos; separar responsabilidades; evitar repetição | pacote `rentsmart/` (ver README) | ✅ |

## C. Entregáveis (quadro "5. Entregável e distribuição da pontuação")

| # | Entregável | Peso | Situação |
|---|---|---|---|
| E01 | Código-fonte .py organizado e executável | Prática 50% | ✅ |
| E02 | Uso efetivo de classes, objetos, atributos e métodos | Prática | ✅ |
| E03 | Regras de casa, apartamento e estúdio corretas | Prática | ✅ (testes automatizados) |
| E04 | Adicionais, descontos e taxa contratual | Prática | ✅ |
| E05 | Validação das principais entradas | Prática | ✅ |
| E06 | Exibição clara do orçamento final | Prática | ✅ |
| E07 | Arquivo .csv funcional com 12 meses | Prática | ✅ (`exemplos/`) |
| E08 | README com instruções de execução | Prática | ✅ |
| E09 | **Link do repositório GitHub** | Prática | 🟡 repositório local pronto; criar o remoto e enviar é com o Eduardo |
| E10 | PDF: análise do problema e regras | Teórica 25% | ✅ rascunho em `docs/parte-teorica/` |
| E11 | PDF: entradas, processamentos e saídas | Teórica | ✅ |
| E12 | PDF: fluxograma | Teórica | ✅ |
| E13 | PDF: estrutura de classes (atributos e métodos) | Teórica | ✅ |
| E14 | PDF: justificativa de pensamento algorítmico + POO | Teórica | ✅ |
| E15 | Documentação corresponde ao programa desenvolvido | Teórica | ✅ (gerada a partir do código final) |
| E16 | Vídeo pitch de até 4 min com tela (problema, fluxograma, classes, código, execução, CSV, POO) | Vídeo 25% | 🟡 roteiro em `docs/roteiro-video.md`; gravar e publicar é com o Eduardo |
| E17 | Vídeo publicado no YouTube (não listado) ou plataforma acessível | Vídeo | 🟡 Eduardo |
| E18 | Conferir que o link do repositório e do vídeo estão acessíveis antes de enviar | — | 🟡 Eduardo |

## D. Pontos que o documento não define (decisões tomadas e justificadas)

| # | Lacuna | Decisão |
|---|---|---|
| D01 | Estúdio tem opção de 2 quartos? | Não. O documento só fala em 2 quartos para apartamento e casa. |
| D02 | Estúdio pode ter "vaga de garagem" de R$ 300? | Não. Para estúdio a regra de estacionamento "será diferente": só o pacote de 2 vagas + vagas adicionais. |
| D03 | Vagas adicionais sem o pacote? | Não. As vagas adicionais complementam o "pacote inicial"; só são perguntadas se o cliente aceitar o pacote. |
| D04 | Quantas vagas de garagem para casa/apartamento? | Uma ("uma vaga de garagem"). |
| D05 | O desconto de 5% incide sobre a garagem? | Sim. O desconto vem "após a aplicação dos adicionais correspondentes"; quarto extra e garagem são os adicionais do apartamento. |
| D06 | Juros no parcelamento da taxa? | Não há. O documento não fala em juros. |
| D07 | Divisão que não dá centavos exatos (ex.: 3x) | Os centavos que sobram vão para as primeiras parcelas: 3x = 666,67 + 666,67 + 666,66 (soma exata R$ 2.000,00). |
| D08 | Em que meses a taxa é cobrada na projeção? | Nos primeiros meses do contrato (parcela 1 no mês 1, até a parcela N no mês N). |
| D09 | Formato do CSV | Separador `;`, vírgula decimal e UTF-8 com BOM, para abrir direto no Excel em português. Uma linha por mês (12) + linha TOTAL. |
| D10 | Prazo de entrega | Não consta no documento: confirmar no AVA. |
