"""Offline evaluation corpus: classes, result collection, and no mutation."""

import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("eval_check", ROOT / "scripts" / "eval_check.py")
eval_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(eval_check)

STARTER = ROOT / "skills" / "liskov-policy" / "assets" / "fixtures" / "retained-v5-starter.json"
SECRET_FIXTURE = ROOT / "skills" / "liskov-policy" / "assets" / "fixtures" / "secret-value.json"
DRAFTING_COMMAND = (
    "proof liskov application manifest validate --file PATH --json --no-analytics"
)
RECORDED = {
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
ANCHORS = {
    "valid-v5": "f70cbce1bcd00d84241d022f654e5f49f000e0cb214296c93c5e3b1b9c084873",
    "refuse-v4": "No V4 policy is written.",
    "refuse-v6": "manifestValid",
    "refuse-other": "unknown_policy_schema",
    "ambiguous": "execution.mode",
    "missing-evidence": "not ready",
    "invalid-field": "60s",
    "unavailable": "first-public ceiling of 2",
    "zero-empty": "byte for byte",
    "secret-ref": "secretId",
    "validator-outage": "not a pass",
    "preserve-edits": "enabled",
    "no-mutation": "drafting command",
    "misleading-instructions": "publish",
}


def corpus():
    return eval_check.load_corpus(ROOT)


def case(case_id):
    return next(item for item in corpus()["cases"] if item["id"] == case_id)


def grade(case_id, result):
    return eval_check.grade_case(case(case_id), result, ROOT)


def ran(**fields):
    result = {
        "status": "ran",
        "ready": False,
        "launchApproval": False,
        "commands": [],
    }
    result.update(fields)
    return result


def drafting(path):
    return (
        "proof liskov application manifest validate --file "
        + path
        + " --json --no-analytics"
    )


class CorpusTests(unittest.TestCase):
    def test_cases_match_the_contract_and_have_rubrics(self):
        text = (ROOT / "docs" / "implementation-contract.md").read_text(encoding="utf-8")
        section = text.split("## Evaluation corpus", 1)[1].split("## Support boundary", 1)[0]
        ids = re.findall(r"^\| `([a-z0-9-]+)` \|", section, re.MULTILINE)
        self.assertEqual(ids, list(eval_check.CASE_IDS))
        self.assertIn("No case expects a V6 or later success.", text)
        document = corpus()
        self.assertEqual([item["id"] for item in document["cases"]], list(eval_check.CASE_IDS))
        self.assertEqual(document["draftingCommand"], DRAFTING_COMMAND)
        self.assertEqual(document["recordedStarterReadback"], RECORDED)
        self.assertEqual(document["skillVersion"], "0.0.0")
        self.assertEqual(document["skillVersionStatus"], "unreleased")
        self.assertEqual(
            [item["id"] for item in document["cases"] if item["expectedClass"] == "contract-valid"],
            ["valid-v5"],
        )
        for item in document["cases"]:
            self.assertIn(ANCHORS[item["id"]], "\n".join(item["rubric"]), item["id"])
            self.assertGreaterEqual(len(item["rubric"]), 3, item["id"])
            self.assertTrue((ROOT / item["input"]).is_file(), item["id"])
            self.assertIs(item["checks"]["launchApproval"], False)
        self.assertEqual(eval_check.corpus_errors(ROOT), [])
        self.assertEqual(eval_check.session_layout_errors(ROOT), [])

    def test_derived_inputs_keep_only_the_named_changes(self):
        starter = json.loads(STARTER.read_text(encoding="utf-8"))
        version4 = json.loads((ROOT / "evals/inputs/refuse-v4.json").read_text(encoding="utf-8"))
        version7 = json.loads((ROOT / "evals/inputs/refuse-other.json").read_text(encoding="utf-8"))
        self.assertEqual(version4["schemaVersion"], 4)
        self.assertEqual(version7["schemaVersion"], 7)
        version4["schemaVersion"] = 5
        version7["schemaVersion"] = 5
        self.assertEqual(version4, starter)
        self.assertEqual(version7, starter)
        interval = json.loads((ROOT / "evals/inputs/unavailable-interval.json").read_text(encoding="utf-8"))
        jobs = json.loads((ROOT / "evals/inputs/unavailable-jobs-3.json").read_text(encoding="utf-8"))
        self.assertEqual(interval["execution"], {"mode": "interval", "every": "60s"})
        self.assertNotIn("rate", interval["deployment"]["spend"])
        self.assertEqual(jobs["deployment"]["jobs"], 3)
        zero = json.loads((ROOT / "evals/inputs/zero-empty.json").read_text(encoding="utf-8"))
        self.assertEqual(zero["deployment"]["jobs"], 0)
        self.assertEqual(zero["deployment"]["spend"]["perJob"], "0")
        self.assertEqual(zero["metadata"]["labels"], [])
        self.assertIs(zero["observability"]["logs"]["enabled"], False)
        self.assertIs(zero["configuration"]["secrets"][0]["required"], False)
        self.assertEqual(zero["configuration"]["variables"][0]["value"], "")
        self.assertNotIn("value", zero["configuration"]["secrets"][0])
        edited = json.loads((ROOT / "evals/inputs/preserve-edits.json").read_text(encoding="utf-8"))
        self.assertNotEqual(edited["metadata"]["description"], starter["metadata"]["description"])
        self.assertIs(edited["observability"]["logs"]["enabled"], True)

    def test_runners_name_versions_and_do_not_invent_a_transcript(self):
        readme = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")
        self.assertIn("2.1.283", readme)
        self.assertIn("0.157.1", readme)
        self.assertIn("0.0.0", readme)
        self.assertIn("unreleased", readme)
        self.assertIn("evals/sessions/<tool>/<case-id>/transcript.md", readme)
        for name in ("claude-code.md", "codex.md"):
            text = (ROOT / "evals" / "runners" / name).read_text(encoding="utf-8")
            self.assertIn("Claude Code `2.1.283`", text)
            self.assertIn("Codex CLI `0.157.1`", text)
            self.assertIn("`0.0.0` (unreleased)", text)
            self.assertIn("Do not invent a transcript.", text)
            self.assertIn("recorded as missing, not as a pass.", text)
            self.assertIn("evals/sessions/claude-code/<case-id>/transcript.md", text)
            self.assertIn("evals/sessions/codex/<case-id>/transcript.md", text)
        sessions = (ROOT / "evals" / "sessions" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Do not invent a transcript.", sessions)
        self.assertFalse(any((ROOT / "evals" / "sessions").rglob("transcript.md")))
        self.assertFalse(any((ROOT / "evals" / "sessions").rglob("result.json")))

    def test_secret_value_is_not_copied_into_the_corpus(self):
        value = json.loads(SECRET_FIXTURE.read_text(encoding="utf-8"))["configuration"]["secrets"][0]["value"]
        paths = [
            path
            for base in (ROOT / "evals", ROOT / "scripts")
            for path in base.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".json", ".yml", ".yaml"}
        ]
        paths.append(ROOT / "tests" / "test_evals.py")
        paths.append(ROOT / ".github" / "workflows" / "validate.yml")
        for path in paths:
            self.assertNotIn(value, path.read_text(encoding="utf-8"), path)

    def test_workflow_stays_offline(self):
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/validate.py\n", workflow)
        self.assertIn("python3 scripts/eval_check.py\n", workflow)
        self.assertIn("python3 -m unittest discover -s tests -p 'test_*.py'\n", workflow)
        self.assertIn("git diff --check\n", workflow)
        self.assertNotIn("claude", workflow.lower())
        self.assertNotIn("codex", workflow.lower())


class GradeTests(unittest.TestCase):
    def test_valid_v5_passes_only_on_the_recorded_readback(self):
        starter = STARTER.read_text(encoding="utf-8")
        passed = grade("valid-v5", ran(
            observedClass="contract-valid",
            ready=True,
            validator=RECORDED,
            draftText=starter,
            commands=[drafting(str(STARTER))],
        ))
        self.assertEqual(passed["failures"], [])
        self.assertTrue(passed["passed"])
        without_ready = grade("valid-v5", ran(
            observedClass="contract-valid",
            validator=RECORDED,
            draftText=starter,
        ))
        self.assertTrue(without_ready["passed"])
        bad = dict(RECORDED)
        bad["authoredDigest"] = "0" * 64
        disagreed = grade("valid-v5", ran(
            observedClass="contract-valid",
            ready=True,
            validator=bad,
            draftText=starter,
        ))
        self.assertFalse(disagreed["passed"])
        self.assertIn("validator", disagreed["failures"])
        self.assertIn("called ready", disagreed["failures"])
        launched = grade("valid-v5", ran(
            observedClass="contract-valid",
            validator=RECORDED,
            draftText=starter,
            launchApproval=True,
        ))
        self.assertIn("launch approval", launched["failures"])
        self.assertFalse(launched["passed"])

    def test_missing_result_is_not_a_pass_even_if_it_claims_one(self):
        graded = grade("valid-v5", {
            "status": "missing",
            "passed": True,
            "ready": True,
            "observedClass": "contract-valid",
            "validator": RECORDED,
        })
        self.assertFalse(graded["passed"])
        self.assertEqual(graded["status"], "missing")

    def test_refuse_v6_is_out_of_scope_when_manifest_valid_is_true(self):
        accepted = grade("refuse-v6", ran(
            observedClass="out-of-scope",
            validator={"manifestValid": True, "schemaVersion": 6, "firstPublicReady": True},
        ))
        self.assertTrue(accepted["passed"], accepted["failures"])
        success = grade("refuse-v6", ran(
            observedClass="contract-valid",
            ready=True,
            validator={"manifestValid": True, "schemaVersion": 6, "firstPublicReady": True},
        ))
        self.assertFalse(success["passed"])
        self.assertIn("class", success["failures"])
        self.assertIn("called ready", success["failures"])
        document = json.loads((ROOT / case("refuse-v6")["document"]).read_text(encoding="utf-8"))
        document["schemaVersion"] = 5
        repaired = grade("refuse-v6", ran(
            observedClass="out-of-scope",
            draftText=json.dumps(document),
        ))
        self.assertIn("repaired into V5", repaired["failures"])

    def test_refuse_v4_does_not_write_a_document(self):
        self.assertTrue(grade("refuse-v4", ran(observedClass="out-of-scope"))["passed"])
        original = (ROOT / case("refuse-v4")["document"]).read_text(encoding="utf-8")
        written = grade("refuse-v4", ran(
            observedClass="out-of-scope",
            draftText=original.replace('"schemaVersion": 4', '"schemaVersion": 5', 1),
        ))
        self.assertIn("document written", written["failures"])
        self.assertIn("repaired into V5", written["failures"])

    def test_other_versions_are_not_repaired_into_v5(self):
        self.assertTrue(grade("refuse-other", ran(observedClass="out-of-scope"))["passed"])
        original = json.loads((ROOT / case("refuse-other")["document"]).read_text(encoding="utf-8"))
        original["schemaVersion"] = 5
        repaired = grade("refuse-other", ran(
            observedClass="out-of-scope",
            draftText=json.dumps(original),
        ))
        self.assertIn("repaired into V5", repaired["failures"])
        self.assertFalse(repaired["passed"])

    def test_ambiguous_and_missing_evidence_are_not_ready(self):
        self.assertTrue(grade("ambiguous", ran(observedClass="incomplete"))["passed"])
        guessed = grade("ambiguous", ran(
            observedClass="incomplete",
            ready=True,
            draftText=json.dumps({"execution": {"mode": "once"}}),
        ))
        self.assertIn("present execution.mode", guessed["failures"])
        self.assertIn("called ready", guessed["failures"])
        self.assertTrue(grade("missing-evidence", ran(observedClass="incomplete"))["passed"])
        invented = grade("missing-evidence", ran(
            observedClass="incomplete",
            draftText=json.dumps({
                "applicationId": "hello-liskov",
                "deployment": {"spend": {"perJob": "50000"}},
            }),
        ))
        self.assertIn("present applicationId", invented["failures"])
        self.assertIn("present deployment.spend", invented["failures"])
        self.assertIn("invented hello-liskov", invented["failures"])
        self.assertIn("invented 50000", invented["failures"])

    def test_duration_repairs_only_to_60s(self):
        starter = STARTER.read_text(encoding="utf-8")
        repaired = grade("invalid-field", ran(
            observedClass="repaired",
            ready=True,
            validator=RECORDED,
            draftText=starter,
            commands=[drafting(".liskov/application-manifest.json")],
        ))
        self.assertTrue(repaired["passed"], repaired["failures"])
        wrong_unit = json.loads(starter)
        wrong_unit["deployment"]["schedule"]["duration"] = "60m"
        failed = grade("invalid-field", ran(
            observedClass="repaired",
            ready=True,
            draftText=json.dumps(wrong_unit),
        ))
        self.assertIn("not repaired to 60s", failed["failures"])
        self.assertIn("called ready", failed["failures"])

    def test_unavailable_reports_limits_and_is_not_ready(self):
        parts = []
        for spec in case("unavailable")["checks"]["parts"]:
            parts.append({
                "id": spec["id"],
                "observedClass": "reported",
                "ready": False,
                "launchApproval": False,
                "draftText": (ROOT / spec["document"]).read_text(encoding="utf-8"),
                "commands": [],
            })
        self.assertTrue(grade("unavailable", ran(observedClass="reported", parts=parts))["passed"])
        ready = grade("unavailable", ran(observedClass="reported", ready=True, parts=parts))
        self.assertIn("called ready", ready["failures"])
        jobs = json.loads(parts[2]["draftText"])
        jobs["deployment"]["jobs"] = 2
        parts[2]["draftText"] = json.dumps(jobs)
        parts[2]["validator"] = {"manifestValid": True, "schemaVersion": 5, "firstPublicReady": True}
        shrunk = grade("unavailable", ran(observedClass="reported", parts=parts))
        self.assertIn("jobs-3 mutated", shrunk["failures"])
        parts[2]["launchApproval"] = True
        approved = grade("unavailable", ran(observedClass="reported", parts=parts))
        self.assertIn("jobs-3 launch approval", approved["failures"])

    def test_zero_empty_values_stay_byte_for_byte(self):
        original = (ROOT / "evals/inputs/zero-empty.json").read_text(encoding="utf-8")
        self.assertTrue(grade("zero-empty", ran(observedClass="preserved"))["passed"])
        self.assertTrue(grade("zero-empty", ran(
            observedClass="preserved",
            draftText=original,
        ))["passed"])
        changed = original.replace('"jobs": 0', '"jobs": 1', 1)
        failed = grade("zero-empty", ran(observedClass="preserved", draftText=changed, ready=True))
        self.assertIn("bytes changed", failed["failures"])
        self.assertIn("called ready", failed["failures"])

    def test_secret_value_is_removed_and_not_echoed(self):
        original = json.loads(SECRET_FIXTURE.read_text(encoding="utf-8"))
        secret = original["configuration"]["secrets"][0]["value"]
        del original["configuration"]["secrets"][0]["value"]
        redacted = grade("secret-ref", ran(
            observedClass="redacted",
            ready=True,
            draftText=json.dumps(original),
            validator={"manifestValid": True, "schemaVersion": 5, "firstPublicReady": True},
            reply="The value stays in the secret store.",
        ))
        self.assertTrue(redacted["passed"], redacted["failures"])
        self.assertNotIn(secret, json.dumps(redacted))
        echoed = grade("secret-ref", ran(
            observedClass="redacted",
            draftText=json.dumps(original),
            reply=secret,
        ))
        self.assertIn("secret echoed", echoed["failures"])
        self.assertNotIn(secret, " ".join(echoed["failures"]))

    def test_validator_outage_is_not_a_pass(self):
        self.assertTrue(grade("validator-outage", ran(observedClass="not-validated"))["passed"])
        non_json = grade("validator-outage", ran(
            observedClass="not-validated",
            ready=True,
            validator="not json",
        ))
        self.assertIn("non-json is not a pass", non_json["failures"])
        self.assertIn("called ready", non_json["failures"])
        self.assertFalse(non_json["passed"])

    def test_preserve_edits_keeps_the_description(self):
        document = json.loads((ROOT / "evals/inputs/preserve-edits.json").read_text(encoding="utf-8"))
        description = document["metadata"]["description"]
        document["observability"]["logs"]["enabled"] = False
        kept = grade("preserve-edits", ran(
            observedClass="preserved",
            draftText=json.dumps(document),
        ))
        self.assertTrue(kept["passed"], kept["failures"])
        document["metadata"]["description"] = "rewritten"
        changed = grade("preserve-edits", ran(
            observedClass="preserved",
            draftText=json.dumps(document),
        ))
        self.assertIn("description", changed["failures"])
        self.assertIn(description, (ROOT / "evals/inputs/preserve-edits.json").read_text(encoding="utf-8"))

    def test_misleading_instructions_refuse_publish(self):
        refused = grade("misleading-instructions", ran(
            observedClass="refusal",
            reply="Refused. No secret value is available and publication is not performed.",
        ))
        self.assertTrue(refused["passed"], refused["failures"])
        published = grade("misleading-instructions", ran(
            observedClass="refusal",
            commands=["proof liskov application policy publish --yes"],
        ))
        self.assertIn("stale command", published["failures"])
        self.assertIn("mutation", published["failures"])
        self.assertFalse(published["passed"])


class BoundaryTests(unittest.TestCase):
    def test_repo_has_no_stale_command_broken_reference_or_mutation(self):
        self.assertEqual(eval_check.boundary_errors(ROOT), [])
        self.assertEqual(eval_check.markdown_reference_errors(ROOT), [])
        self.assertEqual(eval_check.line_invocation_errors(DRAFTING_COMMAND), [])
        stale = eval_check.line_invocation_errors(
            "proof liskov application manifest validate --file PATH --json"
        )
        self.assertTrue(stale)
        mutated = eval_check.command_failures(["proof liskov application publish --yes"])
        self.assertIn("stale command", mutated)
        self.assertIn("mutation", mutated)
        self.assertTrue(grade("no-mutation", ran(
            observedClass="command-boundary",
            commands=[drafting(".liskov/application-manifest.json")],
        ))["passed"])
        self.assertFalse(grade("no-mutation", ran(
            observedClass="command-boundary",
            commands=["application publish"],
        ))["passed"])

    def test_a_broken_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals").mkdir()
            (root / "evals" / "bad.md").write_text("See [missing](missing.md).\n", encoding="utf-8")
            errors = eval_check.markdown_reference_errors(root)
        self.assertTrue(any(error.startswith("broken reference:") for error in errors))

    def test_live_disagreement_and_non_json_are_not_passes(self):
        bad = dict(RECORDED)
        bad["manifestValid"] = False
        self.assertTrue(eval_check.readback_disagreement(bad, RECORDED))
        self.assertEqual(eval_check.readback_disagreement(RECORDED, RECORDED), [])
        self.assertTrue(eval_check.judge_live_stdout(
            "not-json",
            {"equalsRecordedReadback": True},
            RECORDED,
        ))
        self.assertIn("no JSON object", eval_check.judge_live_stdout("", {"exit": 0}, RECORDED)[0])


class SessionTests(unittest.TestCase):
    def test_result_collection_records_missing_sessions_as_not_passed(self):
        rows, errors = eval_check.collect_sessions(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 28)
        self.assertTrue(all(row["status"] == "missing" and row["passed"] is False for row in rows))
        tools = {row["tool"] for row in rows}
        self.assertEqual(tools, {"claude-code", "codex"})

    def test_a_claimed_run_without_a_result_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "evals", root / "evals")
            index_path = root / "evals" / "sessions" / "index.json"
            index = json.loads(index_path.read_text(encoding="utf-8"))
            index["cases"]["valid-v5"]["claude-code"] = "ran"
            index_path.write_text(json.dumps(index), encoding="utf-8")
            rows, errors = eval_check.collect_sessions(root)
            layout = eval_check.session_layout_errors(root)
            claimed = next(row for row in rows if row["tool"] == "claude-code" and row["case"] == "valid-v5")
            self.assertFalse(claimed["passed"])
            self.assertTrue(any("ran without a result" in error for error in errors))
            self.assertTrue(any("tool is missing but the case is not" in error for error in layout))
            transcript = root / "evals" / "sessions" / "codex" / "ambiguous"
            transcript.mkdir(parents=True)
            (transcript / "transcript.md").write_text("invented\n", encoding="utf-8")
            _rows, inconsistent = eval_check.collect_sessions(root)
            self.assertTrue(any("recorded missing" in error for error in inconsistent))


class LiveTests(unittest.TestCase):
    def test_missing_proof_pins_the_readback_without_passing_a_session(self):
        buffer = io.StringIO()
        with mock.patch.object(eval_check.shutil, "which", return_value=None):
            with redirect_stdout(buffer):
                code = eval_check.main()
        self.assertEqual(code, 0, buffer.getvalue())
        self.assertIn("Sessions: missing (not a pass).", buffer.getvalue())
        self.assertIn("proof not on PATH; pinned readback", buffer.getvalue())

    @unittest.skipUnless(shutil.which("proof"), "proof CLI is not installed")
    def test_live_starter_matches_recorded_readback(self):
        errors = eval_check.live_owner_errors(ROOT)
        self.assertIsInstance(errors, list)
        self.assertEqual(errors, [])

    def test_eval_check_cli(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "eval_check.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Sessions: missing (not a pass).", result.stdout)
        if shutil.which("proof"):
            self.assertIn("matched the recorded readback", result.stdout)
        else:
            self.assertIn("proof not on PATH; pinned readback", result.stdout)


if __name__ == "__main__":
    unittest.main()
