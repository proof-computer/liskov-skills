"""Package checks and isolated Claude/Codex install discovery."""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_check", REPO / "scripts" / "package_check.py")
package_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_check)

CLAUDE_VERSION = "2.1.283"
CODEX_VERSION = "0.157.1"
FIXTURE_SKILL = """---
name: fixture-skill
description: Temporary packaging fixture. Not a released skill.
---

Read [the note](references/note.md) before using this fixture.
"""
FIXTURE_NOTE = "fixture-reference\n"
UPDATED_NOTE = "fixture-reference-updated\n"
OPERATOR_CONFIG = (
    Path.home() / ".claude.json",
    Path.home() / ".claude" / "settings.json",
    Path.home() / ".claude" / "plugins" / "known_marketplaces.json",
    Path.home() / ".claude" / "plugins" / "installed_plugins.json",
    Path.home() / ".codex" / "config.toml",
)
INSTALL_COMMANDS = (
    "claude plugin marketplace add proof-computer/liskov-skills",
    "claude plugin install liskov-policy@liskov-skills --scope user",
    "claude plugin update liskov-policy@liskov-skills",
    "claude plugin uninstall liskov-policy@liskov-skills",
    "claude --plugin-dir PATH",
    "codex plugin marketplace add proof-computer/liskov-skills",
    "codex plugin add liskov-policy@liskov-skills",
    "codex plugin remove liskov-policy",
)


def _stage_manifests(root):
    shutil.copytree(REPO / ".claude-plugin", root / ".claude-plugin")
    shutil.copytree(REPO / ".codex-plugin", root / ".codex-plugin")
    shutil.copytree(REPO / "skills", root / "skills")
    return root


def _write_json(path, document):
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _linked_reference(skill_md):
    match = re.search(r"\[[^\]]*\]\(([^)\s]+)\)", skill_md.read_text(encoding="utf-8"))
    if match is None:
        raise AssertionError(f"no reference link in {skill_md}")
    resolved = (skill_md.parent / match.group(1)).resolve()
    if not resolved.is_file():
        raise AssertionError(f"unresolved reference {match.group(1)} from {skill_md}")
    return resolved


def _parse_json(text):
    stripped = text.strip()
    start = min((index for index in (stripped.find("{"), stripped.find("[")) if index != -1), default=-1)
    if start < 0:
        raise AssertionError(f"no JSON in {text!r}")
    return json.loads(stripped[start:])


def _run(command, cwd, env):
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )


