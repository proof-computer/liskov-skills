"""Pin the managed Runtime SSH skill text. A missing live agent run is not a pass."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "liskov-access"
REQUIRED = (
    "before the first launch",
    "does not end the job",
    "--print-command",
    "do not generate a key",
)
REFERENCES = (
    "references/command-boundary.md",
    "references/limits.md",
    "references/eval-cases.md",
)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s\n]+)\)")
SECRET_MARKERS = (
    "sk_live",
    "AKIA",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN PRIVATE KEY",
    "liskov-" + "agent-" + "orchestrator",
)
PATH_ROOTS = ("home", "Users", "opt", "var", "tmp", "usr", "private", "etc", "mnt", "Volumes")
ABSOLUTE = re.compile(
    r"(?:^|[\s`'\"(=])/(?:" + "|".join(PATH_ROOTS) + r")/\S+"
    + r"|(?:^|[\s`'\"(=])" + re.escape("~" + "/") + r"\S+"
    + r"|(?:^|[\s`'\"(=])" + re.escape("file:" + "//")
)


def skill_markdown():
    return sorted(path for path in SKILL.rglob("*.md") if path.is_file())


def fence_commands(text):
    commands = []
    for block in FENCE.findall(text):
        folded = re.sub(r"\\\s*\n\s*", " ", block)
        for line in folded.splitlines():
            if re.search(r"\bproof\s+liskov\b", line):
                commands.append(line.strip())
    return commands


class AccessSkillTests(unittest.TestCase):
    def test_frontmatter_name_matches_directory(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0].strip(), "")
        front = parts[1]
        self.assertIn("name: liskov-access", front)
        self.assertEqual(SKILL.name, "liskov-access")
        self.assertRegex(front, r"(?m)^description:\s+\S")
        self.assertTrue(parts[2].strip())

    def test_required_substrings_and_relative_links(self):
        body = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for needle in REQUIRED:
            self.assertIn(needle, body)
        for relative in REFERENCES:
            self.assertIn(f"]({relative})", body)
            self.assertTrue((SKILL / relative).is_file(), relative)
        for path in skill_markdown():
            for target in LINK.findall(path.read_text(encoding="utf-8")):
                cleaned = target.split("#", 1)[0].split("?", 1)[0]
                if cleaned == "" or "://" in cleaned or cleaned.startswith("mailto:"):
                    continue
                resolved = (path.parent / cleaned).resolve()
                self.assertTrue(resolved.is_file(), f"{path} -> {target}")
                self.assertIn("liskov-access", resolved.as_posix())

    def test_every_proof_liskov_fence_opts_out_of_analytics(self):
        found = []
        verify = "proof liskov ssh APP --identity IDENTITY_PATH --print-command --json --no-analytics"
        bare = "proof liskov ssh APP --print-command --json --no-analytics"
        for path in skill_markdown():
            for line in fence_commands(path.read_text(encoding="utf-8")):
                found.append(line)
                self.assertIn("--no-analytics", line, line)
                self.assertNotIn("--yes", line)
                if "--accept-host-key" in line:
                    self.assertNotIn("--json", line, line)
                else:
                    self.assertIn("--json", line, line)
        self.assertIn(verify, found)
        self.assertNotIn(bare, found)
        self.assertNotIn("runtime-ssh integration", "\n".join(found))

    def test_eval_cases_are_not_a_live_pass(self):
        text = (SKILL / "references" / "eval-cases.md").read_text(encoding="utf-8")
        self.assertIn("A missing live agent run is not a pass.", text)
        sections = re.split(r"(?m)^## ", text)[1:]
        self.assertGreaterEqual(len(sections), 6)
        for section in sections:
            self.assertIn("Prompt:", section)
            self.assertIn("Required:", section)
            self.assertIn("Refused:", section)

    def test_forbidden_strings_are_absent(self):
        for path in skill_markdown():
            text = path.read_text(encoding="utf-8")
            for marker in SECRET_MARKERS:
                self.assertNotIn(marker, text, path)
            self.assertIsNone(ABSOLUTE.search(text), path)
            self.assertNotIn("file:" + "//", text, path)


if __name__ == "__main__":
    unittest.main()
