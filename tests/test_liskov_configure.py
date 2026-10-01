"""Pin the liskov-configure skill: refusals, links, and the validate command."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "liskov-configure"
REFUSALS = (
    "does not publish",
    "never a credential",
    "decimal string",
    "Console",
)
FORBIDDEN = (
    "sk_live",
    "AKIA",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "/" + "home" + "/",
)
LINK = re.compile(r"\[[^\]\n]*\]\(<([^>\n]+)>\)|\[[^\]\n]*\]\(([^)\s\n]+)\)")
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
PROOF = re.compile(r"\bproof\s+liskov\b")
VALIDATE = (
    "proof liskov application manifest validate --file PATH --json --no-analytics"
)


def skill_text():
    parts = []
    for path in sorted(SKILL.rglob("*")):
        if path.is_file():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def proof_lines(text):
    found = []
    for block in FENCE.findall(text):
        folded = re.sub(r"\\\s*\n\s*", " ", block)
        for line in folded.splitlines():
            if PROOF.search(line):
                found.append(line.strip())
    return found


class LiskovConfigureTests(unittest.TestCase):
    def test_frontmatter_name(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        self.assertEqual(len(parts), 3)
        self.assertFalse(parts[0].strip())
        front = parts[1]
        match = re.search(r"(?m)^name:\s*(\S+)\s*$", front)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "liskov-configure")
        self.assertEqual(match.group(1), SKILL.name)
        self.assertRegex(front, r"(?m)^description:\s*\S")
        self.assertTrue(parts[2].strip())

    def test_refusal_substrings(self):
        blob = skill_text()
        for phrase in REFUSALS:
            self.assertIn(phrase, blob)
        self.assertIn(VALIDATE, blob)

    def test_relative_links_resolve_inside_the_skill(self):
        skill_root = SKILL.resolve()
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for match in LINK.finditer(text):
                target = (match.group(1) or match.group(2) or "").strip()
                target = target.split("#", 1)[0].split("?", 1)[0].strip()
                if target == "" or "://" in target or target.startswith(("mailto:", "#")):
                    continue
                if any(char in target for char in "{}[]^*"):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved == skill_root or skill_root in resolved.parents,
                    f"{path}: {target}",
                )
                self.assertTrue(resolved.is_file(), f"{path}: {target}")

    def test_proof_liskov_fences_disable_analytics(self):
        lines = []
        for path in SKILL.rglob("*.md"):
            lines.extend(proof_lines(path.read_text(encoding="utf-8")))
        self.assertGreater(len(lines), 0)
        for line in lines:
            self.assertIn("--no-analytics", line)
            self.assertIn("--json", line)
            self.assertIn("application manifest validate", line)
            self.assertNotIn("--organization", line)
            self.assertNotIn("--yes", line)
            self.assertNotIn("--dry-run", line)

    def test_eval_cases(self):
        text = (SKILL / "references" / "eval-cases.md").read_text(encoding="utf-8")
        self.assertIn("A missing live Claude/Codex run is not a pass.", text)
        parts = re.split(r"(?m)^## ", text)[1:]
        self.assertGreaterEqual(len(parts), 6)
        for part in parts:
            self.assertRegex(part, r"(?m)^Prompt:")
            self.assertRegex(part, r"(?m)^Required:")
            self.assertRegex(part, r"(?m)^Refused:")

    def test_forbidden_strings(self):
        for path in SKILL.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN:
                self.assertNotIn(token, text, f"{path}: {token}")


if __name__ == "__main__":
    unittest.main()
