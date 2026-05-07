# INICIAR-AQUI (3 minutos)

Este projeto gera documentacao e cards profissionais com Python.
Regra fixa: sem envio automatico para Trello/Jira. O sistema gera tudo para copiar e colar.

## 1) Abrir terminal na pasta do projeto
```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
```

## 2) Criar ambiente Python e instalar dependencias
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## 3) Criar arquivo base do projeto
```powershell
pobots init
```

## 4) Editar o arquivo project.yaml
Preencha nome do projeto, objetivo, RF, RNF e regras.

## 5) Gerar artefatos
```powershell
pobots generate
pobots validate
pobots export
```

## 6) Usar resultado
Arquivos gerados em `dist/`:
- `documento-mestre.md`
- `catalogo-rf-rnf.md`
- `cards-trello.md`
- `cards.json`
- `qualidade-validacao.md`
- `cards-trello.csv`
- `cards-copy-paste.txt`

Agora e so copiar e colar os cards no Trello/Jira.
