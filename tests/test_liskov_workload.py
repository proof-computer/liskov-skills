"""Pin the workload skill: fit decision, refusals, and no live-run pass."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "liskov-workload"
NAME = "liskov-workload"
REFUSALS = (
    "does not write a manifest",
    "does not publish",
    "no public inbound",
    "state.mode",
)
FORBIDDEN = (
    "sk_live",
    "AKIA",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "/" + "home/",
)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s\n]+)\)")


def skill_markdown():
    return sorted(SKILL.rglob("*.md"))


class WorkloadSkillTests(unittest.TestCase):
    def test_frontmatter_name_matches_directory(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        front, _body = text.split("---", 2)[1:]
        name = next(
            line for line in front.splitlines() if line.startswith("name:")
        )
        self.assertEqual(name, f"name: {NAME}")
        self.assertEqual(SKILL.name, NAME)
        description = next(
            line for line in front.splitlines() if line.startswith("description:")
        )
        self.assertIn("Use when", description)
        self.assertGreater(len(description.split(":", 1)[1].strip()), 0)

    def test_skill_contains_required_refusals(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for sentence in REFUSALS:
            self.assertIn(sentence, text)

    def test_relative_links_resolve(self):
        self.assertGreaterEqual(len(skill_markdown()), 4)
        for path in skill_markdown():
            for match in LINK.finditer(path.read_text(encoding="utf-8")):
                target = match.group(1).strip().split("#", 1)[0].split("?", 1)[0]
                if target == "" or "://" in target or target.startswith(("mailto:", "#")):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_file(), f"{path}: {target}")

    def test_proof_fences_pass_no_analytics(self):
        for path in skill_markdown():
            for block in FENCE.findall(path.read_text(encoding="utf-8")):
                if "proof liskov" in block:
                    self.assertIn("--no-analytics", block, path)

    def test_eval_cases_have_prompt_required_and_refused(self):
        text = (SKILL / "references" / "eval-cases.md").read_text(encoding="utf-8")
        self.assertIn("a missing live run is not a pass", text)
        bodies = re.split(r"(?=^## )", text, flags=re.MULTILINE)
        cases = [body for body in bodies if body.startswith("## ")]
        self.assertGreaterEqual(len(cases), 6)
        for body in cases:
            for label in ("Prompt:", "Required:", "Refused:"):
                self.assertIn(label, body)

    def test_skill_files_have_no_secret_markers(self):
        files = [path for path in SKILL.rglob("*") if path.is_file()]
        self.assertGreaterEqual(len(files), 4)
        for path in files:
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN:
                self.assertNotIn(token, text, f"{path}: {token}")


if __name__ == "__main__":
    unittest.main()
