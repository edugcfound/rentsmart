# O que falta para entregar (só o Eduardo pode fazer)

Tudo o que é código, teste, README, fluxograma e PDF teórico já está pronto, commitado e publicado
em https://github.com/edugcfound/rentsmart. Faltam os passos que dependem da sua conta e da sua voz:

1. **Confirmar o prazo no AVA** — o documento do trabalho não informa a data.
2. **Nome do professor(a) na capa do PDF** — abrir `docs/parte-teorica/parte-teorica.html` num editor,
   trocar o texto `preencher` (na capa) pelo nome e salvar. Depois gerar o PDF de novo e enviar:

   ```powershell
   powershell -ExecutionPolicy Bypass -File docs\parte-teorica\gerar-pdf.ps1
   ```

   e em seguida `git add -A`, `git commit -m "docs: nome do professor na capa"`, `git push`.
3. ~~Criar o repositório no GitHub e enviar o projeto~~ — **feito em 2026-11-23**: https://github.com/edugcfound/rentsmart (público).
   O link já está no PDF. Para enviar mudanças futuras: `git add -A`, `git commit -m "mensagem"`, `git push`.
4. **Gravar o vídeo** seguindo `docs/roteiro-video.md` (até 4 min), publicar no YouTube como
   **Não listado** e testar o link numa janela anônima.
5. **Enviar no AVA**: o PDF `docs/parte-teorica/Parte Teorica - RentSmart - Eduardo.pdf`, o link do
   repositório e o link do vídeo.
