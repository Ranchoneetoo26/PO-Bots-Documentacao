param(
    [string]$ProjectFile = "project.yaml",
    [string]$DistDir = "dist"
)

$ErrorActionPreference = "Stop"

Write-Host "==> PO Bots: bootstrap + pipeline completo"

function Invoke-Step {
    param([scriptblock]$Script, [string]$ErrorMessage)
    & $Script
    if ($LASTEXITCODE -ne 0) {
        throw $ErrorMessage
    }
}

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) { return "py" }
    if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
    if (Get-Command python3 -ErrorAction SilentlyContinue) { return "python3" }
    throw "Python nao encontrado. Instale Python 3.10+ e tente novamente."
}

$PythonCmd = Get-PythonCommand
Write-Host "==> Usando interpretador: $PythonCmd"

if (!(Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "==> Criando ambiente virtual (.venv)"
    & $PythonCmd -m venv .venv
}

$ResolvedVenvPython = Resolve-Path ".venv\Scripts\python.exe" -ErrorAction SilentlyContinue
if (!$ResolvedVenvPython) {
    throw "Nao foi possivel localizar .venv\Scripts\python.exe"
}
$VenvPython = $ResolvedVenvPython.Path

Write-Host "==> Instalando/atualizando dependencias"
Invoke-Step { & $VenvPython -m pip install -r requirements.txt } "Falha ao instalar dependencias."
$ResolvedSrc = Resolve-Path ".\src" -ErrorAction SilentlyContinue
if (!$ResolvedSrc) { throw "Pasta src nao encontrada." }
$env:PYTHONPATH = "$($ResolvedSrc.Path);$($env:PYTHONPATH)"

if (!(Test-Path $ProjectFile)) {
    Write-Host "==> $ProjectFile nao existe. Criando com base padrao..."
    Invoke-Step { & $VenvPython -m pobots.cli init --output $ProjectFile } "Falha ao criar project.yaml."
}
else {
    Write-Host "==> $ProjectFile ja existe. Reutilizando arquivo atual."
}

Write-Host "==> Rodando doctor"
Invoke-Step { & $VenvPython -m pobots.cli doctor --project-file $ProjectFile } "Falha no doctor."

Write-Host "==> Gerando artefatos"
Invoke-Step { & $VenvPython -m pobots.cli generate --project-file $ProjectFile --dist-dir $DistDir } "Falha no generate."

Write-Host "==> Validando qualidade"
Invoke-Step { & $VenvPython -m pobots.cli validate --dist-dir $DistDir } "Falha no validate."

Write-Host "==> Exportando cards"
Invoke-Step { & $VenvPython -m pobots.cli export --dist-dir $DistDir } "Falha no export."

Write-Host ""
Write-Host "Concluido com sucesso."
Write-Host "Arquivos prontos em: $DistDir"
Write-Host "Use cards-trello.md e cards-copy-paste.txt para copiar/colar no Trello/Jira."
