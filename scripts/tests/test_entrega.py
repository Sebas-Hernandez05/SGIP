"""Verifica aceptación de commits normales e integraciones en repositorios aislados."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "entrega.py"


class EntregaTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.repo = Path(self.directory.name)
        self.git("init", "-q", "-b", "entrega/prueba")
        self.git("config", "user.name", "QA")
        self.git("config", "user.email", "qa@example.test")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.repo / "hooks-vacios"))
        self.git("commit", "--allow-empty", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], cwd=self.repo, text=True, stderr=subprocess.PIPE
        ).strip()

    def run_script(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], cwd=self.repo,
            text=True, capture_output=True, check=check,
        )

    def stage(self, name, content):
        (self.repo / name).write_text(content, encoding="utf-8")
        self.git("add", "--", name)

    def prepare_merge(self):
        self.git("switch", "-qc", "develop")
        self.stage("develop.txt", "configuración del coordinador\n")
        self.git("commit", "-qm", "coordinación")
        develop = self.git("rev-parse", "HEAD")
        self.git("switch", "entrega/prueba")
        self.stage("registro.txt", "registro aceptado\n")
        self.git("commit", "-qm", "registro")
        parent = self.git("rev-parse", "HEAD")
        self.git("merge", "--no-commit", "--no-ff", "develop")
        return parent, develop

    def test_normal_commit_keeps_previous_fingerprint_format(self):
        self.stage("registro.txt", "registro\n")
        tree = self.git("write-tree")
        expected = hashlib.sha256(json.dumps([
            "refs/heads/entrega/prueba", self.base, tree,
        ]).encode()).hexdigest()
        fingerprint = self.run_script("preparar").stdout.strip()
        self.assertEqual(fingerprint, expected)
        result = self.run_script("commit", fingerprint, "revisión de QA", "entrega")
        self.assertEqual(result.stdout.strip(), self.git("rev-parse", "HEAD"))
        self.assertEqual(self.git("show", "-s", "--format=%P %T"), f"{self.base} {tree}")

    def test_merge_commit_preserves_both_parents_and_approved_tree(self):
        parent, develop = self.prepare_merge()
        tree = self.git("write-tree")
        fingerprint = self.run_script("preparar").stdout.strip()
        self.run_script("commit", fingerprint, "revisión de QA", "integra develop")
        self.assertEqual(self.git("show", "-s", "--format=%P %T"), f"{parent} {develop} {tree}")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_merge_rejects_changed_staged_content(self):
        parent, _ = self.prepare_merge()
        fingerprint = self.run_script("preparar").stdout.strip()
        self.stage("develop.txt", "contenido posterior a la revisión\n")
        result = self.run_script("commit", fingerprint, "QA", "integra", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), parent)

    def test_merge_rejects_changed_parent_with_same_tree(self):
        parent, _ = self.prepare_merge()
        fingerprint = self.run_script("preparar").stdout.strip()
        merge_head = self.repo / self.git("rev-parse", "--git-path", "MERGE_HEAD")
        merge_head.write_text(self.base + "\n", encoding="utf-8")
        result = self.run_script("commit", fingerprint, "QA", "integra", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), parent)

    def test_unresolved_conflicts_cannot_be_accepted(self):
        self.stage("compartido.txt", "original\n")
        self.git("commit", "-qm", "archivo compartido")
        self.git("switch", "-qc", "develop")
        self.stage("compartido.txt", "develop\n")
        self.git("commit", "-qm", "cambio develop")
        self.git("switch", "entrega/prueba")
        self.stage("compartido.txt", "entrega\n")
        self.git("commit", "-qm", "cambio entrega")
        subprocess.run(["git", "merge", "--no-commit", "develop"], cwd=self.repo,
                       check=False, capture_output=True)
        result = self.run_script("preparar", check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_other_operations_still_block_acceptance(self):
        self.stage("registro.txt", "registro\n")
        for name in ("CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
            with self.subTest(operation=name):
                marker = self.repo / self.git("rev-parse", "--git-path", name)
                marker.write_text(self.base + "\n", encoding="utf-8")
                try:
                    result = self.run_script("preparar", check=False)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("operación de Git", result.stderr)
                finally:
                    marker.unlink()


if __name__ == "__main__":
    unittest.main()
