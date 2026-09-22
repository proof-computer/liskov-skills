"""Pin the bootstrap gate's rejection of empty or malformed skill entries."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("validate", Path(__file__).resolve().parents[1] / "scripts/validate.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


class SkillStructureTests(unittest.TestCase):
    def errors(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(text)
            return validate.skill_errors(path)

    def test_rejects_missing_frontmatter_and_description(self):
        self.assertTrue(self.errors("# Just a heading"))
        self.assertIn("missing description", self.errors("---\nname: liskov-policy\n---\nInstructions"))

    def test_rejects_empty_body_and_accepts_shared_entrypoint(self):
        metadata = "---\nname: liskov-policy\ndescription: Create a V5+ policy.\n---\n"
        self.assertIn("empty skill instructions", self.errors(metadata))
        self.assertEqual([], self.errors(metadata + "Use the supported owner validator."))