class PackageCheckTests(unittest.TestCase):
    def test_repo_versions_match_and_pin_same_tag(self):
        self.assertEqual(package_check.manifest_versions(REPO), ("0.0.0", "0.0.0"))
        self.assertEqual(package_check.check_package(REPO), [])
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            package_check.pin_release(root, "v0.1.0")
            self.assertEqual(package_check.manifest_versions(root), ("v0.1.0", "v0.1.0"))
            self.assertEqual(package_check.check_package(root), [])
            self.assertEqual(package_check.manifest_versions(REPO), ("0.0.0", "0.0.0"))

    def test_divergent_versions_fail_until_the_same_tag_is_pinned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            codex = root / ".codex-plugin" / "plugin.json"
            document = json.loads(codex.read_text(encoding="utf-8"))
            document["version"] = "9.9.9"
            _write_json(codex, document)
            errors = package_check.check_package(root)
            self.assertTrue(any("version mismatch" in error for error in errors))
            package_check.pin_release(root, "skill-v1")
            self.assertEqual(package_check.manifest_versions(root), ("skill-v1", "skill-v1"))
            self.assertEqual(package_check.check_package(root), [])

    def test_broken_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            skill = root / "skills" / "fixture-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: fixture-skill\ndescription: Broken fixture.\n---\n\n"
                "Read [the note](references/missing.md).\n",
                encoding="utf-8",
            )
            errors = package_check.check_package(root)
            self.assertTrue(any(error.startswith("broken reference:") for error in errors))

    def test_divergent_shared_content_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            codex = root / ".codex-plugin" / "plugin.json"
            document = json.loads(codex.read_text(encoding="utf-8"))
            document["skills"] = "./codex-skills/"
            _write_json(codex, document)
            other = root / "codex-skills" / "fixture-skill"
            other.mkdir(parents=True)
            (other / "SKILL.md").write_text("different workflow\n", encoding="utf-8")
            errors = package_check.check_package(root)
            self.assertIn("divergent shared content", errors)

    def test_absolute_path_and_private_orchestrator_url_fail(self):
        private = "liskov-" + "agent-" + "orchestrator"
        machine = "/" + "home/" + "example/machine"
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            (root / "skills" / "liskov-policy" / "leak.txt").write_text(
                machine + "\n" + "https://example.invalid/" + private + ".git\n",
                encoding="utf-8",
            )
            errors = package_check.check_package(root)
            self.assertTrue(any(error.startswith("absolute path:") for error in errors))
            self.assertTrue(any(error.startswith("private orchestrator URL:") for error in errors))

    def test_codex_catalog_is_not_packaged(self):
        self.assertFalse((REPO / ".agents" / "plugins" / "marketplace.json").exists())
        with tempfile.TemporaryDirectory() as directory:
            root = _stage_manifests(Path(directory))
            catalog = root / ".agents" / "plugins"
            catalog.mkdir(parents=True)
            (catalog / "marketplace.json").write_text("{}\n", encoding="utf-8")
            errors = package_check.check_package(root)
            self.assertIn("packaging must not create .agents/plugins/marketplace.json", errors)

    def test_manifest_contract_and_install_commands(self):
        claude = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        codex = json.loads((REPO / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["name"], "liskov-policy")
        self.assertEqual(claude["author"]["name"], "PROOF Computer")
        self.assertEqual(claude["license"], "Apache-2.0")
        self.assertEqual(claude["version"], "0.0.0")
        self.assertEqual(market["name"], "liskov-skills")
        self.assertEqual(market["owner"]["name"], "PROOF Computer")
        self.assertEqual(market["plugins"], [{"name": "liskov-policy", "source": "."}])
        self.assertEqual(codex["name"], "liskov-policy")
        self.assertEqual(codex["version"], "0.0.0")
        self.assertEqual(codex["skills"], "./skills/")
        installation = (REPO / "docs" / "installation.md").read_text(encoding="utf-8")
        for command in INSTALL_COMMANDS:
            self.assertIn(command, installation)
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("skills/liskov-policy/", readme)
        self.assertIn("0.0.0", readme)
        self.assertNotIn("skill has been released", readme.lower())

    def test_package_script_accepts_the_repo(self):
        result = subprocess.run(
            ["python3", str(REPO / "scripts" / "package_check.py")],
            cwd=REPO,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Package OK (version 0.0.0)", result.stdout)


class PackageInstallTests(unittest.TestCase):
    def setUp(self):
        self._config_before = {
            path: path.read_bytes() if path.is_file() else None for path in OPERATOR_CONFIG
        }

    def tearDown(self):
        changed = []
        for path, previous in self._config_before.items():
            current = path.read_bytes() if path.is_file() else None
            if current == previous:
                continue
            changed.append(path)
            if previous is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(previous)
        if changed:
            self.fail(
                "missing: live install changed operator config and was restored: "
                + ", ".join(str(path) for path in changed)
            )

    def _require(self, command, version):
        if shutil.which(command) is None:
            self.skipTest(f"missing: {command} is not installed")
        result = _run([command, "--version"], REPO, os.environ.copy())
        if result.returncode != 0 or version not in result.stdout + result.stderr:
            self.fail(f"missing: {command} {version} is not available ({result.stdout!r} {result.stderr!r})")

    def _fixture(self, root):
        shutil.copytree(
            REPO,
            root,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )
        skill = root / "skills" / "fixture-skill"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(FIXTURE_SKILL, encoding="utf-8")
        (skill / "references" / "note.md").write_text(FIXTURE_NOTE, encoding="utf-8")
        self.assertEqual(package_check.check_package(root), [])
        catalog = root / ".agents" / "plugins"
        catalog.mkdir(parents=True)
        _write_json(catalog / "marketplace.json", {
            "name": "liskov-skills",
            "plugins": [{
                "name": "liskov-policy",
                "source": {"source": "local", "path": "./"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }],
        })
        return skill

    def test_claude_and_codex_discover_the_same_fixture_references(self):
        self._require("claude", CLAUDE_VERSION)
        self._require("codex", CODEX_VERSION)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "plugin"
            skill = self._fixture(root)
            source_skill = (skill / "SKILL.md").read_bytes()
            source_note = _linked_reference(skill / "SKILL.md").read_bytes()
            self.assertEqual(source_note, FIXTURE_NOTE.encode("utf-8"))

            claude_home = base / "claude-home"
            project = base / "project"
            claude_home.mkdir()
            (project / ".claude").mkdir(parents=True)
            _write_json(claude_home / "settings.json", {
                "theme": "keep-user",
                "preferredNotifChannel": "off",
            })
            _write_json(project / ".claude" / "settings.local.json", {
                "enabledPlugins": {"unrelated-plugin@unrelated-market": True},
            })
            claude_env = os.environ.copy()
            claude_env["CLAUDE_CONFIG_DIR"] = str(claude_home)
            claude_env.pop("CLAUDE_CODE_PLUGIN_DIRS", None)

            details = _run(
                ["claude", "--plugin-dir", str(root), "plugin", "details", "liskov-policy"],
                project,
                claude_env,
            )
            self.assertEqual(details.returncode, 0, details.stderr)
            self.assertIn("fixture-skill", details.stdout)

            added = _run(
                ["claude", "plugin", "marketplace", "add", str(root), "--scope", "local"],
                project,
                claude_env,
            )
            self.assertEqual(added.returncode, 0, added.stdout + added.stderr)
            installed = _run(
                ["claude", "plugin", "install", "liskov-policy@liskov-skills", "--scope", "local", "--json"],
                project,
                claude_env,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            listing = _run(["claude", "plugin", "list", "--json"], project, claude_env)
            self.assertEqual(listing.returncode, 0, listing.stderr)
            claude_row = next(
                item for item in _parse_json(listing.stdout)
                if item.get("id") == "liskov-policy@liskov-skills"
            )
            claude_skill = Path(claude_row["installPath"]) / "skills" / "fixture-skill" / "SKILL.md"
            self.assertEqual(claude_skill.read_bytes(), source_skill)
            self.assertEqual(_linked_reference(claude_skill).read_bytes(), source_note)

            codex_home = base / "codex-home"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text(
                'model = "unrelated-model-pin"\n'
                'notify = ["echo", "keep-me"]\n'
                '\n'
                '[projects."/keep"]\n'
                'trust_level = "untrusted"\n',
                encoding="utf-8",
            )
            codex_env = os.environ.copy()
            codex_env["CODEX_HOME"] = str(codex_home)
            market = _run(["codex", "plugin", "marketplace", "add", str(root), "--json"], project, codex_env)
            self.assertEqual(market.returncode, 0, market.stderr)
            added_plugin = _run(
                ["codex", "plugin", "add", "liskov-policy@liskov-skills", "--json"],
                project,
                codex_env,
            )
            self.assertEqual(added_plugin.returncode, 0, added_plugin.stderr)
            codex_info = _parse_json(added_plugin.stdout)
            codex_skill = Path(codex_info["installedPath"]) / "skills" / "fixture-skill" / "SKILL.md"
            self.assertEqual(codex_skill.read_bytes(), source_skill)
            self.assertEqual(_linked_reference(codex_skill).read_bytes(), source_note)
            self.assertEqual(claude_skill.read_bytes(), codex_skill.read_bytes())

            local_settings = json.loads((project / ".claude" / "settings.local.json").read_text(encoding="utf-8"))
            self.assertTrue(local_settings["enabledPlugins"]["unrelated-plugin@unrelated-market"])
            user_settings = json.loads((claude_home / "settings.json").read_text(encoding="utf-8"))
            self.assertEqual(user_settings["theme"], "keep-user")
            self.assertEqual(user_settings["preferredNotifChannel"], "off")
            codex_config = (codex_home / "config.toml").read_text(encoding="utf-8")
            self.assertIn('model = "unrelated-model-pin"', codex_config)
            self.assertIn('notify = ["echo", "keep-me"]', codex_config)
            self.assertIn('trust_level = "untrusted"', codex_config)

    def test_install_update_and_remove_preserve_unrelated_configuration(self):
        self._require("claude", CLAUDE_VERSION)
        self._require("codex", CODEX_VERSION)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "plugin"
            skill = self._fixture(root)
            claude_home = base / "claude-home"
            project = base / "project"
            claude_home.mkdir()
            (project / ".claude").mkdir(parents=True)
            _write_json(claude_home / "settings.json", {
                "theme": "keep-user",
                "preferredNotifChannel": "off",
            })
            _write_json(project / ".claude" / "settings.local.json", {
                "enabledPlugins": {"unrelated-plugin@unrelated-market": True},
            })
            claude_env = os.environ.copy()
            claude_env["CLAUDE_CONFIG_DIR"] = str(claude_home)
            claude_env.pop("CLAUDE_CODE_PLUGIN_DIRS", None)
            codex_home = base / "codex-home"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text(
                'model = "unrelated-model-pin"\n'
                'notify = ["echo", "keep-me"]\n'
                '\n'
                '[projects."/keep"]\n'
                'trust_level = "untrusted"\n',
                encoding="utf-8",
            )
            codex_env = os.environ.copy()
            codex_env["CODEX_HOME"] = str(codex_home)

            self.assertEqual(_run(
                ["claude", "plugin", "marketplace", "add", str(root), "--scope", "local"],
                project, claude_env,
            ).returncode, 0)
            self.assertEqual(_run(
                ["claude", "plugin", "install", "liskov-policy@liskov-skills", "--scope", "local", "--json"],
                project, claude_env,
            ).returncode, 0)
            self.assertEqual(_run(
                ["codex", "plugin", "marketplace", "add", str(root), "--json"],
                project, codex_env,
            ).returncode, 0)
            self.assertEqual(_run(
                ["codex", "plugin", "add", "liskov-policy@liskov-skills", "--json"],
                project, codex_env,
            ).returncode, 0)

            (skill / "references" / "note.md").write_text(UPDATED_NOTE, encoding="utf-8")
            package_check.pin_release(root, "0.0.1")
            updated = _run(
                ["claude", "plugin", "update", "liskov-policy@liskov-skills", "--scope", "local", "--json"],
                project, claude_env,
            )
            self.assertEqual(updated.returncode, 0, updated.stdout + updated.stderr)
            self.assertEqual(_parse_json(updated.stdout).get("newVersion"), "0.0.1")
            codex_updated = _run(
                ["codex", "plugin", "add", "liskov-policy@liskov-skills", "--json"],
                project, codex_env,
            )
            self.assertEqual(codex_updated.returncode, 0, codex_updated.stderr)
            self.assertEqual(_parse_json(codex_updated.stdout).get("version"), "0.0.1")

            listing = _run(["claude", "plugin", "list", "--json"], project, claude_env)
            claude_row = next(
                item for item in _parse_json(listing.stdout)
                if item.get("id") == "liskov-policy@liskov-skills"
            )
            claude_note = _linked_reference(
                Path(claude_row["installPath"]) / "skills" / "fixture-skill" / "SKILL.md"
            )
            codex_note = _linked_reference(
                Path(_parse_json(codex_updated.stdout)["installedPath"]) / "skills" / "fixture-skill" / "SKILL.md"
            )
            self.assertEqual(claude_note.read_text(encoding="utf-8"), UPDATED_NOTE)
            self.assertEqual(codex_note.read_text(encoding="utf-8"), UPDATED_NOTE)

            removed = _run(
                ["claude", "plugin", "uninstall", "liskov-policy@liskov-skills", "--scope", "local", "--json"],
                project, claude_env,
            )
            self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
            # Codex 0.157.1 rejects the bare plugin name documented for operators.
            codex_removed = _run(
                ["codex", "plugin", "remove", "liskov-policy@liskov-skills", "--json"],
                project, codex_env,
            )
            self.assertEqual(codex_removed.returncode, 0, codex_removed.stderr)

            local_settings = json.loads((project / ".claude" / "settings.local.json").read_text(encoding="utf-8"))
            self.assertTrue(local_settings["enabledPlugins"]["unrelated-plugin@unrelated-market"])
            self.assertNotIn("liskov-policy@liskov-skills", local_settings["enabledPlugins"])
            user_settings = json.loads((claude_home / "settings.json").read_text(encoding="utf-8"))
            self.assertEqual(user_settings["theme"], "keep-user")
            self.assertEqual(user_settings["preferredNotifChannel"], "off")
            codex_config = (codex_home / "config.toml").read_text(encoding="utf-8")
            self.assertIn('model = "unrelated-model-pin"', codex_config)
            self.assertIn('notify = ["echo", "keep-me"]', codex_config)
            self.assertIn('[projects."/keep"]', codex_config)
            self.assertIn('trust_level = "untrusted"', codex_config)
            self.assertNotIn("liskov-policy@liskov-skills", codex_config)
            self.assertFalse((REPO / ".claude" / "settings.local.json").exists())
