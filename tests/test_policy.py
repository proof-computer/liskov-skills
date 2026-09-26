"""Pin the V5 policy skill: fixture bytes, recorded readback, and no mutation."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "liskov-policy"
FIXTURES = SKILL / "assets" / "fixtures"
HELPER = SKILL / "scripts" / "validate_manifest.py"

STARTER = """\
{
  "schema": "proof.liskov.application-manifest",
  "schemaVersion": 5,
  "applicationId": "hello-liskov",
  "metadata": {
    "description": "Fetch example.com and record the HTTP result in managed logs."
  },
  "release": {
    "mode": "source"
  },
  "runtime": {
    "kind": "javascript",
    "engine": "nodejs",
    "entrypoint": {
      "file": "bundle.js"
    }
  },
  "execution": {
    "mode": "once"
  },
  "deployment": {
    "schedule": {
      "duration": "60s"
    },
    "spend": {
      "unit": "service_credit_micros",
      "perJob": "50000"
    }
  },
  "state": {
    "mode": "off"
  },
  "observability": {
    "logs": {
      "enabled": true
    }
  }
}
"""

RECORDED_READBACK = {
    "ok": True,
    "manifestValid": True,
    "schemaVersion": 5,
    "authoredDigest": "f70cbce1bcd00d84241d022f654e5f49f000e0cb214296c93c5e3b1b9c084873",
    "releaseIntentDigest": "854fa5568c55b627b85d3cdc79ff56bf798d12a8450a96245edb7d76ecb3315b",
    "firstPublicReady": True,
    "errors": [],
    "capabilityDiagnostics": [],
    "deprecationDiagnostics": [],
}

DRAFTING_COMMAND = (
    "proof liskov application manifest validate --file PATH --json --no-analytics"
)

JOURNEY = (
    "## 1. Requirements",
    "## 2. Local draft",
    "## 3. Validation and repair",
    "## 4. Explanation",
    "## 5. Unresolved requirements",
)


def fixture_text(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def reject_duplicate_keys(pairs):
    keys = [key for key, _value in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate JSON key")
    return dict(pairs)


def proof_liskov_lines(text):
    folded = re.sub(r"\\\s*\n\s*", " ", text)
    return [line for line in folded.splitlines() if re.search(r"\bproof\s+liskov\b", line)]


class PolicyFixtureTests(unittest.TestCase):
    def test_starter_bytes_match_the_public_sample(self):
        self.assertEqual(fixture_text("retained-v5-starter.json"), STARTER)
        document = json.loads(STARTER, object_pairs_hook=reject_duplicate_keys)
        self.assertEqual(document["schema"], "proof.liskov.application-manifest")
        self.assertEqual(document["schemaVersion"], 5)
        self.assertEqual(document["applicationId"], "hello-liskov")
        self.assertEqual(document["deployment"]["spend"]["perJob"], "50000")

    def test_other_fixtures_are_the_starter_with_one_contract_change(self):
        expected = {
            "invalid-duration.json": STARTER.replace(
                '"duration": "60s"', '"duration": "60"', 1
            ),
            "missing-application-id.json": STARTER.replace(
                '  "applicationId": "hello-liskov",\n', "", 1
            ),
            "schema-v6.json": STARTER.replace(
                '"schemaVersion": 5', '"schemaVersion": 6', 1
            ),
            "jobs-zero.json": STARTER.replace(
                '  "deployment": {\n    "schedule": {',
                '  "deployment": {\n    "jobs": 0,\n    "schedule": {',
                1,
            ),
            "unsupported-ingress.json": STARTER.replace(
                '      "enabled": true\n    }\n  }\n}\n',
                '      "enabled": true\n    }\n  },\n  "ingress": {}\n}\n',
                1,
            ),
            "secret-value.json": STARTER.replace(
                '  "state": {\n    "mode": "off"\n  },\n',
                (
                    '  "configuration": {\n'
                    '    "secrets": [\n'
                    '      {\n'
                    '        "secretId": "api-token",\n'
                    '        "destination": {\n'
                    '          "kind": "environment",\n'
                    '          "name": "API_TOKEN"\n'
                    '        },\n'
                    '        "value": "rejected-secret-value"\n'
                    '      }\n'
                    '    ]\n'
                    '  },\n'
                    '  "state": {\n'
                    '    "mode": "off"\n'
                    '  },\n'
                ),
                1,
            ),
        }
        self.assertEqual(sorted(path.name for path in FIXTURES.glob("*.json")), sorted([
            "retained-v5-starter.json",
            *expected,
        ]))
        for name, text in expected.items():
            self.assertNotEqual(text, STARTER, name)
            self.assertEqual(fixture_text(name), text, name)
            json.loads(text, object_pairs_hook=reject_duplicate_keys)

    def test_fixture_changes_keep_their_contract_meaning(self):
        self.assertEqual(
            json.loads(fixture_text("invalid-duration.json"))["deployment"]["schedule"]["duration"],
            "60",
        )
        self.assertNotIn("applicationId", json.loads(fixture_text("missing-application-id.json")))
        self.assertEqual(json.loads(fixture_text("schema-v6.json"))["schemaVersion"], 6)
        self.assertEqual(json.loads(fixture_text("jobs-zero.json"))["deployment"]["jobs"], 0)
        self.assertEqual(json.loads(fixture_text("unsupported-ingress.json"))["ingress"], {})
        secret = json.loads(fixture_text("secret-value.json"))["configuration"]["secrets"][0]
        self.assertEqual(secret["secretId"], "api-token")
        self.assertEqual(secret["value"], "rejected-secret-value")

    def test_recorded_starter_readback_is_pinned(self):
        self.assertEqual(RECORDED_READBACK["schemaVersion"], 5)
        self.assertTrue(RECORDED_READBACK["manifestValid"])
        self.assertEqual(
            RECORDED_READBACK["authoredDigest"],
            "f70cbce1bcd00d84241d022f654e5f49f000e0cb214296c93c5e3b1b9c084873",
        )
        self.assertEqual(
            RECORDED_READBACK["releaseIntentDigest"],
            "854fa5568c55b627b85d3cdc79ff56bf798d12a8450a96245edb7d76ecb3315b",
        )
        boundary = (SKILL / "references" / "command-boundary.md").read_text(encoding="utf-8")
        match = re.search(r"```json\n(\{.*?\n\})\n```", boundary, re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), RECORDED_READBACK)


class PolicyInstructionTests(unittest.TestCase):
    def test_frontmatter_triggers_on_v5_not_v4(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        front = text.split("---", 2)[1]
        description = next(
            line for line in front.splitlines() if line.startswith("description:")
        )
        self.assertIn("name: liskov-policy", front)
        self.assertIn("V5", description)
        self.assertIn("proof.liskov.application-manifest", description)
        self.assertNotIn("V4", description)
        self.assertNotIn("v4", description)
        body = text.split("---", 2)[2]
        positions = [body.index(heading) for heading in JOURNEY]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(".liskov/application-manifest.json", body)
        self.assertIn("hello-liskov", body)
        self.assertIn('"50000"', body)
        self.assertIn("at most three", body)
        self.assertIn("owner validator did not run", body)
        self.assertIn("version 4", body)
        self.assertIn("version 6", body)
        self.assertIn("out of scope", body)
        self.assertIn("manifestValid", body)
        self.assertIn("firstPublicReady", body)
        self.assertIn("secretId", body)

    def test_skill_tree_names_only_the_drafting_command(self):
        files = [
            path
            for path in SKILL.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".sh"}
        ]
        self.assertGreaterEqual(len(files), 5)
        found = []
        for path in files:
            for line in proof_liskov_lines(path.read_text(encoding="utf-8")):
                found.append((path, line))
                match = re.search(
                    r"\bproof\s+liskov\s+application\s+manifest\s+validate\s+"
                    r"--file\s+\S+\s+--json\s+--no-analytics\b",
                    line,
                )
                self.assertIsNotNone(match, f"{path}: {line}")
                tail = line[match.end():].strip(" `\"').,")
                self.assertEqual(tail, "", f"{path}: {line}")
        self.assertEqual(
            sorted(path.relative_to(SKILL).as_posix() for path, _line in found),
            [
                "SKILL.md",
                "references/command-boundary.md",
                "scripts/validate_manifest.py",
            ],
        )
        self.assertIn(DRAFTING_COMMAND, (SKILL / "SKILL.md").read_text(encoding="utf-8"))

    def test_references_keep_mutation_commands_off_the_drafting_path(self):
        boundary = (SKILL / "references" / "command-boundary.md").read_text(encoding="utf-8")
        for name in (
            "application create",
            "application import",
            "application policy publish",
            "application policy explain",
            "application publish",
            "source-binding set",
            "custody execution",
            "--dry-run",
        ):
            self.assertIn(name, boundary)
        verdicts = (SKILL / "references" / "verdicts.md").read_text(encoding="utf-8")
        self.assertIn("schemaVersion", verdicts)
        self.assertIn("out of scope", verdicts.lower())
        self.assertIn("firstPublicReady", verdicts)
        rules = (SKILL / "references" / "field-rules.md").read_text(encoding="utf-8")
        self.assertIn("hello-liskov", rules)
        self.assertIn('"50000"', rules)
        self.assertIn("/configuration/secrets/0/value", rules)
        self.assertIn("jobs", rules)

    def test_secret_marker_is_not_copied_into_instructions(self):
        for path in SKILL.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".py"}:
                continue
            if path.name == "secret-value.json":
                continue
            self.assertNotIn(
                "rejected-secret-value",
                path.read_text(encoding="utf-8"),
                path,
            )


class PolicyHelperTests(unittest.TestCase):
    def test_helper_source_cannot_shell_out_to_another_command(self):
        text = HELPER.read_text(encoding="utf-8")
        self.assertIn(DRAFTING_COMMAND, text)
        self.assertNotIn("shell=True", text)
        self.assertNotIn("os.system", text)
        self.assertEqual(text.count("proof liskov"), 1)

    def test_helper_refuses_every_other_command_without_running_proof(self):
        starter = FIXTURES / "retained-v5-starter.json"
        refused = [
            [],
            ["--help"],
            ["proof", "liskov", "application", "create"],
            ["proof", "liskov", "application", "import", "manifest.json"],
            ["proof", "liskov", "application", "policy", "publish", "--dry-run"],
            ["proof", "liskov", "application", "policy", "publish", "--yes"],
            ["proof", "liskov", "application", "policy", "explain", "hello-liskov"],
            ["proof", "liskov", "application", "publish"],
            ["proof", "liskov", "application", "source-binding", "set"],
            ["proof", "liskov", "application", "pause"],
            ["proof", "liskov", "application", "resume"],
            ["proof", "liskov", "application", "run"],
            ["proof", "liskov", "custody"],
            ["--file", str(starter), "--dry-run"],
            ["--file", str(starter), "--json"],
            ["--file", str(starter), "--no-analytics"],
            [
                "proof",
                "liskov",
                "application",
                "manifest",
                "validate",
                "--file",
                str(starter),
                "--json",
                "--no-analytics",
            ],
            ["--file", ""],
            ["--file", "--no-analytics"],
        ]
        for args in refused:
            with self.subTest(args=args):
                self.assertTrue(self.run_helper(args, proof="fake").refused)

    def test_helper_runs_only_validate_when_proof_is_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "application-manifest.json"
            target.write_text(STARTER, encoding="utf-8")
            outcome = self.run_helper(["--file", str(target)], proof="fake")
        self.assertFalse(outcome.refused)
        self.assertEqual(outcome.returncode, 0)
        self.assertEqual(
            outcome.argv,
            [
                "liskov",
                "application",
                "manifest",
                "validate",
                "--file",
                str(target),
                "--json",
                "--no-analytics",
            ],
        )
        self.assertEqual(json.loads(outcome.stdout), {"ok": True})

    def test_helper_reports_a_missing_validator_without_passing(self):
        outcome = self.run_helper(
            ["--file", str(FIXTURES / "retained-v5-starter.json")],
            proof="missing",
        )
        self.assertEqual(outcome.returncode, 127)
        self.assertIn("owner validator did not run", outcome.stderr)
        self.assertNotIn("manifestValid", outcome.stdout)
        self.assertIsNone(outcome.argv)

    def run_helper(self, args, proof):
        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / "argv.log"
            env = os.environ.copy()
            env["PROOF_ARGV_LOG"] = str(log_path)
            if proof == "fake":
                bindir = Path(directory) / "bin"
                bindir.mkdir()
                binary = bindir / "proof"
                binary.write_text(
                    "#!/bin/sh\n"
                    'printf "%s\\n" "$@" >> "$PROOF_ARGV_LOG"\n'
                    'printf "%s\\n" \'{"ok":true}\'\n',
                    encoding="utf-8",
                )
                binary.chmod(0o755)
                env["PATH"] = str(bindir)
            elif proof == "missing":
                env["PATH"] = str(Path(directory) / "empty")
                Path(env["PATH"]).mkdir()
            completed = subprocess.run(
                [sys.executable, str(HELPER), *args],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
            argv = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else None
        return HelperOutcome(
            completed.returncode,
            completed.stdout,
            completed.stderr,
            argv,
            refused=completed.returncode == 2 and argv is None and "refused:" in completed.stderr,
        )


class HelperOutcome:
    def __init__(self, returncode, stdout, stderr, argv, refused):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.argv = argv
        self.refused = refused


@unittest.skipUnless(shutil.which("proof"), "proof CLI is not installed")
class PolicyLiveCliTests(unittest.TestCase):
    def test_live_starter_matches_recorded_readback(self):
        verdict, returncode = run_validate(FIXTURES / "retained-v5-starter.json")
        self.assertEqual(returncode, 0)
        self.assertEqual(verdict, RECORDED_READBACK)

    def test_live_helper_matches_recorded_readback(self):
        completed = subprocess.run(
            [sys.executable, str(HELPER), "--file", str(FIXTURES / "retained-v5-starter.json")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout), RECORDED_READBACK)

    def test_live_schema_v6_is_still_not_a_skill_success(self):
        verdict, returncode = run_validate(FIXTURES / "schema-v6.json")
        self.assertEqual(returncode, 0)
        self.assertTrue(verdict["manifestValid"])
        self.assertEqual(verdict["schemaVersion"], 6)
        self.assertTrue(verdict["firstPublicReady"])
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("schemaVersion", skill)
        self.assertIn("out of scope", skill)

    def test_live_negative_fixtures_match_the_recorded_diagnostics(self):
        expected = {
            "invalid-duration.json": ("invalid_manifest", "/deployment/schedule/duration"),
            "unsupported-ingress.json": ("unknown_field", "/ingress"),
            "missing-application-id.json": ("invalid_manifest", ""),
            "secret-value.json": ("unknown_field", "/configuration/secrets/0/value"),
            "jobs-zero.json": ("invalid_manifest", "/deployment/jobs"),
        }
        for name, (code, pointer) in expected.items():
            with self.subTest(name=name):
                verdict, returncode = run_validate(FIXTURES / name)
                self.assertEqual(returncode, 1)
                self.assertFalse(verdict["manifestValid"])
                self.assertEqual(verdict["schemaVersion"], 5)
                self.assertEqual(verdict["errors"][0]["code"], code)
                self.assertEqual(verdict["errors"][0]["pointer"], pointer)
                self.assertNotIn("rejected-secret-value", json.dumps(verdict))


def run_validate(path):
    completed = subprocess.run(
        [
            "proof",
            "liskov",
            "application",
            "manifest",
            "validate",
            "--file",
            str(path),
            "--json",
            "--no-analytics",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return json.loads(completed.stdout), completed.returncode


if __name__ == "__main__":
    unittest.main()
