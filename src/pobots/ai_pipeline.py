from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, List

import typer

from .exporter import export_cards_copy_paste, export_cards_csv
from .generator import generate_artifacts
from .io_utils import read_yaml, write_text, write_yaml
from .memory_store import MemoryLesson, add_lessons, ensure_memory_db, fetch_relevant_lessons, record_run
from .multi_bot import run_multi_bot_handoff
from .validator import save_validation_report, validate_cards_from_payload


def _extract_fenced_block(content: str, language: str) -> str:
    pattern = rf"```{language}\s*([\s\S]*?)```"
    match = re.search(pattern, content, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return content.strip()


def _chat_completion(
    *,
    token: str,
    model: str,
    messages: List[dict[str, str]],
    api_base_url: str,
    temperature: float = 0.2,
) -> str:
    url = api_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Falha na API de IA (HTTP {err.code}): {detail}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Falha de conexao com API de IA: {err}") from err

    parsed = json.loads(body)
    choices = parsed.get("choices", [])
    if not choices:
        raise RuntimeError("Resposta de IA sem choices.")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not content:
        raise RuntimeError("Resposta de IA sem content.")
    return content


def _load_prompt_bundle(repo_root: Path) -> str:
    files = [
        repo_root / "bots" / "framework-bots-base-documental.md",
        repo_root / "bots" / "prompts" / "prompt-mestre-bots-universal-v2.md",
        repo_root / "bots" / "prompts" / "prompt-pack-bots.md",
        repo_root / "bots" / "protocolo-handoff-bots.md",
    ]
    chunks: list[str] = []
    for file in files:
        if file.exists():
            chunks.append(f"# ARQUIVO: {file.name}\n\n{file.read_text(encoding='utf-8')}")
    return "\n\n".join(chunks)


def _llm_call_adapter(*, token: str, model: str, api_base_url: str):
    def _call(*, messages: List[dict[str, str]]) -> str:
        return _chat_completion(
            token=token,
            model=model,
            messages=messages,
            api_base_url=api_base_url,
        )

    return _call


def _generate_questions(
    *,
    token: str,
    model: str,
    task: str,
    prompt_bundle: str,
    api_base_url: str,
) -> list[str]:
    content = _chat_completion(
        token=token,
        model=model,
        api_base_url=api_base_url,
        messages=[
            {
                "role": "system",
                "content": (
                    "Voce e um analista senior. Gere no maximo 6 perguntas objetivas "
                    "para detalhar a task do cliente. Responda JSON puro no formato: "
                    '{"questions":["...","..."]}. Se nao precisar, retorne {"questions":[]}.'
                ),
            },
            {
                "role": "user",
                "content": f"TASK:\n{task}\n\nBASE:\n{prompt_bundle}",
            },
        ],
    )
    try:
        payload = json.loads(_extract_fenced_block(content, "json"))
    except json.JSONDecodeError:
        return []
    questions = payload.get("questions", [])
    if not isinstance(questions, list):
        return []
    return [str(item).strip() for item in questions if str(item).strip()]


def _auto_answer_questions(
    *,
    token: str,
    model: str,
    task: str,
    questions: list[str],
    api_base_url: str,
) -> dict[str, str]:
    if not questions:
        return {}
    content = _chat_completion(
        token=token,
        model=model,
        api_base_url=api_base_url,
        messages=[
            {
                "role": "system",
                "content": (
                    "Responda as perguntas com hipoteses conservadoras e explicitas. "
                    "Retorne JSON puro: {\"answers\":{\"pergunta\":\"resposta\"}}"
                ),
            },
            {
                "role": "user",
                "content": f"TASK:\n{task}\n\nPERGUNTAS:\n" + "\n".join([f"- {q}" for q in questions]),
            },
        ],
    )
    try:
        payload = json.loads(_extract_fenced_block(content, "json"))
    except json.JSONDecodeError:
        return {}
    answers = payload.get("answers", {})
    if not isinstance(answers, dict):
        return {}
    return {str(k): str(v) for k, v in answers.items()}


def _build_project_yaml(
    *,
    token: str,
    model: str,
    task: str,
    prompt_bundle: str,
    qa_pairs: dict[str, str],
    api_base_url: str,
) -> dict[str, Any]:
    qas = "\n".join([f"- {k}: {v}" for k, v in qa_pairs.items()]) or "- (sem perguntas)"
    content = _chat_completion(
        token=token,
        model=model,
        api_base_url=api_base_url,
        messages=[
            {
                "role": "system",
                "content": (
                    "Voce gera um YAML valido para project.yaml. "
                    "Responda apenas em bloco ```yaml``` seguindo o schema:\n"
                    "project{name,objective,audience,deadline,stack[],constraints[],assumptions[]}\n"
                    "functional_requirements[{id RF000,title,description,business_rules[],acceptance_criteria[],out_of_scope[],priority,labels[]}]\n"
                    "non_functional_requirements[{id RNF000,title,description}]\n"
                    "Inclua no minimo 3 RF e 2 RNF quando possivel."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"TASK DO CLIENTE:\n{task}\n\n"
                    f"Q&A DE DETALHAMENTO:\n{qas}\n\n"
                    f"PROMPTS BASE:\n{prompt_bundle}"
                ),
            },
        ],
    )
    yaml_text = _extract_fenced_block(content, "yaml")
    temp = Path("project.ai.tmp.yaml")
    write_text(temp, yaml_text)
    try:
        return read_yaml(temp)
    finally:
        if temp.exists():
            temp.unlink()


def run_ai_pipeline(
    *,
    repo_root: Path,
    task: str,
    token: str,
    model: str,
    api_base_url: str,
    interactive: bool,
    project_file: Path,
    dist_dir: Path,
) -> Path:
    memory_db = repo_root / "memory" / "bots_memory.db"
    ensure_memory_db(memory_db)
    lessons = fetch_relevant_lessons(memory_db, task=task, limit=5)
    memory_notes = [f"{item.category}: {item.solution} (resultado: {item.result})" for item in lessons]

    prompt_bundle = _load_prompt_bundle(repo_root)
    if memory_notes:
        prompt_bundle += "\n\n# MEMORIA OPERACIONAL\n" + "\n".join([f"- {note}" for note in memory_notes])

    questions = _generate_questions(
        token=token,
        model=model,
        task=task,
        prompt_bundle=prompt_bundle,
        api_base_url=api_base_url,
    )

    answers: dict[str, str] = {}
    unresolved: list[str] = []
    for question in questions:
        if interactive:
            answer = typer.prompt(f"{question} (enter vazio = IA decide)", default="", show_default=False)
            if answer.strip():
                answers[question] = answer.strip()
            else:
                unresolved.append(question)
        else:
            unresolved.append(question)

    if unresolved:
        auto_answers = _auto_answer_questions(
            token=token,
            model=model,
            task=task,
            questions=unresolved,
            api_base_url=api_base_url,
        )
        for question in unresolved:
            answers[question] = auto_answers.get(question, "Hipotese padrao aplicada pela IA.")

    llm_call = _llm_call_adapter(token=token, model=model, api_base_url=api_base_url)
    bot_outputs, refined_task = run_multi_bot_handoff(
        task=task,
        qa_pairs=answers,
        memory_notes=memory_notes,
        prompt_bundle=prompt_bundle,
        llm_call=llm_call,
    )

    project_payload = _build_project_yaml(
        token=token,
        model=model,
        task=refined_task,
        prompt_bundle=prompt_bundle,
        qa_pairs=answers,
        api_base_url=api_base_url,
    )
    write_yaml(project_file, project_payload)

    cards, run_dir = generate_artifacts(project_file=project_file, dist_dir=dist_dir)
    cards_payload = [card.model_dump(mode="json") for card in cards]
    backlog_dir = run_dir / "06-backlog"
    summary = validate_cards_from_payload(cards_payload)
    save_validation_report(summary, backlog_dir)
    export_cards_csv(cards_payload, backlog_dir / "cards-trello.csv")
    export_cards_copy_paste(cards_payload, backlog_dir / "cards-copy-paste.txt")

    qa_md = ["# Perguntas e Respostas da IA", ""]
    if answers:
        for question, answer in answers.items():
            qa_md.extend([f"## {question}", answer, ""])
    else:
        qa_md.append("- Nenhuma pergunta adicional necessaria.")
    write_text(run_dir / "qa-detalhamento-ia.md", "\n".join(qa_md))

    audit_payload = {
        "run": run_dir.name,
        "task_original": task,
        "task_refinada": refined_task,
        "questions": questions,
        "answers": answers,
        "bot_outputs": bot_outputs,
        "memory_used": memory_notes,
        "global_score": summary.global_score,
    }
    write_text(run_dir / "audit-log.json", json.dumps(audit_payload, ensure_ascii=False, indent=2))

    derived_lessons = []
    for item in bot_outputs:
        if item["acoes_recomendadas"]:
            derived_lessons.append(
                MemoryLesson(
                    category=item["bot"],
                    problem=item["resumo"],
                    solution="; ".join(item["acoes_recomendadas"]),
                    result=f"status={item['status']}",
                    confidence=0.75 if item["status"] == "OK" else 0.6,
                )
            )
    if derived_lessons:
        add_lessons(
            memory_db,
            project=project_payload.get("project", {}).get("name", "projeto"),
            sprint=run_dir.name,
            lessons=derived_lessons,
        )
    record_run(
        memory_db,
        run_name=run_dir.name,
        project=project_payload.get("project", {}).get("name", "projeto"),
        task=task,
        score=summary.global_score,
    )

    return run_dir
