# Regras Butler - Prontas para configurar

## Regra 1 - Entrada em Refino
When a card is moved into list "Refino":
- add checklist "Validação Documental"
- add checklist "Critérios de Aceite (Gherkin)"
- add checklist "Checklist Técnico"
- add checklist "Checklist QA"
- add label "Risco"
- post comment "Card em refino automático. Iniciando análise dos bots."

## Regra 2 - Documentação validada
When checklist "Validação Documental" is completed:
- set custom field "Doc Alinhada" to "OK"
- remove label "Risco"
- add label "DOC-ALINHADO"
- post comment "Validação documental concluída."

## Regra 3 - Pronto para desenvolvimento
When all checklists are complete in list "Refino":
- move the card to list "Ready"
- add label "PRONTO-PARA-CODE"
- post comment "Card pronto para desenvolvimento."

## Regra 4 - Entrada em QA
When a card is moved into list "QA":
- set custom field "QA Gate" to "Bloqueado"
- add label "QA"
- post comment "Card em QA. Gate bloqueado até validação final."

## Regra 5 - QA aprovado
When checklist "Checklist QA" is completed in list "QA":
- set custom field "QA Gate" to "OK"
- add label "PRONTO-PARA-QA"
- post comment "QA concluído com sucesso."

## Regra 6 - Bloqueio de Done sem QA gate
When a card is moved into list "Done":
- if custom field "QA Gate" is not "OK", move the card to list "QA" and post comment "Movimento para Done bloqueado: QA Gate não está OK."

## Regra 7 - Bloqueio explícito
When label "BLOQUEADO" is added to a card:
- move the card to list "Blocked"
- post comment "Card bloqueado. Definir causa, dono e prazo de desbloqueio."

## Regra 8 - Sinal de card parado
Every weekday at 9:00 am:
- for each card in list "In Progress" with no activity in 2 days, post comment "Atenção: card sem avanço há 2 dias. Atualizar status ou remover bloqueio."
