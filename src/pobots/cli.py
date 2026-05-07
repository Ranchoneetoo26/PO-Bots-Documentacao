from __future__ import annotations

import json
import os
from pathlib import Path

import typer

from .ai_pipeline import run_ai_pipeline
from .exporter import export_cards_copy_paste, export_cards_csv
from .generator import generate_artifacts
from .io_utils import ensure_dir, write_yaml
from .validator import save_validation_report, validate_cards_from_payload

app = typer.Typer(help="PO Bots CLI - geracao de documentacao e cards em modo manual.")


def _find_latest_run(dist_dir: Path) -> Path | None:
    if not dist_dir.exists():
        return None
    candidates = [item for item in dist_dir.iterdir() if item.is_dir() and item.name.startswith("gerado-")]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def _resolve_cards_file(cards_file: Path | None, dist_dir: Path) -> Path | None:
    if cards_file:
        return cards_file
    latest = _find_latest_run(dist_dir)
    if not latest:
        return None
    candidate = latest / "06-backlog" / "cards.json"
    return candidate if candidate.exists() else None


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
    cards, run_dir = generate_artifacts(project_file=project_file, dist_dir=dist_dir)
    typer.echo(f"Geracao concluida. Cards criados: {len(cards)}")
    typer.echo(f"Arquivos disponiveis em: {run_dir}")


@app.command()
def validate(
    cards_file: Path | None = typer.Option(None, help="Arquivo JSON de cards."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio raiz onde as geracoes foram criadas."),
) -> None:
    """Valida qualidade dos cards e gera score global."""
    resolved_cards_file = _resolve_cards_file(cards_file, dist_dir)
    if not resolved_cards_file:
        typer.echo("Arquivo de cards nao encontrado. Rode o comando generate primeiro.")
        raise typer.Exit(code=1)
    with resolved_cards_file.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        typer.echo("cards.json invalido: esperado um array de cards.")
        raise typer.Exit(code=1)
    summary = validate_cards_from_payload(payload)
    save_validation_report(summary, resolved_cards_file.parent)
    typer.echo(f"Validacao concluida. Score global: {summary.global_score}")
    typer.echo(f"Relatorio salvo em: {resolved_cards_file.parent}")


@app.command()
def export(
    cards_file: Path | None = typer.Option(None, help="Arquivo JSON de cards."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio raiz onde as geracoes foram criadas."),
) -> None:
    """Exporta cards em CSV e TXT para copiar/colar."""
    resolved_cards_file = _resolve_cards_file(cards_file, dist_dir)
    if not resolved_cards_file:
        typer.echo("Arquivo de cards nao encontrado. Rode o comando generate primeiro.")
        raise typer.Exit(code=1)
    with resolved_cards_file.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, list):
        typer.echo("cards.json invalido: esperado um array de cards.")
        raise typer.Exit(code=1)
    target_dir = resolved_cards_file.parent
    ensure_dir(target_dir)
    export_cards_csv(payload, target_dir / "cards-trello.csv")
    export_cards_copy_paste(payload, target_dir / "cards-copy-paste.txt")
    typer.echo("Exportacao concluida: cards-trello.csv e cards-copy-paste.txt")
    typer.echo(f"Arquivos exportados em: {target_dir}")


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


@app.command("ai-generate")
def ai_generate(
    task: str = typer.Argument(..., help="Task inicial informada pelo cliente."),
    token: str | None = typer.Option(None, help="Token da API de IA do cliente."),
    model: str = typer.Option("gpt-4o-mini", help="Modelo da IA."),
    api_base_url: str = typer.Option(
        "https://api.openai.com/v1",
        help="Base URL da API compatível com OpenAI.",
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--auto-decide",
        help="Quando ativo, pergunta ao usuario e deixa IA decidir respostas vazias.",
    ),
    project_file: Path = typer.Option(Path("project.yaml"), help="Arquivo de projeto gerado pela IA."),
    dist_dir: Path = typer.Option(Path("dist"), help="Diretorio raiz de saida."),
) -> None:
    """Gera project.yaml + documentacao completa usando token do cliente e prompts internos."""
    final_token = token or os.getenv("POBOTS_API_TOKEN", "")
    if not final_token.strip():
        typer.echo("Token nao informado. Use --token ou variavel de ambiente POBOTS_API_TOKEN.")
        raise typer.Exit(code=1)
    try:
        run_dir = run_ai_pipeline(
            repo_root=Path(".").resolve(),
            task=task,
            token=final_token,
            model=model,
            api_base_url=api_base_url,
            interactive=interactive,
            project_file=project_file,
            dist_dir=dist_dir,
        )
    except Exception as exc:  # pragma: no cover - erro de runtime externo
        typer.echo(f"Falha no pipeline de IA: {exc}")
        raise typer.Exit(code=1) from exc

    typer.echo(f"Pipeline de IA concluido. Arquivos em: {run_dir}")
    typer.echo("Backlog pronto para copy/paste em: 06-backlog/cards-trello.md")


if __name__ == "__main__":
    app()
