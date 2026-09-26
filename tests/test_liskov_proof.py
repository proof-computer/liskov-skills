"""Pin the liskov-proof skill text.

A missing live agent run is not a pass.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "liskov-proof"
NAME = "liskov-proof"
REQUIRED = ("read only", "does not prove", "no processor list", "unpublished")
REFERENCES = (
    "references/command-boundary.md",
    "references/limits.md",
    "references/eval-cases.md",
)
FORBIDDEN = (
    "sk_live",
    "AKIA",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "/" + "home/",
)
ALLOWED = (
    "proof liskov application artifact-pin list ",
    "proof liskov application deployment status ",
    "proof liskov application plans ",
    "proof liskov application policy explain ",
    "proof liskov application source-binding show ",
    "proof liskov application status ",
    "proof liskov organization use ",
    "proof liskov whoami ",
)


def markdown_files():
    return sorted(path for path in SKILL.rglob("*.md") if path.is_file())


def combined():
    return "\n".join(path.read_text(encoding="utf-8") for path in markdown_files())


def proof_lines(text):
    folded = re.sub(r"\\\s*\n\s*", " ", text)
    return [line.strip() for line in folded.splitlines() if re.search(r"\bproof\s+liskov\b", line)]


class ProofSkillTests(unittest.TestCase):
    def test_frontmatter_name(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0].strip(), "")
        front = parts[1]
        self.assertIn("name: " + NAME, front)
        self.assertRegex(front, r"(?m)^description:\s*\S")
        self.assertTrue(parts[2].strip())
        for relative in REFERENCES:
            self.assertIn("](" + relative + ")", parts[2])
            self.assertTrue((SKILL / relative).is_file())

    def test_required_refusal_substrings(self):
        text = combined()
        for phrase in REQUIRED:
            self.assertIn(phrase, text, phrase)

    def test_relative_links_resolve_inside_the_skill(self):
        skill_root = SKILL.resolve()
        link = re.compile(r"\[[^\]\n]*\]\(([^)\s\n]+)\)")
        seen = 0
        for path in markdown_files():
            for match in link.finditer(path.read_text(encoding="utf-8")):
                target = match.group(1).strip().split("#", 1)[0].split("?", 1)[0]
                if target == "" or "://" in target or target.startswith("mailto:"):
                    continue
                seen += 1
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_file(), target)
                self.assertTrue(resolved == skill_root or skill_root in resolved.parents)
        self.assertGreaterEqual(seen, 3)

    def test_every_proof_liskov_line_disables_analytics(self):
        lines = proof_lines(combined())
        self.assertGreater(len(lines), 0)
        for line in lines:
            self.assertIn("--no-analytics", line)
            self.assertIn("--json", line)
            self.assertTrue(line.startswith(ALLOWED), line)

    def test_eval_cases_have_prompt_required_and_refused(self):
        text = (SKILL / "references" / "eval-cases.md").read_text(encoding="utf-8")
        sections = re.split(r"(?m)^## ", text)[1:]
        self.assertGreaterEqual(len(sections), 6)
        for section in sections:
            self.assertRegex(section, r"(?m)^Prompt:")
            self.assertRegex(section, r"(?m)^Required:")
            self.assertRegex(section, r"(?m)^Refused:")

    def test_no_secrets_or_machine_paths(self):
        text = combined()
        for phrase in FORBIDDEN:
            self.assertNotIn(phrase, text, phrase)

    def test_missing_live_agent_run_is_not_a_pass(self):
        """A missing live agent run is not a pass."""
        self.assertIn(
            "A missing live agent run is not a pass.",
            (SKILL / "SKILL.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
