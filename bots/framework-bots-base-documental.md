# Framework de Bots Baseado em Documentação (Universal)

## 1) Objetivo
Criar um sistema de bots interligados que transforma entrada de projeto em documentação executável, rastreável e pronta para backlog, usando a lógica estrutural de:
- `DVP-E` (visão, problema, valor, stakeholders, escopo);
- `DVS` (viabilidade técnica/econômica/operacional/legal/cronograma/humana, riscos, Go/No-Go);
- `DRP` (RF, RN, RNF, dados, regras de negócio, critérios de aceite);
- `DAT` (arquitetura técnica, módulos, dados, segurança, observabilidade, deploy);
- `GDR` (rastreabilidade, governança de mudança, homologação e gates).

Este framework é universal: pode ser aplicado em qualquer domínio.

---

## 2) Mapa de conhecimento por documento (o que os bots devem aprender)
## DVP-E (Estratégia e Produto)
- Problema e impacto de negócio;
- visão e objetivos do produto;
- stakeholders e perfis de usuário;
- escopo MoSCoW (Must/Should/Could/Won't);
- critérios de sucesso e riscos de negócio.

## DVS (Viabilidade)
- viabilidade técnica, operacional, econômica, legal, cronograma e humana;
- matriz de riscos e mitigação;
- critérios de decisão Go/No-Go.

## DRP (Requisitos)
- catálogo RF/RN/RNF;
- regras de negócio executáveis;
- requisitos de dados e validações;
- critérios de aceite testáveis;
- fluxos principais e fora de escopo.

## DAT (Arquitetura)
- drivers e restrições técnicas;
- visão de módulos e componentes;
- modelo de dados, consistência e transações;
- segurança e controle de acesso;
- observabilidade, deploy e operação.

## GDR (Governança e Rastreabilidade)
- trilha: problema -> requisito -> regra -> CA -> solução técnica;
- política de mudança (CR);
- checklist de homologação;
- gates de aprovação documental e funcional.

---

## 3) Bots e papéis do início ao fim
## BOT_CEO (Estratégia)
- Dono do valor de negócio e prioridade.
- Decide escopo e corte de fase.
- Bloqueia itens sem impacto/ROI claro.

## BOT_ANALISTA (Requisito)
- Converte necessidade em requisito executável.
- Remove ambiguidades.
- Gera critérios Gherkin e DoD.

## BOT_ARQUITETO (Solução)
- Define arquitetura e impactos.
- Garante aderência técnica e escalabilidade.
- Bloqueia inconsistência entre requisito e solução.

## BOT_DEV_BACK (Execução Backend)
- Especifica APIs, domínio, validações, dados e logs.
- Gera checklist técnico backend.

## BOT_DEV_FRONT (Execução Frontend)
- Especifica fluxos de tela, validações por campo, estados de UI e integração.
- Gera checklist técnico frontend.

## BOT_QA (Qualidade)
- Define estratégia de testes e cobertura mínima.
- Bloqueia sem evidência de teste.

## BOT_COMPLIANCE (Segurança e Conformidade)
- Valida privacidade, trilha de auditoria, controle de acesso e políticas.
- Bloqueia violações de conformidade.

## BOT_PM (Planejamento e Entrega)
- Planeja sprint, dependências, marcos, capacidade e métricas.
- Mantém previsibilidade e execução.

---

## 4) Protocolo de colaboração entre bots
Ordem de execução obrigatória:
1. BOT_ANALISTA
2. BOT_ARQUITETO
3. BOT_CEO
4. BOT_DEV_BACK
5. BOT_DEV_FRONT
6. BOT_QA
7. BOT_COMPLIANCE
8. BOT_PM

Regra:
- qualquer `BLOQUEADO` interrompe o fluxo;
- `PENDENTE` volta para o bot da etapa com plano de ajuste;
- somente todos `OK` permite avançar para “pronto para execução”.

---

## 5) Entregáveis obrigatórios por ciclo
1. Documento mestre consolidado.
2. Catálogo RF/RNF completo.
3. Arquitetura lógica/técnica.
4. Contratos de API (quando aplicável).
5. Modelo de dados inicial (quando aplicável).
6. Plano de testes + matriz de cobertura.
7. Backlog pronto para Trello/Jira.
8. Critérios Gherkin para todos os itens.
9. Checklist operacional e governança.
10. Plano de métricas de sprint e qualidade.

---

## 6) Auto-melhoria contínua (aprendizado entre projetos)
Ao final de cada projeto/sprint registrar:
- ambiguidades recorrentes;
- erros de estimativa;
- falhas de cobertura de teste;
- decisões arquiteturais que funcionaram;
- pontos de conformidade críticos.

Aplicar no próximo projeto:
- biblioteca de padrões aprovados;
- catálogo de riscos recorrentes;
- templates com melhoria incremental.

Regra de ouro:
- melhorar continuamente sem quebrar rastreabilidade, clareza e segurança.
