# Operação de Sprints com Bots Integrados (Modo Manual + Evolução para Automação)

## 1) O que este modelo resolve
Este modelo cria um sistema de acompanhamento e execução de sprint com bots especializados que:
- validam alinhamento com documentação antes de qualquer execução;
- geram tarefas e critérios técnicos sem ambiguidade;
- bloqueiam avanço quando qualidade/aceite não estão completos;
- mantêm rastreabilidade entre requisito, card, código, teste e evidência.

## 2) Arquitetura recomendada (estado atual e futuro)
## Estado atual (ativo)
- Bots geram documentação e cards completos em texto.
- Time copia e cola no Trello/Jira manualmente.
- Gates e validações são aplicados no conteúdo antes da execução.

## Futuro (opcional)
Automação completa com Trello + n8n.

## Arquitetura futura (simples e escalável)
## Camada A - Trello (fonte de verdade do fluxo)
- Board de sprint com listas padronizadas:
  - `Backlog Sprint`
  - `Refino`
  - `Ready`
  - `In Progress`
  - `Code Review`
  - `QA`
  - `Done`
  - `Blocked`

## Camada B - Orquestrador (n8n ou Make)
- Gatilhos:
  - card criado
  - card movido de lista
  - checklist concluído
  - label adicionada/removida
- Ações:
  - chamar API LLM por papel (CEO, Arquiteto, Analista, QA, Dev Back, Dev Front)
  - atualizar descrição/checklists/labels do card
  - comentar decisões e bloqueios
  - abrir subtarefas automáticas

## Camada C - Bots especializados (LLM por papel)
- Um bot por responsabilidade.
- Todos usam o mesmo contexto documental.
- Todos seguem o mesmo protocolo de handoff.

## 3) Ferramentas recomendadas (modo atual)
- OpenAI API (ou equivalente) para os bots
- Trello/Jira para execução manual dos cards (cópia/cola)
- Google Sheets (opcional) para dashboard de métricas
- VSCode para organização do repositório de documentação

## Ferramentas opcionais (futuro)
- Trello + Butler (automação nativa)
- n8n (orquestração principal)
- Slack/Discord (alertas automáticos)

## 4) Modelo de governança (obrigatório)
## 4.1 Campos customizados do Trello
- `RF` (texto)
- `Sprint` (texto)
- `Tipo` (Feature/Bug/TechDebt/Infra)
- `Pontos` (número)
- `Critérios Aceite` (texto curto: `OK/Pendente`)
- `Doc Alinhada` (texto curto: `OK/Pendente`)
- `QA Gate` (texto curto: `OK/Bloqueado`)

## 4.2 Labels padrão
- `BACKEND`
- `FRONTEND`
- `QA`
- `DOC-ALINHADO`
- `BLOQUEADO`
- `PRONTO-PARA-CODE`
- `PRONTO-PARA-QA`

## 4.3 Regras de bloqueio (gate)
- Não sair de `Refino` sem:
  - critérios de aceite Gherkin;
  - checklist técnico;
  - checklist QA;
  - validação de alinhamento documental (`Doc Alinhada=OK`).
- Não sair de `Code Review` sem:
  - evidências de testes;
  - lint/build verdes;
  - checklist de segurança básico.
- Não sair de `QA` sem `QA Gate=OK`.

## 5) Fluxo entre bots (interligado)
1. **Analista** recebe card em `Refino` e estrutura requisito executável.
2. **Arquiteto** valida impacto técnico, dependências e riscos.
3. **CEO** valida prioridade, valor e escopo.
4. **Dev Back** e **Dev Front** recebem plano técnico aprovado.
5. **QA** gera cenários de teste e bloqueios de qualidade.
6. Orquestrador consolida pareceres e atualiza card.

Se qualquer bot reprovar (`Pendente/Bloqueado`), o card não avança.

## 6) Matriz de responsabilidade (RACI simplificada)
- CEO: prioridade, valor de negócio, corte de escopo.
- Arquiteto: desenho técnico, dependências, risco.
- Analista: clareza do requisito e critérios de aceite.
- Dev Back: API, dados, regras de domínio, testes backend.
- Dev Front: UX, validações de tela, integração API, testes frontend.
- QA: estratégia e execução de validação final.

## 7) Implementação em 60 minutos (modo manual - ativo)
## Passo 1 - Preparar board (15 min)
1. Criar listas padrão.
2. Criar custom fields e labels.
3. Definir template de card com checklists (técnico + QA + Gherkin).

## Passo 2 - Rodar bots e gerar cards (20 min)
1. Executar o prompt mestre.
2. Fornecer contexto mínimo do projeto.
3. Gerar pacote de cards completos com:
   - descrição detalhada;
   - checklist técnico;
   - checklist QA;
   - critérios Gherkin.
4. Copiar e colar no board.

## Passo 3 - Revisão e gate manual (15 min)
1. Validar se todos os gates estão cobertos no texto do card.
2. Marcar `Doc Alinhada=OK` apenas com evidência.
3. Marcar `QA Gate=OK` somente com critérios completos.
4. Mover para `Ready`.

## Passo 4 - Teste real (10 min)
1. Criar card piloto RF real.
2. Rodar bots e gerar card final.
3. Colar no Trello/Jira.
4. Validar execução sem ambiguidades.

## 8) Métricas do sistema de bots (modo atual)
- % de cards aprovados na primeira passagem do refino.
- Tempo médio `Refino -> Ready`.
- % de bloqueio por falta de documentação.
- % de bloqueio por QA.
- Tempo médio de resolução de bloqueios.

## 9) Política anti-desalinhamento (crítica)
- Nenhum bot pode inventar regra fora dos documentos oficiais.
- Toda decisão deve citar origem:
  - `drp.md`, `us.md`, `api-banco...`, `especificacao-tecnica...`
- Quando houver conflito documental:
  - marcar `Bloqueado`;
  - abrir comentário: `Conflito documental identificado`;
  - exigir decisão explícita antes de avançar.

## 10) Entregáveis mínimos (modo atual)
- Board configurado.
- Prompts dos bots carregados.
- Card piloto executado com sucesso.
- Dashboard de métricas de sprint atualizado.

## 11) Evolução futura (opcional)
- Ativar Butler e n8n para reduzir trabalho manual.
- Automatizar comentários e movimentação de cards.
- Automatizar gates com bloqueio técnico.
