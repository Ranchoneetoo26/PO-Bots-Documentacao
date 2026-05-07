param(
  [Parameter(Mandatory=$true)]
  [string]$GithubUser
)

$ErrorActionPreference = "Stop"
$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoPath

$remoteUrl = "https://github.com/$GithubUser/PO-Bots-Documentacao.git"

if (-not (git rev-parse --is-inside-work-tree 2>$null)) {
  throw "Pasta não é um repositório git."
}

$hasOrigin = (git remote) -contains "origin"
if ($hasOrigin) {
  git remote set-url origin $remoteUrl
} else {
  git remote add origin $remoteUrl
}

git branch -M main
git push -u origin main

Write-Host ""
Write-Host "Publicação concluída com sucesso em $remoteUrl"
