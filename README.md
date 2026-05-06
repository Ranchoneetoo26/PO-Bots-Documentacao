# PO-Bots-Documentacao

Framework de bots de IA para criação e governança de documentação de projetos de software, com rastreabilidade ponta a ponta e operação integrada ao Trello.

## O que este repositório entrega
- Arquitetura de bots por papéis (CEO, Analista, Arquiteto, Dev Back, Dev Front, QA, Compliance, PM).
- Prompt mestre universal para qualquer projeto.
- Protocolo de handoff e regras de gate entre bots.
- Workflow n8n importável para orquestração automática.
- Regras de Butler para Trello.
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
  Workflow n8n pronto para importar.
- `trello-butler-regras-prontas.md`  
  Regras de automação no Trello.
- `automacao-bots-trello-playbook.md`  
  Guia operacional completo.
- `analise-alinhamento-e-divergencia.md`  
  Verificação de consistência.

## Plataformas recomendadas
- **Editor:** VSCode
- **Orquestração:** n8n Cloud (ou self-hosted)
- **Board:** Trello
- **IA:** OpenAI API (ou equivalente)
- **Alertas:** Slack/Discord/Email (opcional)
- **Memória de aprendizado:** PostgreSQL/Notion/Google Sheets (recomendado)

## Pré-requisitos
1. Conta no Trello com board configurado.
2. Conta no n8n (cloud ou self-hosted).
3. Chave de API de IA.
4. Permissões para criar automações no Trello (Butler).

## Instalação e uso (passo a passo)
## 1) Preparar Trello
1. Criar listas:
   - `Backlog Sprint`, `Refino`, `Ready`, `In Progress`, `Code Review`, `QA`, `Done`, `Blocked`.
2. Criar campos customizados:
   - `RF`, `Sprint`, `Tipo`, `Pontos`, `Doc Alinhada`, `Critérios Aceite`, `QA Gate`.
3. Criar labels padrão:
   - `BACKEND`, `FRONTEND`, `QA`, `DOC-ALINHADO`, `BLOQUEADO`, `PRONTO-PARA-CODE`, `PRONTO-PARA-QA`.
4. Aplicar regras de `trello-butler-regras-prontas.md`.

## 2) Preparar n8n
1. Criar credenciais:
   - Trello API
   - OpenAI API
2. Importar `n8n-workflow-po-bots-orchestrator.json`.
3. Configurar variáveis de ambiente:
   - `TRELLO_BOARD_ID`
   - `TRELLO_LIST_READY_ID`
   - `TRELLO_LIST_BLOCKED_ID`
4. Ativar workflow.

## 3) Rodar primeiro fluxo
1. Criar card no Trello.
2. Mover para `Refino`.
3. Verificar:
   - comentários automáticos de bots;
   - bloqueios/gates;
   - movimento automático para `Ready` ou `Blocked`.

## 4) Rodar em qualquer projeto
1. Use o prompt: `bots/prompts/prompt-mestre-bots-universal-v2.md`.
2. Forneça contexto mínimo do projeto.
3. Orquestrador executa bots e gera documentação completa.
4. Converter saída em backlog Trello/Jira.

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
- `QA Gate` obrigatório antes de `Done`.

## Segurança e conformidade
- Usar variáveis de ambiente para chaves.
- Não gravar segredos em cards/comentários.
- Ativar trilha de auditoria (quem aprovou, quando e por quê).

## Roadmap sugerido
1. v1: operação com Trello + n8n + OpenAI (manual assistido).
2. v2: memória persistente e scoring de qualidade.
3. v3: detecção automática de conflito documental.
4. v4: geração automática de cards e matriz de rastreabilidade.

## Licença
Defina conforme sua política (MIT/privada).
