# Automação de Sprints com Bots Integrados (Trello)

## 1) O que este modelo resolve
Este modelo cria um sistema de acompanhamento e execução de sprint com bots especializados que:
- validam alinhamento com documentação antes de qualquer execução;
- geram tarefas e critérios técnicos sem ambiguidade;
- bloqueiam avanço quando qualidade/aceite não estão completos;
- mantêm rastreabilidade entre requisito, card, código, teste e evidência.

## 2) Arquitetura recomendada (simples e escalável)
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

## 3) Ferramentas recomendadas
- Trello + Butler (automação nativa)
- n8n (orquestração principal)
- OpenAI API (ou equivalente) para os bots
- Google Sheets (opcional) para dashboard de métricas
- Slack/Discord (opcional) para alertas

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

## 7) Implementação em 90 minutos (passo a passo)
## Passo 1 - Preparar board (15 min)
1. Criar listas padrão.
2. Criar custom fields e labels.
3. Definir template de card com checklists (técnico + QA + Gherkin).

## Passo 2 - Ativar Butler (20 min)
Crie automações:
1. Quando card entrar em `Refino`:
   - adicionar checklist `Validação Documental`.
   - comentar `Iniciar análise dos bots`.
2. Quando checklist `Validação Documental` for concluída:
   - setar `Doc Alinhada=OK`.
3. Quando card entrar em `QA`:
   - setar `QA Gate=Bloqueado`.
4. Quando checklist `QA` concluída:
   - setar `QA Gate=OK`.
5. Bloquear avanço para `Done` se `QA Gate != OK`.

## Passo 3 - Orquestrador n8n (35 min)
1. Criar workflow com gatilho `Trello Card Updated`.
2. Condição: `lista == Refino`.
3. Ler card + documentação base (via arquivos/URL).
4. Chamar bots na ordem:
   - Analista -> Arquiteto -> CEO -> QA
5. Consolidar saídas:
   - `status_final = OK` apenas se todos `OK`.
6. Atualizar card:
   - descrição refinada;
   - checklists;
   - campos `Doc Alinhada` e `Critérios Aceite`;
   - comentário com resumo executivo.

## Passo 4 - Alertas (10 min)
1. Se bot retornar `Bloqueado`, enviar alerta para canal de gestão.
2. Se card ficar > 24h em `Blocked`, alertar dono + líder.

## Passo 5 - Teste real (10 min)
1. Criar card piloto RF real.
2. Mover para `Refino`.
3. Validar atualização automática.
4. Corrigir regra que não disparar.

## 8) Métricas automáticas do sistema de bots
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

## 10) Entregáveis mínimos da automação
- Board configurado.
- Butler ativo.
- Workflow n8n ativo.
- Prompts dos 6 bots carregados.
- Card piloto executado com sucesso.
- Dashboard de métricas de sprint atualizado.
