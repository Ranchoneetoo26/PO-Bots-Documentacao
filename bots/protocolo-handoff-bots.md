# Protocolo de Handoff entre Bots

## Ordem obrigatória
1. Analista
2. Arquiteto
3. CEO
4. Dev Back
5. Dev Front
6. QA
7. Compliance
8. PM

## Regra de avanço
- Só avança para o próximo bot se `status=OK`.
- Se `PENDENTE`, o orquestrador ajusta card e reenfileira no mesmo bot.
- Se `BLOQUEADO`, card vai para lista `Blocked` com comentário obrigatório.

## Comentário obrigatório no Trello por etapa
Formato:
`[BOT:<nome>] [STATUS:<status>] <resumo> | Ações: <acoes_recomendadas>`

## Critérios de bloqueio cruzado
- CEO pode bloquear por desalinhamento de valor.
- Arquiteto pode bloquear por risco técnico estrutural.
- QA pode bloquear por falta de evidência de teste.
- Dev Back/Front podem bloquear por ambiguidade de requisito.
- Compliance pode bloquear por risco de segurança/conformidade.
- PM pode bloquear por inviabilidade de entrega/capacidade.

## Definição de card pronto para desenvolvimento
Somente quando todos os itens estiverem `OK`:
- Critérios Gherkin completos.
- Checklist técnico.
- Checklist QA.
- Evidência documental citada.
- Labels e campos de governança preenchidos.

## Definição de card pronto para Done
- Código aprovado.
- QA Gate = OK.
- Evidências anexadas.
- Sem bloqueios abertos.
