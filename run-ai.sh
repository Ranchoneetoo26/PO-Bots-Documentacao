#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Uso: bash ./run-ai.sh \"TASK\" [TOKEN_OPCIONAL]"
  exit 1
fi

TASK="$1"
TOKEN="${2:-${POBOTS_API_TOKEN:-}}"
MODEL="${POBOTS_MODEL:-gpt-4o-mini}"
API_BASE_URL="${POBOTS_API_BASE_URL:-https://api.openai.com/v1}"
INTERACTIVE_FLAG="${POBOTS_INTERACTIVE_FLAG:---interactive}"

echo "==> PO Bots AI: comando unico (token + task)"

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

if [[ ! -d ".venv" ]]; then
  echo "==> Criando ambiente virtual (.venv)"
  "${PY_CMD}" -m venv .venv
fi

if [[ -f ".venv/Scripts/activate" ]]; then
  source ".venv/Scripts/activate"
elif [[ -f ".venv/bin/activate" ]]; then
  source ".venv/bin/activate"
else
  echo "ERRO: nao foi possivel localizar script de ativacao do venv."
  exit 1
fi

echo "==> Instalando dependencias"
python -m pip install -r requirements.txt
export PYTHONPATH="$(pwd)/src${PYTHONPATH+:$PYTHONPATH}"

if [[ -z "${TOKEN}" ]]; then
  echo "ERRO: token nao informado. Passe como 2o argumento ou exporte POBOTS_API_TOKEN."
  exit 1
fi
export POBOTS_API_TOKEN="${TOKEN}"

echo "==> Executando pipeline de IA"
python -m pobots.cli ai-generate \
  "${TASK}" \
  --model "${MODEL}" \
  --api-base-url "${API_BASE_URL}" \
  ${INTERACTIVE_FLAG}

echo ""
echo "Concluido com sucesso."
echo "Resultado em pasta nova dentro de: dist"
echo "Use 06-backlog/cards-trello.md para copiar/colar no Trello/Jira."
