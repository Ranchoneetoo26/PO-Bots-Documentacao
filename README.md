# PO-Bots-Documentacao

Framework de bots de IA para criação e governança de documentação de projetos de software, com rastreabilidade ponta a ponta e **modo manual de operação**.

## O que este repositório entrega
- Arquitetura de bots por papéis (CEO, Analista, Arquiteto, Dev Back, Dev Front, QA, Compliance, PM).
- Prompt mestre universal para qualquer projeto.
- Protocolo de handoff e regras de gate entre bots.
- Geração de cards completos prontos para copiar e colar no Trello/Jira.
- Guia para evolução futura para automação (opcional).
- Auditoria de alinhamento com base metodológica documental.

## Estrutura
- `bots/framework-bots-base-documental.md`  
  Base metodológica (DVP-E, DVS, DRP, DAT, GDR).
- `bots/prompts/prompt-mestre-bots-universal-v2.md`  
  Prompt principal para iniciar qualquer projeto.
- `bots/prompts/prompt-pack-bots.md`  
  Prompts por papel.
- `bots/protocolo-handoff-bots.md`  
  Ordem, gates e bloqueios.
- `n8n-workflow-po-bots-orchestrator.json`  
  Referência técnica para automação futura (não obrigatório no modo atual).
- `trello-butler-regras-prontas.md`  
  Referência técnica para automação futura (não obrigatório no modo atual).
- `automacao-bots-trello-playbook.md`  
  Guia operacional completo.
- `analise-alinhamento-e-divergencia.md`  
  Verificação de consistência.

## Plataformas recomendadas (modo atual)
- **Editor:** VSCode
- **Board:** Trello/Jira (uso manual)
- **IA:** OpenAI API (ou equivalente)
- **Memória de aprendizado:** Notion/Google Sheets/Markdown versionado (recomendado)

## Pré-requisitos (modo atual)
1. Board Trello/Jira criado.
2. Chave de API de IA (ou uso manual em Chat/LLM).
3. Templates de card e checklists deste repositório.

## Instalação e uso (passo a passo - modo manual)
## 1) Preparar board
1. Criar listas:
   - `Backlog Sprint`, `Refino`, `Ready`, `In Progress`, `Code Review`, `QA`, `Done`, `Blocked`.
2. Criar campos customizados:
   - `RF`, `Sprint`, `Tipo`, `Pontos`, `Doc Alinhada`, `Critérios Aceite`, `QA Gate`.
3. Criar labels padrão:
   - `BACKEND`, `FRONTEND`, `QA`, `DOC-ALINHADO`, `BLOQUEADO`, `PRONTO-PARA-CODE`, `PRONTO-PARA-QA`.
4. Criar template de card com:
   - descrição técnica;
   - checklist técnico;
   - checklist QA;
   - critérios de aceite Gherkin.

## 2) Executar bots (manual)
1. Use `bots/prompts/prompt-mestre-bots-universal-v2.md`.
2. Forneça contexto do projeto ao orquestrador.
3. Deixe os bots gerarem:
   - documentação completa;
   - backlog por RF;
   - cards completos para cópia/cola.
4. Copie e cole os cards no Trello/Jira.

## 3) Fluxo operacional manual
1. Rodar bots para gerar lote de cards da sprint.
2. Revisar e aprovar cards internamente.
3. Colar cards no board.
4. Executar sprint com acompanhamento por métricas.

## 4) Rodar em qualquer projeto
1. Use o prompt: `bots/prompts/prompt-mestre-bots-universal-v2.md`.
2. Forneça contexto mínimo do projeto.
3. Orquestrador executa bots e gera documentação completa.
4. Converter saída em backlog manual (cópia/cola) no Trello/Jira.

## Aprendizado contínuo (IA nunca para de evoluir)
Este framework inclui melhoria contínua obrigatória:
- Ao fim de cada sprint/projeto registrar:
  - ambiguidades encontradas;
  - erros de estimativa;
  - gaps de teste;
  - padrões que funcionaram.
- Alimentar uma base de memória (recomendado `PostgreSQL` ou `Notion`).
- Injetar essa memória no contexto do prompt em cada nova execução.
- Revisar prompts mensalmente e atualizar “biblioteca de padrões aprovados”.

### Ciclo de evolução recomendado
1. Coleta de feedback (retro/sprint).
2. Classificação de lições aprendidas.
3. Atualização de prompts e gates.
4. Revalidação com card piloto.
5. Publicação da versão nova do framework.

## Governança e qualidade
- Sem evidência documental = sem aprovação.
- Qualquer bot pode `BLOQUEAR` por risco crítico.
- Apenas status `OK` em todos os bots libera card para desenvolvimento.
- `QA Gate` obrigatório antes de `Done` (mesmo no modo manual).

## Segurança e conformidade
- Não gravar segredos em cards/comentários.
- Registrar aprovação manual por etapa (quem aprovou, quando e por quê).

## Roadmap sugerido
1. v1: operação manual assistida por IA (atual).
2. v2: memória persistente e scoring de qualidade.
3. v3: semiautomação de geração de cards.
4. v4: automação completa com Trello/n8n (futuro).

## Licença
Defina conforme sua política (MIT/privada).
