# PO-Bots-Documentacao

Framework de bots de IA para criar documentacao de projeto de forma profissional, com foco em:
- clareza total;
- rastreabilidade;
- padrao executivo;
- cards prontos para copiar e colar no Trello/Jira.

## Importante (estado atual)
Hoje o projeto esta em **modo manual assistido por IA**:
- os bots **geram** toda a documentacao e os cards completos;
- voce **copia e cola** no Trello/Jira;
- nao existe integracao automatica ativa com Trello neste momento.

---

## O que voce encontra neste repositorio
- `bots/framework-bots-base-documental.md`  
  Base metodologica (logica de DVP-E, DVS, DRP, DAT, GDR).

- `bots/prompts/prompt-mestre-bots-universal-v2.md`  
  Prompt principal para rodar os bots em qualquer projeto.

- `bots/prompts/prompt-pack-bots.md`  
  Prompt por papel (CEO, Analista, Arquiteto, Dev Back, Dev Front, QA, Compliance, PM).

- `bots/protocolo-handoff-bots.md`  
  Ordem de trabalho entre bots, gates e bloqueios.

- `bots/aprendizado-continuo-ia.md`  
  Como os bots melhoram entre projetos (memoria e licoes aprendidas).

- `analise-alinhamento-e-divergencia.md`  
  Auditoria de alinhamento com a base documental.

- `publish-to-github.ps1`  
  Script utilitario para publicar no GitHub.

---

## Para quem e este repositório
Este material foi feito para:
- Product Owner / PM;
- Analista;
- Arquiteto;
- QA;
- Dev Back e Dev Front;
- qualquer pessoa que precise transformar ideia em documentacao executavel.

Mesmo quem tem pouca experiencia tecnica consegue usar, seguindo os passos abaixo.

---

## Requisitos minimos
Voce precisa de:
1. Uma conta no ChatGPT (ou outra IA compativel com prompts longos).
2. Um board no Trello ou projeto no Jira.
3. VSCode (opcional, para editar arquivos com mais conforto).

---

## Guia rapido (5 minutos)
1. Abra o arquivo `bots/prompts/prompt-mestre-bots-universal-v2.md`.
2. Copie todo o conteudo.
3. Abra o ChatGPT.
4. Cole o prompt.
5. Envie uma mensagem com o contexto do seu novo projeto.
6. Receba a documentacao + cards prontos.
7. Copie e cole os cards no Trello/Jira.

---

## Passo a passo detalhado (para leigo)

### Etapa 1 - Abrir o prompt certo
1. Abra a pasta do projeto no seu computador.
2. Entre em `bots` -> `prompts`.
3. Clique em `prompt-mestre-bots-universal-v2.md`.
4. Selecione tudo (`Ctrl + A`) e copie (`Ctrl + C`).

### Etapa 2 - Rodar no ChatGPT
1. Abra o ChatGPT no navegador.
2. Clique em `Novo chat`.
3. Cole o prompt inteiro (`Ctrl + V`).
4. No final, adicione seu contexto de projeto, por exemplo:
   - nome do projeto;
   - objetivo;
   - publico-alvo;
   - prazo;
   - stack desejada.
5. Clique em `Enviar`.

### Etapa 3 - Receber a saida correta
A IA deve entregar:
- documento mestre;
- RF e RNF;
- arquitetura;
- checklists;
- criterios Gherkin;
- cards completos para Trello/Jira.

Se vier incompleto, responda:
`Refaça no formato completo com checklist tecnico, checklist QA e Gherkin para cada RF.`

### Etapa 4 - Levar para Trello/Jira (manual)
1. Abra seu Trello.
2. Entre no board da sprint.
3. Clique em `Adicionar card`.
4. Cole o titulo e a descricao completa do card gerado.
5. Repita para todos os cards.
6. Adicione labels e responsavel.

Sugestao de listas no Trello:
- Backlog
- Refino
- Ready
- In Progress
- Code Review
- QA
- Done
- Blocked

### Etapa 5 - Garantir qualidade antes de executar
Antes de comecar a sprint, verifique se cada card tem:
- objetivo;
- escopo e fora de escopo;
- regras executaveis;
- checklist tecnico;
- checklist QA;
- criterios de aceite (Gherkin).

Se faltar qualquer item, volte ao bot e peça complemento.

---

## Como os bots trabalham juntos
Ordem oficial:
1. Analista
2. Arquiteto
3. CEO
4. Dev Back
5. Dev Front
6. QA
7. Compliance
8. PM

Regra de gate:
- `OK`: segue.
- `PENDENTE`: corrige e roda de novo.
- `BLOQUEADO`: para tudo, corrige causa raiz.

Detalhes em: `bots/protocolo-handoff-bots.md`.

---

## Modelo de comando para iniciar qualquer projeto
Use este texto apos colar o prompt mestre:

```txt
Projeto: [nome]
Objetivo: [objetivo]
Publico: [publico-alvo]
Prazo: [prazo]
Stack: [stack desejada]
Restricoes: [restricoes]

Execute Fase 1 a 5 e entregue:
- Documento mestre completo
- RF/RNF completos
- Checklist tecnico + QA
- Gherkin por RF
- Cards completos para copiar e colar no Trello
```

---

## Aprendizado continuo (melhoria constante)
Para os bots evoluirem com o tempo:
1. Ao fim de cada sprint, registre:
   - ambiguidades;
   - retrabalho;
   - bugs;
   - estimativas ruins;
   - decisoes que funcionaram.
2. Salve isso em um arquivo ou Notion.
3. Na proxima execucao, cole essas licoes no contexto inicial.

Guia completo: `bots/aprendizado-continuo-ia.md`.

---

## O que NAO fazer
- Nao usar card sem Gherkin.
- Nao usar card com frase vaga.
- Nao aprovar card sem checklist QA.
- Nao mudar regra sem atualizar rastreabilidade.

---

## Checklist final de uso
- [ ] Prompt mestre copiado
- [ ] Contexto do projeto enviado
- [ ] Saida completa recebida
- [ ] Cards colados no Trello/Jira
- [ ] Checklists e Gherkin revisados
- [ ] Sprint iniciada com cards claros

---

## Publicar atualizacao no GitHub
Se voce alterar qualquer arquivo e quiser subir:

```powershell
cd "c:\Users\Antonio\Desktop\Projeto-CarWash\PO-Bots-Documentacao"
git add .
git commit -m "docs: atualiza modo manual e guia passo a passo"
git push
```

---

## Suporte de uso
Se um bot estiver gerando saida fraca, rode novamente com este reforco:
`Responda com nivel senior, sem ambiguidade, checklist tecnico + QA + criterios Gherkin por RF.`
