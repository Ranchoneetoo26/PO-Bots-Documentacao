from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import List

from pydantic import ValidationError

from .io_utils import bullets, ensure_dir, read_yaml, write_json, write_text
from .models import Card, FunctionalRequirement, ProjectDefinition


def default_technical_checklist(requirement: FunctionalRequirement) -> List[str]:
    return [
        f"Implementar regra principal do {requirement.id} sem ambiguidade.",
        "Mapear validacoes de entrada e mensagens de erro por campo.",
        "Definir status HTTP e comportamento de fallback quando aplicavel.",
        "Garantir logs tecnicos com rastreabilidade de execucao.",
        "Atualizar documentacao tecnica e criterios de pronto (DoD).",
    ]


def default_qa_checklist() -> List[str]:
    return [
        "Validar happy path completo sem erro funcional.",
        "Validar cenarios de erro e mensagens esperadas.",
        "Validar cenarios de borda e dados invalidos.",
        "Validar nao regressao dos fluxos relacionados.",
        "Registrar evidencia de teste para homologacao.",
    ]


def gherkin_from_acceptance(requirement: FunctionalRequirement) -> List[str]:
    if requirement.acceptance_criteria:
        scenarios = []
        for index, item in enumerate(requirement.acceptance_criteria, start=1):
            scenarios.extend(
                [
                    f"Cenario: {requirement.id} criterio {index}",
                    "Dado que o usuario acessa o fluxo previsto",
                    f"Quando ele executa a acao: {item}",
                    "Entao o sistema deve responder conforme a regra esperada",
                    "",
                ]
            )
        return scenarios[:-1]

    return [
        f"Cenario: {requirement.id} fluxo principal",
        "Dado que o usuario atende os pre-requisitos",
        "Quando ele executa a acao principal do requisito",
        "Entao o sistema conclui a operacao com sucesso",
    ]


def build_card(requirement: FunctionalRequirement) -> Card:
    return Card(
        rf_id=requirement.id,
        title=f"{requirement.id} - {requirement.title}",
        objective=requirement.description,
        scope=requirement.description,
        out_of_scope=requirement.out_of_scope,
        business_rules=requirement.business_rules,
        technical_checklist=default_technical_checklist(requirement),
        qa_checklist=default_qa_checklist(),
        gherkin=gherkin_from_acceptance(requirement),
        priority=requirement.priority,
        labels=requirement.labels,
    )


def render_document_master(data: ProjectDefinition) -> str:
    project = data.project
    rf_list = "\n".join([f"- {item.id}: {item.title}" for item in data.functional_requirements]) or "- (sem RF)"
    rnf_list = (
        "\n".join([f"- {item.id}: {item.title}" for item in data.non_functional_requirements]) or "- (sem RNF)"
    )

    return f"""# Documento Mestre - {project.name}

Data de geracao: {date.today().isoformat()}

## 1. Visao do projeto
- Objetivo: {project.objective}
- Publico: {project.audience}
- Prazo: {project.deadline}
- Stack sugerida: {", ".join(project.stack) if project.stack else "(nao informado)"}

## 2. Restricoes
{bullets(project.constraints)}

## 3. Hipoteses declaradas
{bullets(project.assumptions)}

## 4. Requisitos funcionais (RF)
{rf_list}

## 5. Requisitos nao funcionais (RNF)
{rnf_list}

## 6. Regra operacional
- Este pacote gera cards para copiar e colar no Trello/Jira.
- Nao existe envio automatico para Trello/Jira.
"""


def render_rf_rnf(data: ProjectDefinition) -> str:
    parts: list[str] = [f"# Catalogo RF/RNF - {data.project.name}", ""]
    parts.append("## RF")
    if not data.functional_requirements:
        parts.append("- (sem RF)")
    for rf in data.functional_requirements:
        parts.extend(
            [
                f"### {rf.id} - {rf.title}",
                f"Objetivo: {rf.description}",
                "Regras de negocio:",
                bullets(rf.business_rules),
                "Criterios de aceite base:",
                bullets(rf.acceptance_criteria),
                "Fora de escopo:",
                bullets(rf.out_of_scope),
                "",
            ]
        )
    parts.append("## RNF")
    if not data.non_functional_requirements:
        parts.append("- (sem RNF)")
    for rnf in data.non_functional_requirements:
        parts.extend([f"- {rnf.id} - {rnf.title}: {rnf.description}"])
    return "\n".join(parts)


def render_cards_markdown(cards: List[Card], project_name: str) -> str:
    blocks: list[str] = [f"# Cards Prontos (Copiar/Colar) - {project_name}", ""]
    blocks.append("> Operacao manual: copiar e colar no Trello/Jira. Sem integracao automatica.")
    blocks.append("")
    for card in cards:
        blocks.extend(
            [
                f"## {card.title}",
                f"Prioridade: {card.priority}",
                f"Labels: {', '.join(card.labels) if card.labels else '(sem labels)'}",
                "",
                "### Objetivo",
                card.objective,
                "",
                "### Escopo",
                card.scope,
                "",
                "### Fora de escopo",
                bullets(card.out_of_scope),
                "",
                "### Regras de negocio",
                bullets(card.business_rules),
                "",
                "### Checklist tecnico",
                bullets(card.technical_checklist),
                "",
                "### Checklist QA",
                bullets(card.qa_checklist),
                "",
                "### Criterios de aceite (Gherkin)",
                "\n".join(card.gherkin),
                "",
                "---",
                "",
            ]
        )
    return "\n".join(blocks).strip() + "\n"


def render_prompt_copy_paste(data: ProjectDefinition) -> str:
    project = data.project
    requirements = "\n".join([f"- {rf.id}: {rf.title}" for rf in data.functional_requirements]) or "- Definir RF"
    return f"""# Prompt de Execucao Rapida - {project.name}

Use o texto abaixo na IA:

Projeto: {project.name}
Objetivo: {project.objective}
Publico: {project.audience}
Prazo: {project.deadline}
Stack: {", ".join(project.stack) if project.stack else "(definir stack)"}
Restricoes:
{bullets(project.constraints)}

RF ja definidos:
{requirements}

Instrucoes obrigatorias:
- Responder sem ambiguidade.
- Gerar por RF: objetivo, escopo, regras executaveis.
- Incluir checklist tecnico, checklist QA e Gherkin para cada RF.
- Entregar secao final "Cards Prontos (Copiar/Colar)".
- Nao enviar automaticamente para Trello/Jira. Apenas gerar para copy/paste.
"""


def generate_artifacts(project_file: Path, dist_dir: Path) -> List[Card]:
    payload = read_yaml(project_file)
    try:
        project_data = ProjectDefinition.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Arquivo de projeto invalido: {exc}") from exc

    ensure_dir(dist_dir)
    cards = [build_card(requirement) for requirement in project_data.functional_requirements]

    write_text(dist_dir / "documento-mestre.md", render_document_master(project_data))
    write_text(dist_dir / "catalogo-rf-rnf.md", render_rf_rnf(project_data))
    write_text(dist_dir / "cards-trello.md", render_cards_markdown(cards, project_data.project.name))
    write_text(dist_dir / "prompt-ia-copiar-colar.md", render_prompt_copy_paste(project_data))
    write_json(dist_dir / "cards.json", [card.model_dump(mode="json") for card in cards])
    return cards
