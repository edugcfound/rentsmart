# O que falta para entregar (só o Eduardo pode fazer)

Tudo o que é código, teste, README, fluxograma e PDF teórico já está pronto e commitado no git
**local**. Faltam os passos que dependem da sua conta e da sua voz:

1. **Confirmar o prazo no AVA** — o documento do trabalho não informa a data.
2. **Nome do professor(a) na capa do PDF** — abrir `docs/parte-teorica/parte-teorica.html` num editor,
   trocar o texto `preencher` (na capa) pelo nome e salvar.
3. **Criar o repositório no GitHub e enviar o projeto**
   1. Entrar em https://github.com/new, nome sugerido `rentsmart`, visibilidade **Public** (para o
      professor conseguir abrir), **sem** marcar README/.gitignore/licença (o projeto já tem).
   2. No PowerShell, dentro da pasta do projeto, colar os comandos que o GitHub mostra em
      "…or push an existing repository from the command line". Eles são parecidos com:

      ```powershell
      git remote add origin https://github.com/SEU-USUARIO/rentsmart.git
      git push -u origin main
      ```

   3. Abrir o link do repositório numa janela anônima e conferir que o README aparece.
4. **Link do GitHub no PDF** — no mesmo `parte-teorica.html`, trocar `colar aqui o link do GitHub`
   pelo link. Depois gerar o PDF de novo:

   ```powershell
   powershell -ExecutionPolicy Bypass -File docs\parte-teorica\gerar-pdf.ps1
   ```

   E registrar a mudança: `git add -A`, `git commit -m "docs: professor e link do repositório"`, `git push`.
5. **Gravar o vídeo** seguindo `docs/roteiro-video.md` (até 4 min), publicar no YouTube como
   **Não listado** e testar o link numa janela anônima.
6. **Enviar no AVA**: o PDF `docs/parte-teorica/Parte Teorica - RentSmart - Eduardo.pdf`, o link do
   repositório e o link do vídeo.
