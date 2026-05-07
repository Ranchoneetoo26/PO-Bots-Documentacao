# INICIAR-AQUI (3 minutos)

Este projeto gera documentacao e cards profissionais com Python.
Regra fixa: sem envio automatico para Trello/Jira. O sistema gera tudo para copiar e colar.

## 1) Abrir terminal na pasta do projeto
```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
```

## 2) Rodar em comando unico (recomendado)
```powershell
.\run-all.ps1
```

Se estiver usando Git Bash:
```bash
bash ./run-all.sh
```

## 3) Criar arquivo base do projeto (opcional manual)
```powershell
python -m pobots.cli init
```

## 4) Editar o arquivo project.yaml
Preencha nome do projeto, objetivo, RF, RNF e regras.

## 5) Gerar artefatos
```powershell
python -m pobots.cli generate
python -m pobots.cli validate
python -m pobots.cli export
```

Se quiser gerar com IA + token do cliente:
```powershell
$env:POBOTS_API_TOKEN="SEU_TOKEN"
$env:PYTHONPATH=(Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m pobots.cli ai-generate "Task do cliente"
```

## 6) Usar resultado
Arquivos gerados em uma pasta nova por execucao:
- `dist/gerado-<projeto>-<timestamp>/documento-mestre.md`
- `dist/gerado-<projeto>-<timestamp>/01-dvp-e/dvp-e.md`
- `dist/gerado-<projeto>-<timestamp>/02-dvs/dvs.md`
- `dist/gerado-<projeto>-<timestamp>/03-drp/drp.md`
- `dist/gerado-<projeto>-<timestamp>/04-dat/dat.md`
- `dist/gerado-<projeto>-<timestamp>/05-gdr/gdr.md`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards-trello.md`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards-copy-paste.txt`

Agora e so copiar e colar os cards no Trello/Jira.

## Se aparecer "pobots: command not found"
- Nao tem problema.
- Use sempre `python -m pobots.cli ...` ou rode `run-all.ps1` / `run-all.sh`.
- Esse erro acontece quando o terminal nao encontrou o executavel `pobots` no PATH.
