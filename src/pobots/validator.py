from __future__ import annotations

from pathlib import Path
from typing import Any, List

from pydantic import ValidationError

from .io_utils import write_json, write_text
from .models import Card, CardValidationResult, ValidationIssue, ValidationSummary


def _issue(rf_id: str, severity: str, message: str) -> ValidationIssue:
    return ValidationIssue(rf_id=rf_id, severity=severity, message=message)


def validate_card(card: Card) -> CardValidationResult:
    score = 100
    issues: List[ValidationIssue] = []

    if len(card.technical_checklist) < 3:
        score -= 20
        issues.append(_issue(card.rf_id, "alta", "Checklist tecnico com menos de 3 itens."))
    if len(card.qa_checklist) < 3:
        score -= 20
        issues.append(_issue(card.rf_id, "alta", "Checklist QA com menos de 3 itens."))
    if len(card.gherkin) < 3:
        score -= 25
        issues.append(_issue(card.rf_id, "alta", "Gherkin insuficiente para validacao."))

    gherkin_text = " ".join(card.gherkin).lower()
    if "dado" not in gherkin_text or "quando" not in gherkin_text or "entao" not in gherkin_text:
        score -= 20
        issues.append(_issue(card.rf_id, "media", "Gherkin sem estrutura Dado/Quando/Entao."))

    if not card.business_rules:
        score -= 10
        issues.append(_issue(card.rf_id, "media", "Sem regras de negocio declaradas."))
    if not card.labels:
        score -= 5
        issues.append(_issue(card.rf_id, "baixa", "Card sem labels."))

    status = "OK" if score >= 85 else "PENDENTE"
    return CardValidationResult(rf_id=card.rf_id, score=max(score, 0), status=status, issues=issues)


def validate_cards_from_payload(payload: List[dict[str, Any]]) -> ValidationSummary:
    results: List[CardValidationResult] = []
    for item in payload:
        try:
            card = Card.model_validate(item)
            result = validate_card(card)
        except ValidationError as exc:
            result = CardValidationResult(
                rf_id=item.get("rf_id", "RF???"),
                score=0,
                status="BLOQUEADO",
                issues=[_issue(item.get("rf_id", "RF???"), "alta", f"Schema invalido: {exc.errors()}")],
            )
        results.append(result)

    global_score = int(sum(r.score for r in results) / len(results)) if results else 0
    return ValidationSummary(global_score=global_score, results=results)


def save_validation_report(summary: ValidationSummary, dist_dir: Path) -> None:
    write_json(dist_dir / "qualidade-validacao.json", summary.model_dump(mode="json"))

    lines: list[str] = ["# Relatorio de Qualidade", "", f"Score global: {summary.global_score}", ""]
    for result in summary.results:
        lines.extend([f"## {result.rf_id}", f"- Status: {result.status}", f"- Score: {result.score}", "- Issues:"])
        if result.issues:
            for issue in result.issues:
                lines.append(f"  - [{issue.severity}] {issue.message}")
        else:
            lines.append("  - Nenhuma issue.")
        lines.append("")

    write_text(dist_dir / "qualidade-validacao.md", "\n".join(lines))
