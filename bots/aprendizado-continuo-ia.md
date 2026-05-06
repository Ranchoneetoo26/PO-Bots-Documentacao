# Aprendizado Contínuo dos Bots (IA)

## Objetivo
Garantir que os bots melhorem continuamente entre projetos e sprints, sem perder governança documental.

## Estratégia
Usar um ciclo fechado de aprendizado:
1. Captura de feedback (review/retro/QA/incidentes).
2. Estruturação de lições aprendidas.
3. Atualização de padrões e prompts.
4. Reexecução em cards piloto.
5. Publicação de versão nova do framework.

## Dados a capturar por sprint
- ambiguidades detectadas;
- blocos de requisito que geraram retrabalho;
- bugs de regressão;
- causas de bloqueio de QA;
- falhas de estimativa;
- decisões técnicas que reduziram risco.

## Armazenamento recomendado
- Tabela `bots_learning_memory` (PostgreSQL) ou base equivalente:
  - `id`
  - `projeto`
  - `sprint`
  - `categoria` (ambiguidade, teste, arquitetura, compliance, etc.)
  - `problema`
  - `solucao_aplicada`
  - `resultado`
  - `confianca` (0..1)
  - `data_registro`

## Injeção no contexto dos bots
Antes de cada execução do orquestrador:
- recuperar as top N lições com maior relevância para o domínio;
- anexar no prompt em seção `MEMÓRIA OPERACIONAL`;
- exigir que cada bot aplique as lições na análise atual.

## Regras de segurança do aprendizado
- não armazenar segredo/token/dado sensível;
- anonimizar dados pessoais;
- manter trilha de auditoria das atualizações do prompt.

## Métricas de evolução dos bots
- % de cards aprovados na primeira passagem;
- redução de cards bloqueados por ambiguidade;
- redução de retrabalho;
- redução de bugs pós-entrega;
- tempo médio Refino -> Ready.

## Gate de melhoria contínua
Uma melhoria só vira padrão quando:
1. foi aplicada em pelo menos 2 ciclos;
2. trouxe ganho mensurável;
3. não gerou conflito com governança documental.
