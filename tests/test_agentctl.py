from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


CORE = Path(__file__).resolve().parents[1]


class AgentctlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.paper = Path(self.tempdir.name) / "paper"
        self.paper.mkdir()
        subprocess.run(["git", "init", "-q", str(self.paper)], check=True)
        (self.paper / "AGENTS.md").write_text("# Paper instructions\n", encoding="utf-8")
        (self.paper / ".agent").mkdir()
        shutil.copytree(
            CORE,
            self.paper / ".agent" / "shared",
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        (self.paper / "tools").mkdir()
        (self.paper / "tools" / "agentctl").symlink_to("../.agent/shared/tools/agentctl")
        (self.paper / "agent-profile.json").write_text(
            (CORE / "agent-profile.json").read_text(encoding="utf-8"), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_tool(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.paper / "tools" / "agentctl"), *args],
            cwd=self.paper,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_discovers_paper_root(self) -> None:
        result = self.run_tool("root")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()), self.paper)

    def test_lists_shared_skills_with_origin(self) -> None:
        result = self.run_tool("skills", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        self.assertGreaterEqual(len(values), 16)
        self.assertTrue(all(item["origin"] == "shared" for item in values))

    def test_routes_only_relevant_skill_set(self) -> None:
        result = self.run_tool("route", "audit this manuscript derivation", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value["profiles"], ["manuscript"])
        self.assertEqual([item["name"] for item in value["skills"]], ["latex-manuscript-request-router"])

    def test_local_skill_cannot_shadow_shared_skill(self) -> None:
        local = self.paper / "agent_local" / "skills" / "commit"
        local.mkdir(parents=True)
        (local / "SKILL.md").write_text("---\nname: commit\ndescription: local\n---\n", encoding="utf-8")
        result = self.run_tool("skills")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate skill", result.stderr)

    def test_activation_copies_routed_skill(self) -> None:
        result = self.run_tool("activate", "codex", "verify a citation")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.paper / ".codex/skills/latex-citation-verifier/SKILL.md").is_file())
        self.assertFalse((self.paper / ".codex/skills/setup-moose-conda").exists())

    def test_commit_helper_resolves_compatibility_symlink(self) -> None:
        compatibility = self.paper / "agent_environment" / "skills" / "commit"
        compatibility.parent.mkdir(parents=True)
        compatibility.symlink_to("../../.agent/shared/skills/commit")
        helper = compatibility / "scripts" / "commit.sh"
        result = subprocess.run(
            [str(helper)], cwd=self.paper, text=True, capture_output=True, check=False
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)
        self.assertNotIn("agent_environment/tools", result.stderr)


if __name__ == "__main__":
    unittest.main()
