from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple


BOT_ORDER = [
    ("BOT_ANALISTA", "Transforma demanda em requisitos executaveis, claros e testaveis."),
    ("BOT_ARQUITETO", "Valida arquitetura, riscos tecnicos e aderencia ao DAT."),
    ("BOT_CEO", "Valida valor, prioridade e impacto de negocio."),
    ("BOT_DEV_BACK", "Detalha backend, API, dominio, validacoes e dados."),
    ("BOT_DEV_FRONT", "Detalha frontend, fluxo de tela, UX e validacoes por campo."),
    ("BOT_QA", "Define estrategia de testes e bloqueia gaps de qualidade."),
]


def parse_bot_output(bot_name: str, raw_content: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        parsed = {}
    if not isinstance(parsed, dict):
        parsed = {}

    status = str(parsed.get("status", "PENDENTE")).upper()
    if status not in {"OK", "PENDENTE", "BLOQUEADO"}:
        status = "PENDENTE"

    def ensure_list(value: Any) -> List[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        return []

    return {
        "bot": str(parsed.get("bot", bot_name)),
        "status": status,
        "resumo": str(parsed.get("resumo", "Sem resumo objetivo.")),
        "achados": ensure_list(parsed.get("achados")),
        "acoes_recomendadas": ensure_list(parsed.get("acoes_recomendadas")),
        "evidencias_documentais": ensure_list(parsed.get("evidencias_documentais")),
        "criterios_gate": ensure_list(parsed.get("criterios_gate")),
    }


def run_multi_bot_handoff(
    *,
    task: str,
    qa_pairs: Dict[str, str],
    memory_notes: List[str],
    prompt_bundle: str,
    llm_call,
) -> Tuple[List[Dict[str, Any]], str]:
    qa_text = "\n".join([f"- {key}: {value}" for key, value in qa_pairs.items()]) or "- (sem perguntas)"
    memory_text = "\n".join([f"- {note}" for note in memory_notes]) or "- (sem memoria operacional)"
    shared_context = (
        f"TASK ORIGINAL:\n{task}\n\n"
        f"Q&A:\n{qa_text}\n\n"
        f"MEMORIA OPERACIONAL:\n{memory_text}\n\n"
        f"BASE DOCUMENTAL:\n{prompt_bundle}"
    )

    bot_outputs: List[Dict[str, Any]] = []
    prior_summary = "Sem analise anterior."
    for bot_name, mission in BOT_ORDER:
        messages = [
            {
                "role": "system",
                "content": (
                    f"Voce e {bot_name}. Missao: {mission}\n"
                    "Responda JSON puro no schema:\n"
                    '{"bot":"NOME","status":"OK|PENDENTE|BLOQUEADO","resumo":"...","achados":["..."],'
                    '"acoes_recomendadas":["..."],"evidencias_documentais":["..."],"criterios_gate":["..."]}\n'
                    "Nao use markdown e nao retorne texto fora do JSON."
                ),
            },
            {
                "role": "user",
                "content": f"{shared_context}\n\nSUMARIO ANTERIOR:\n{prior_summary}",
            },
        ]
        raw = llm_call(messages=messages)
        output = parse_bot_output(bot_name, raw)
        bot_outputs.append(output)
        prior_summary = f"{output['resumo']} | Acoes: {', '.join(output['acoes_recomendadas'])}"
        if output["status"] == "BLOQUEADO":
            break

    refined_parts = [f"TASK: {task}", "AJUSTES RECOMENDADOS:"]
    for item in bot_outputs:
        refined_parts.append(f"- {item['bot']} [{item['status']}]: {item['resumo']}")
        for action in item["acoes_recomendadas"]:
            refined_parts.append(f"  * {action}")
    refined_task = "\n".join(refined_parts)
    return bot_outputs, refined_task
