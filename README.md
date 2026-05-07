# PO-Bots-Documentacao

Plataforma de bots para gerar documentacao de projeto e backlog profissional.

## Regra mais importante
Este projeto **nao envia nada automaticamente para Trello/Jira**.
Ele gera cards completos para **copiar e colar**.

## Resultado que voce recebe
Ao rodar a CLI, voce recebe:
- documento mestre;
- catalogo RF/RNF;
- cards detalhados por RF;
- checklist tecnico e QA por card;
- criterios Gherkin por card;
- relatorio de qualidade com score;
- arquivos CSV/TXT para uso manual.

## Modo de uso para leigo (clone e usa)
1. Clone o repositorio.
2. Abra terminal na pasta.
3. Instale dependencias.
4. Rode `pobots init`.
5. Preencha `project.yaml`.
6. Rode `pobots generate`.
7. Rode `pobots validate`.
8. Rode `pobots export`.
9. Copie e cole no Trello/Jira.

Guia ultra rapido: `INICIAR-AQUI.md`.

---

## Instalacao (Windows PowerShell)
```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Comandos principais
### 1) Criar arquivo base do projeto
```powershell
pobots init
```

### 2) Gerar documentacao e cards
```powershell
pobots generate
```

### 3) Validar qualidade (score por card)
```powershell
pobots validate
```

### 4) Exportar para operacao manual
```powershell
pobots export
```

### 5) Diagnostico rapido
```powershell
pobots doctor
```

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
- `documento-mestre.md`
- `catalogo-rf-rnf.md`
- `cards-trello.md`
- `cards.json`
- `prompt-ia-copiar-colar.md`
- `qualidade-validacao.md`
- `qualidade-validacao.json`
- `cards-trello.csv`
- `cards-copy-paste.txt`

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

### Posso usar em qualquer tipo de projeto?
Sim. O framework e universal e orientado por documentos base.

### Posso incluir IA no fluxo?
Sim. Use o arquivo `dist/prompt-ia-copiar-colar.md` para acelerar refinamento.

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
