#!/usr/bin/env bash
set -euo pipefail

echo "==> PO Bots: bootstrap + pipeline completo"

if command -v py >/dev/null 2>&1; then
  PY_CMD="py"
elif command -v python >/dev/null 2>&1; then
  PY_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
  PY_CMD="python3"
else
  echo "ERRO: Python nao encontrado. Instale Python 3.10+ e tente novamente."
  exit 1
fi

echo "==> Usando interpretador: ${PY_CMD}"

if [[ ! -d ".venv" ]]; then
  echo "==> Criando ambiente virtual (.venv)"
  "${PY_CMD}" -m venv .venv
fi

if [[ -f ".venv/Scripts/activate" ]]; then
  # Git Bash no Windows
  source ".venv/Scripts/activate"
elif [[ -f ".venv/bin/activate" ]]; then
  # Linux/macOS
  source ".venv/bin/activate"
else
  echo "ERRO: nao foi possivel localizar script de ativacao do venv."
  exit 1
fi

echo "==> Instalando/atualizando dependencias"
python -m pip install -r requirements.txt
export PYTHONPATH="$(pwd)/src${PYTHONPATH+:$PYTHONPATH}"

if [[ ! -f "project.yaml" ]]; then
  echo "==> project.yaml nao existe. Criando com base padrao..."
  python -m pobots.cli init --output project.yaml
else
  echo "==> project.yaml ja existe. Reutilizando arquivo atual."
fi

echo "==> Rodando doctor"
python -m pobots.cli doctor --project-file project.yaml

echo "==> Gerando artefatos"
python -m pobots.cli generate --project-file project.yaml --dist-dir dist

echo "==> Validando qualidade"
python -m pobots.cli validate --dist-dir dist

echo "==> Exportando cards"
python -m pobots.cli export --dist-dir dist

echo ""
echo "Concluido com sucesso."
echo "Arquivos prontos em: dist/"
echo "Use dist/cards-trello.md e dist/cards-copy-paste.txt para copiar/colar no Trello/Jira."
