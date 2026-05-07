param(
    [Parameter(Mandatory = $true)]
    [string]$Task,
    [string]$Token = "",
    [string]$Model = "gpt-4o-mini",
    [string]$ApiBaseUrl = "https://api.openai.com/v1",
    [string]$ProjectFile = "project.yaml",
    [string]$DistDir = "dist",
    [switch]$AutoDecide
)

$ErrorActionPreference = "Stop"

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

Write-Host "==> PO Bots AI: comando unico (token + task)"
$PythonCmd = Get-PythonCommand

if (!(Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "==> Criando ambiente virtual (.venv)"
    & $PythonCmd -m venv .venv
}

$ResolvedVenvPython = Resolve-Path ".venv\Scripts\python.exe" -ErrorAction SilentlyContinue
if (!$ResolvedVenvPython) {
    throw "Nao foi possivel localizar .venv\Scripts\python.exe"
}
$VenvPython = $ResolvedVenvPython.Path

Write-Host "==> Instalando dependencias"
Invoke-Step { & $VenvPython -m pip install -r requirements.txt } "Falha ao instalar dependencias."

$ResolvedSrc = Resolve-Path ".\src" -ErrorAction SilentlyContinue
if (!$ResolvedSrc) { throw "Pasta src nao encontrada." }
$env:PYTHONPATH = "$($ResolvedSrc.Path);$($env:PYTHONPATH)"

if ($Token.Trim()) {
    $env:POBOTS_API_TOKEN = $Token
}
if (!($env:POBOTS_API_TOKEN) -or !($env:POBOTS_API_TOKEN.Trim())) {
    throw "Token nao informado. Use -Token ou variavel POBOTS_API_TOKEN."
}

$InteractiveFlag = "--interactive"
if ($AutoDecide.IsPresent) {
    $InteractiveFlag = "--auto-decide"
}

Write-Host "==> Executando pipeline de IA"
Invoke-Step {
    & $VenvPython -m pobots.cli ai-generate `
        "$Task" `
        --model "$Model" `
        --api-base-url "$ApiBaseUrl" `
        --project-file "$ProjectFile" `
        --dist-dir "$DistDir" `
        $InteractiveFlag
} "Falha no pipeline de IA."

Write-Host ""
Write-Host "Concluido com sucesso."
Write-Host "Resultado em pasta nova dentro de: $DistDir"
Write-Host "Use 06-backlog/cards-trello.md para copiar/colar no Trello/Jira."
