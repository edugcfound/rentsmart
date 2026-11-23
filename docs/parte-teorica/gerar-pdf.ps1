# Gera o PDF da parte teórica a partir de parte-teorica.html usando o Microsoft Edge (modo headless).
# Uso (na pasta do projeto):  powershell -ExecutionPolicy Bypass -File docs\parte-teorica\gerar-pdf.ps1
# Rode de novo sempre que editar o HTML (por exemplo depois de preencher o professor e o link do GitHub).
$dir  = $PSScriptRoot
$out  = Join-Path $dir "Parte Teorica - RentSmart - Eduardo.pdf"
$src  = "file:///" + ((Join-Path $dir "parte-teorica.html") -replace '\\','/' -replace ' ','%20')
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
$prof = Join-Path $env:TEMP "edge-pdf-rentsmart"
# O Edge grava primeiro na pasta temporaria e depois o arquivo e movido (evita falha do Edge com caminhos muito longos).
$tmp  = Join-Path $env:TEMP "rentsmart-parte-teorica.pdf"
Remove-Item $tmp -ErrorAction SilentlyContinue
$p = Start-Process -FilePath $edge -ArgumentList "--headless=new","--disable-gpu","--no-first-run","--user-data-dir=`"$prof`"","--no-pdf-header-footer","--allow-file-access-from-files","--print-to-pdf=`"$tmp`"","`"$src`"" -Wait -PassThru -WindowStyle Hidden
if ($p.ExitCode -ne 0 -or -not (Test-Path $tmp)) { throw "O Edge nao gerou o PDF (codigo $($p.ExitCode))." }
Move-Item $tmp $out -Force
"PDF gerado: $out ({0:N0} KB)" -f ((Get-Item $out).Length/1KB)
