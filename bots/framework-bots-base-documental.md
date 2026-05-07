# Framework de Bots Baseado em Documentacao (Universal)

## 1) Objetivo
Criar um sistema de bots que transforma entrada de projeto em documentacao executavel, rastreavel e pronta para backlog, com automacao local em Python e operacao manual no Trello/Jira.

Base estrutural obrigatoria:
- `DVP-E` (visao, problema, valor, stakeholders, escopo);
- `DVS` (viabilidade e riscos com decisao Go/No-Go);
- `DRP` (RF, RN, RNF, regras e criterios de aceite);
- `DAT` (arquitetura tecnica, dados, seguranca, operacao);
- `GDR` (rastreabilidade, homologacao e gates).

Regra fixa do produto:
- Sem envio automatico para Trello/Jira.
- O sistema gera cards completos para copiar e colar.

---

## 2) Camadas da plataforma
1. **Camada de entrada**
   - arquivo `project.yaml` com contexto do cliente e RF/RNF.
2. **Camada de orquestracao**
   - CLI Python (`pobots`) executa fases de geracao, validacao e exportacao.
3. **Camada de qualidade**
   - score por card (0-100), status `OK | PENDENTE | BLOQUEADO`.
4. **Camada de entrega**
   - arquivos finais em `dist/` para uso imediato.

---

## 3) Bots e papeis do inicio ao fim
## BOT_CEO (Estrategia)
- Valida valor de negocio, prioridade e ROI.
- Bloqueia card sem impacto claro.

## BOT_ANALISTA (Requisito)
- Remove ambiguidade.
- Gera RF executavel com checklist e Gherkin.

## BOT_ARQUITETO (Solucao)
- Valida aderencia tecnica e escalabilidade.
- Bloqueia conflito requisito vs arquitetura.

## BOT_DEV_BACK (Execucao Backend)
- Especifica API, dominio, validacoes, dados e logs.

## BOT_DEV_FRONT (Execucao Frontend)
- Especifica tela, estados, validacoes por campo e integracao.

## BOT_QA (Qualidade)
- Define cobertura minima e evidencias obrigatorias.

## BOT_COMPLIANCE (Seguranca e Conformidade)
- Garante privacidade, auditoria e controle de acesso.

## BOT_PM (Planejamento e Entrega)
- Organiza dependencias, sprint, risco e previsibilidade.

---

## 4) Fluxo de execucao (automatizado local)
Ordem:
1. BOT_ANALISTA
2. BOT_ARQUITETO
3. BOT_CEO
4. BOT_DEV_BACK
5. BOT_DEV_FRONT
6. BOT_QA
7. BOT_COMPLIANCE
8. BOT_PM

Regra de gate:
- `BLOQUEADO`: interrompe fluxo e gera ajustes necessarios.
- `PENDENTE`: volta para etapa anterior com plano de correcao.
- `OK`: segue para etapa seguinte.

---

## 5) Entregaveis obrigatorios por ciclo
1. Documento mestre consolidado.
2. Catalogo RF/RNF.
3. Cards prontos para copiar e colar no Trello/Jira.
4. Checklist tecnico por RF.
5. Checklist QA por RF.
6. Criterios Gherkin por RF.
7. Relatorio de qualidade com score.
8. Exportacao CSV/TXT para operacao manual.

---

## 6) Modo de uso recomendado
1. Clonar repositorio.
2. Rodar `pobots init`.
3. Preencher `project.yaml`.
4. Rodar `pobots generate`.
5. Rodar `pobots validate`.
6. Rodar `pobots export`.
7. Copiar/colar cards no Trello/Jira.

---

## 7) Auto-melhoria continua
Ao final de cada sprint, registrar:
- ambiguidades recorrentes;
- retrabalho;
- bugs pos-entrega;
- estimativas ruins;
- padroes que funcionaram.

Aplicar no ciclo seguinte para elevar qualidade sem perder rastreabilidade.
