# PO-Bots-Documentacao

Plataforma de bots para gerar documentacao de projeto e backlog profissional.

## Regra mais importante
Este projeto **nao envia nada automaticamente para Trello/Jira**.
Ele gera cards completos para **copiar e colar**.

## Resultado que voce recebe
Ao rodar a CLI, voce recebe:
- documento mestre;
- documentos separados por bloco (`dvp-e`, `dvs`, `drp`, `dat`, `gdr`);
- cards detalhados por RF;
- checklist tecnico e QA por card;
- criterios Gherkin por card;
- relatorio de qualidade com score;
- arquivos CSV/TXT para uso manual.

Cada execucao cria uma pasta nova, para nao misturar com arquivos anteriores.

## Modo de uso para leigo (clone e usa)
1. Clone o repositorio.
2. Abra terminal na pasta.
3. Rode **um comando unico** (`run-all.sh` no Git Bash ou `run-all.ps1` no PowerShell).
4. Preencha `project.yaml`.
5. Rode novamente o comando unico para gerar tudo.
9. Copie e cole no Trello/Jira.

Guia ultra rapido: `INICIAR-AQUI.md`.

---

## Instalacao (Windows PowerShell)
```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
.\run-all.ps1
```

## Instalacao (Git Bash)
```bash
cd ~/Desktop/Projeto-PO/PO-Bots-Documentacao
bash ./run-all.sh
```

## Comandos principais
### 0) Comando unico (recomendado)
```powershell
.\run-all.ps1
```
```bash
bash ./run-all.sh
```

### 0.1) Ambiente manual (somente se precisar)
```powershell
$env:PYTHONPATH=(Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m pobots.cli doctor
```
```bash
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
python -m pobots.cli doctor
```

### 1) Criar arquivo base do projeto
```powershell
.\.venv\Scripts\python.exe -m pobots.cli init
```

### 2) Gerar documentacao e cards
```powershell
.\.venv\Scripts\python.exe -m pobots.cli generate
```

### 3) Validar qualidade (score por card)
```powershell
.\.venv\Scripts\python.exe -m pobots.cli validate
```

### 4) Exportar para operacao manual
```powershell
.\.venv\Scripts\python.exe -m pobots.cli export
```

### 5) Diagnostico rapido
```powershell
.\.venv\Scripts\python.exe -m pobots.cli doctor
```

### 6) Pipeline com IA + token do cliente
```powershell
$env:POBOTS_API_TOKEN="SEU_TOKEN_AQUI"
.\.venv\Scripts\python.exe -m pobots.cli ai-generate "Task do cliente: criar fluxo de cadastro e agendamento"
```
```bash
export POBOTS_API_TOKEN="SEU_TOKEN_AQUI"
python -m pobots.cli ai-generate "Task do cliente: criar fluxo de cadastro e agendamento"
```

Esse comando executa o fluxo:
- cliente informa task;
- IA faz perguntas de detalhamento;
- cliente responde (ou deixa IA decidir);
- IA combina a task com nossos prompts oficiais;
- IA gera `project.yaml`;
- sistema gera DVP-E, DVS, DRP, DAT, GDR e backlog completo.

---

## Estrutura do repositorio
- `src/pobots/cli.py`: comandos da CLI.
- `src/pobots/generator.py`: geracao de documentos e cards.
- `src/pobots/validator.py`: score de qualidade e gates.
- `src/pobots/exporter.py`: exportacao CSV/TXT.
- `bots/framework-bots-base-documental.md`: modelo metodologico universal.
- `bots/prompts/prompt-mestre-bots-universal-v2.md`: prompt principal.
- `bots/prompts/prompt-pack-bots.md`: prompts por papel.
- `bots/protocolo-handoff-bots.md`: regras de handoff e gate.

---

## Arquivo project.yaml (entrada padrao)
O comando `pobots init` cria um modelo pronto.
Voce pode editar:
- dados do projeto;
- lista de RF;
- lista de RNF;
- regras de negocio;
- criterios de aceite.

Quanto melhor o `project.yaml`, melhor a qualidade final dos cards.

---

## Saida gerada em dist/
- `dist/gerado-<projeto>-<timestamp>/documento-mestre.md`
- `dist/gerado-<projeto>-<timestamp>/01-dvp-e/dvp-e.md`
- `dist/gerado-<projeto>-<timestamp>/02-dvs/dvs.md`
- `dist/gerado-<projeto>-<timestamp>/03-drp/drp.md`
- `dist/gerado-<projeto>-<timestamp>/04-dat/dat.md`
- `dist/gerado-<projeto>-<timestamp>/05-gdr/gdr.md`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards-trello.md`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards.json`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/qualidade-validacao.md`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards-trello.csv`
- `dist/gerado-<projeto>-<timestamp>/06-backlog/cards-copy-paste.txt`

## Como usar no Trello/Jira
1. Abra seu board.
2. Crie um card.
3. Copie o titulo e a descricao de `cards-trello.md` ou `cards-copy-paste.txt`.
4. Cole no card.
5. Repita para os demais.

---

## Gates de qualidade
Cada card recebe score de 0 a 100.
- `>= 85`: OK
- `70 a 84`: PENDENTE
- `< 70`: BLOQUEADO

Validacao considera:
- checklist tecnico;
- checklist QA;
- estrutura Gherkin;
- regras de negocio;
- labels.

---

## Perguntas frequentes
### O sistema publica no Trello automaticamente?
Nao. Ele gera material pronto para copiar e colar.

### Deu erro `pobots: command not found`. E agora?
Use `python -m pobots.cli ...` no lugar de `pobots ...`, ou rode diretamente:
```powershell
.\run-all.ps1
```
```bash
bash ./run-all.sh
```
Esses scripts nao dependem do `PATH` do comando `pobots`.

### Posso usar em qualquer tipo de projeto?
Sim. O framework e universal e orientado por documentos base.

### Posso incluir IA no fluxo?
Sim. Voce pode usar:
- `python -m pobots.cli ai-generate "sua task"` para pipeline automatizado com token.
- `dist/.../06-backlog/prompt-ia-copiar-colar.md` para refinamento manual.

---

## Roadmap sugerido (empresa)
- adicionar dashboard web com FastAPI;
- multi-tenant (um workspace por cliente);
- historico de score por sprint;
- portal de templates por segmento;
- pacote enterprise com branding.

---

## Publicar alteracoes no GitHub
```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
git add .
git commit -m "feat: automacao local python para geracao de cards"
git push
```
