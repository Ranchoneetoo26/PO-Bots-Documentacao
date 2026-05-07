from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import shutil

from pobots.generator import generate_artifacts
from pobots.io_utils import write_yaml
from pobots.memory_store import MemoryLesson, add_lessons, ensure_memory_db, fetch_relevant_lessons
from pobots.multi_bot import parse_bot_output


class CorePipelineTests(unittest.TestCase):
    def test_generate_artifacts_creates_segmented_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_file = root / "project.yaml"
            dist_dir = root / "dist"
            write_yaml(
                project_file,
                {
                    "project": {
                        "name": "Projeto Teste",
                        "objective": "Objetivo de teste para gerar artefatos.",
                        "audience": "Time",
                        "deadline": "2026-12-31",
                        "stack": ["Python"],
                        "constraints": [],
                        "assumptions": [],
                    },
                    "functional_requirements": [
                        {
                            "id": "RF001",
                            "title": "Cadastro",
                            "description": "Permitir cadastro.",
                            "business_rules": ["Nome obrigatorio."],
                            "acceptance_criteria": ["Cadastrar com sucesso."],
                            "out_of_scope": [],
                            "priority": "M",
                            "labels": ["backend"],
                        }
                    ],
                    "non_functional_requirements": [],
                },
            )

            cards, run_dir = generate_artifacts(project_file=project_file, dist_dir=dist_dir)
            self.assertEqual(1, len(cards))
            self.assertTrue((run_dir / "01-dvp-e" / "dvp-e.md").exists())
            self.assertTrue((run_dir / "02-dvs" / "dvs.md").exists())
            self.assertTrue((run_dir / "03-drp" / "drp.md").exists())
            self.assertTrue((run_dir / "04-dat" / "dat.md").exists())
            self.assertTrue((run_dir / "05-gdr" / "gdr.md").exists())
            self.assertTrue((run_dir / "06-backlog" / "cards.json").exists())

    def test_memory_store_roundtrip(self) -> None:
        tmp = tempfile.mkdtemp()
        try:
            db_file = Path(tmp) / "memory" / "bots_memory.db"
            ensure_memory_db(db_file)
            add_lessons(
                db_file,
                project="Projeto X",
                sprint="S1",
                lessons=[
                    MemoryLesson(
                        category="BOT_QA",
                        problem="Ambiguidade no RF de cadastro",
                        solution="Incluir checklist QA por campo",
                        result="reduziu retrabalho",
                        confidence=0.9,
                    )
                ],
            )
            lessons = fetch_relevant_lessons(db_file, task="Cadastro de cliente com validacao")
            self.assertGreaterEqual(len(lessons), 1)
            self.assertIn("checklist", lessons[0].solution.lower())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_parse_bot_output_fallback(self) -> None:
        payload = parse_bot_output("BOT_ANALISTA", "texto invalido")
        self.assertEqual("BOT_ANALISTA", payload["bot"])
        self.assertEqual("PENDENTE", payload["status"])
        self.assertIsInstance(payload["acoes_recomendadas"], list)


if __name__ == "__main__":
    unittest.main()
