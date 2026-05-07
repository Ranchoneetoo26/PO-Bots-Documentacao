from __future__ import annotations

import json
from pathlib import Path

import typer

from .exporter import export_cards_copy_paste, export_cards_csv
from .generator import generate_artifacts
from .io_utils import ensure_dir, read_yaml, write_yaml
from .validator import save_validation_report, validate_cards_from_payload

app = typer.Typer(help="PO Bots CLI - geracao de documentacao e cards em modo manual.")


def _default_project_payload() -> dict:
    return {
        "project": {
            "name": "Projeto Exemplo",
            "objective": "Transformar requisitos em backlog claro, com checklist e Gherkin por RF.",
            "audience": "Time de produto e tecnologia",
            "deadline": "2026-12-31",
            "stack": ["Python", "FastAPI", "React"],
            "constraints": [
                "Sem envio automatico para Trello/Jira.",
                "Cards devem ser completos para copiar e colar.",
            ],
            "assumptions": [
                "Equipe trabalha com sprint quinzenal.",
                "Projeto possui revisao de QA antes de Done.",
            ],
        },
        "functional_requirements": [
            {
                "id": "RF001",
                "title": "Cadastro de cliente",
                "description": "Permitir cadastro de cliente com validacoes por campo.",
                "business_rules": [
                    "Nome e obrigatorio.",
                    "Telefone deve aceitar apenas numeros validos.",
                    "Email deve ser unico no sistema.",
                ],
                "acceptance_criteria": [
                    "Cadastrar cliente com dados validos.",
                    "Bloquear cadastro com email duplicado.",
                    "Exibir mensagem clara em validacao de campo.",
                ],
                "out_of_scope": ["Importacao em lote de clientes."],
                "priority": "M",
                "labels": ["backend", "frontend", "qa"],
            }
        ],
        "non_functional_requirements": [
            {
                "id": "RNF001",
                "title": "Observabilidade",
                "description": "Registrar logs de erro e eventos criticos para auditoria.",
            }
        ],
    }


@app.command()
def init(
    output: Path = typer.Option(Path("project.yaml"), help="Arquivo de configuracao do projeto."),
) -> None:
    """Cria o arquivo project.yaml inicial para comecar rapido."""
    if output.exists():
        typer.echo(f"Arquivo ja existe: {output}")
        raise typer.Exit(code=1)
    write_yaml(output, _default_project_payload())
    typer.echo(f"Arquivo criado: {output}")
    typer.echo("Edite o arquivo e execute: pobots generate --project-file project.yaml")


@app.command()
def generate(
    project_file: Path = typer.Option(Path("project.yaml"), help="Arquivo YAML com definicao do projeto."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio de saida."),
) -> None:
    """Gera documento mestre, catalogo RF/RNF, cards e prompt para IA."""
    if not project_file.exists():
        typer.echo(f"Arquivo nao encontrado: {project_file}")
        raise typer.Exit(code=1)
    cards = generate_artifacts(project_file=project_file, dist_dir=dist_dir)
    typer.echo(f"Geracao concluida. Cards criados: {len(cards)}")
    typer.echo(f"Arquivos disponiveis em: {dist_dir}")


@app.command()
def validate(
    cards_file: Path = typer.Option(Path("dist/cards.json"), help="Arquivo JSON de cards."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio de saida para relatorio."),
) -> None:
    """Valida qualidade dos cards e gera score global."""
    if not cards_file.exists():
        typer.echo(f"Arquivo nao encontrado: {cards_file}")
        raise typer.Exit(code=1)
    ensure_dir(dist_dir)
    with cards_file.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        typer.echo("cards.json invalido: esperado um array de cards.")
        raise typer.Exit(code=1)
    summary = validate_cards_from_payload(payload)
    save_validation_report(summary, dist_dir)
    typer.echo(f"Validacao concluida. Score global: {summary.global_score}")


@app.command()
def export(
    cards_file: Path = typer.Option(Path("dist/cards.json"), help="Arquivo JSON de cards."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio de saida."),
) -> None:
    """Exporta cards em CSV e TXT para copiar/colar."""
    if not cards_file.exists():
        typer.echo(f"Arquivo nao encontrado: {cards_file}")
        raise typer.Exit(code=1)
    ensure_dir(dist_dir)
    with cards_file.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        typer.echo("cards.json invalido: esperado um array de cards.")
        raise typer.Exit(code=1)

    export_cards_csv(payload, dist_dir / "cards-trello.csv")
    export_cards_copy_paste(payload, dist_dir / "cards-copy-paste.txt")
    typer.echo("Exportacao concluida: cards-trello.csv e cards-copy-paste.txt")


@app.command()
def doctor(
    project_file: Path = typer.Option(Path("project.yaml"), help="Arquivo YAML com definicao do projeto."),
) -> None:
    """Checa rapidamente se os arquivos base estao presentes."""
    checks = {
        "project.yaml": project_file.exists(),
        "bots/prompt-mestre": Path("bots/prompts/prompt-mestre-bots-universal-v2.md").exists(),
        "bots/prompt-pack": Path("bots/prompts/prompt-pack-bots.md").exists(),
        "bots/protocolo": Path("bots/protocolo-handoff-bots.md").exists(),
    }
    for key, status in checks.items():
        typer.echo(f"{key}: {'OK' if status else 'FALTANDO'}")
    if not all(checks.values()):
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
