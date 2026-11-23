# Roteiro do vídeo pitch (até 4 minutos)

O enunciado pede: gravação de tela de **até 4 minutos**, publicada no YouTube (de preferência
**não listado**) ou em outra plataforma com acesso para avaliação. Precisa mostrar os 7 itens
marcados com ✔ abaixo.

Ferramenta sugerida no Windows 10: **Xbox Game Bar** (`Win + G` → botão gravar; `Win + Alt + R`
começa/para). Ela grava uma janela por vez, então deixe abertos o VS Code (com o terminal dentro dele)
e o PDF. Outra opção é o OBS Studio.

Antes de gravar:

- Abra a pasta do projeto no VS Code e apague a pasta `saida/` (para o CSV ser criado na hora).
- Deixe abertos: `docs/fluxograma.png`, `rentsmart/imoveis.py` e o terminal do VS Code.
- Aumente a fonte do terminal e do editor (`Ctrl` + `+`), para ficar legível no vídeo.

| Tempo | O que mostrar na tela | O que falar (sugestão) | Item do enunciado |
|---|---|---|---|
| 0:00–0:30 | README ou capa do PDF | "A R.M Imóveis calculava orçamentos de aluguel à mão, com risco de erro em adicionais, descontos e taxa. O RentSmart automatiza isso: recebe as escolhas do cliente, aplica as regras e gera a projeção de 12 meses." | ✔ problema |
| 0:30–1:05 | `docs/fluxograma.png` | Percorrer o fluxo: lê nome e tipo; casa e apartamento perguntam quartos e garagem; só apartamento pergunta crianças; estúdio pergunta estacionamento; depois parcelas, cálculo, resumo, CSV e "outro orçamento?". Toda resposta inválida é recusada e a pergunta se repete. | ✔ fluxograma e lógica |
| 1:05–1:40 | README, seção "Estrutura de classes" | `Imovel` é abstrata; `ImovelComQuartos` junta a regra de quarto e garagem; `Apartamento`, `Casa` e `Estudio` só guardam seus valores. `TaxaContratual` divide os R$ 2.000; `Orcamento` junta tudo; `ExportadorCSV` grava; `InterfaceConsole` conversa com o usuário. | ✔ estrutura de classes |
| 1:40–2:20 | `rentsmart/imoveis.py` | Mostrar `valor_mensal()` (soma da composição, escrito uma vez só), a property `quartos` com validação e o `_calcular_descontos` do `Apartamento` com os 5% depois dos adicionais. Rápido em `taxa_contratual.py`: divisão em centavos. | ✔ principais trechos |
| 2:20–3:20 | Terminal: `python main.py` | Fazer um orçamento completo. Sugestão: Apartamento, 2 quartos, garagem S, crianças N, taxa em 5x. Digitar **uma resposta errada de propósito** (ex.: `3` quartos) para mostrar a validação. Ler o resumo: 700 + 200 + 300 = 1.200, menos 5% = **R$ 1.140,00**; taxa separada: 5x de R$ 400,00. | ✔ execução com orçamento completo |
| 3:20–3:40 | Abrir o CSV da pasta `saida/` (Excel ou VS Code) | 12 meses; nos 5 primeiros entra a parcela de R$ 400; total do ano R$ 15.680,00. | ✔ CSV gerado |
| 3:40–4:00 | Tela do código ou README | "A Orientação a Objetos deixou cada regra em um lugar só: se o valor da garagem mudar, muda uma linha. Herança evitou repetir casa e apartamento, e o polimorfismo deixa o orçamento calcular qualquer imóvel do mesmo jeito." | ✔ contribuição da POO |

Depois de gravar:

1. Conferir se o vídeo tem **no máximo 4:00**.
2. Publicar no YouTube como **Não listado** e copiar o link.
3. Abrir o link numa janela anônima para conferir que abre sem login.
