from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, List

from .io_utils import write_text


def export_cards_csv(cards_payload: List[dict[str, Any]], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "description", "labels", "priority"]
    with output_file.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for card in cards_payload:
            writer.writerow(
                {
                    "title": card.get("title", ""),
                    "description": card.get("objective", ""),
                    "labels": ",".join(card.get("labels", [])),
                    "priority": card.get("priority", "M"),
                }
            )


def export_cards_copy_paste(cards_payload: List[dict[str, Any]], output_file: Path) -> None:
    blocks: list[str] = ["# Cards para copiar e colar", "", "Sem integracao automatica com Trello/Jira.", ""]
    for card in cards_payload:
        blocks.extend(
            [
                f"TITULO: {card.get('title', '')}",
                f"PRIORIDADE: {card.get('priority', 'M')}",
                f"LABELS: {', '.join(card.get('labels', []))}",
                "DESCRICAO:",
                card.get("objective", ""),
                "",
                "----",
                "",
            ]
        )
    write_text(output_file, "\n".join(blocks))
