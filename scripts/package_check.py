#!/usr/bin/env python3
"""Check the shared skill package. Does not install a plugin or publish a release."""
from pathlib import Path
import json
import os
import re
import sys


CLAUDE_PLUGIN = Path(".claude-plugin/plugin.json")
CODEX_PLUGIN = Path(".codex-plugin/plugin.json")
CLAUDE_MARKET = Path(".claude-plugin/marketplace.json")
CODEX_CATALOG = Path(".agents/plugins/marketplace.json")
SKIP_DIRS = {".git", "__pycache__"}
_PRIVATE_REPO = "liskov-" + "agent-" + "orchestrator"

# Machine paths and private-orchestrator URLs. A prose mention of the
# repository name is not a URL and is not flagged. Prefixes are assembled so
# this file does not contain the path or URL text it rejects.
_PATH_ROOTS = ("home", "Users", "opt", "var", "tmp", "usr", "private", "etc", "mnt", "Volumes")
_TILDE_PATH = "~" + "/"
_FILE_URL = "file:" + "//" + "/"
_ABSOLUTE_PATH = re.compile(
    r"(?:^|[\s`'\"(=])/(?:" + "|".join(_PATH_ROOTS) + r")/\S+"
    + r"|(?:^|[\s`'\"(=])" + re.escape(_TILDE_PATH) + r"\S+"
    + r"|(?:^|[\s`'\"(=])" + re.escape(_FILE_URL) + r"\S+"
    + r"|(?:^|[\s`'\"(=])[A-Za-z]:\\+\S+"
)
_ORCHESTRATOR_URL = re.compile(
    r"(?:https?://|git@|ssh://|" + "file:" + "//" + r"|git://)\S*"
    + re.escape(_PRIVATE_REPO)
    + r"\S*"
    + r"|(?:^|[\s`'\"(=])/(?:[\w.+-]+/)*"
    + re.escape(_PRIVATE_REPO)
    + r"(?:/\S*)?",
    re.IGNORECASE,
)
_LINK = re.compile(r"\[[^\]\n]*\]\(<([^>\n]+)>\)|\[[^\]\n]*\]\(([^)\s\n]+)\)")


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_paths(root):
    return (root / CLAUDE_PLUGIN, root / CODEX_PLUGIN)


def manifest_versions(root):
    """Return the Claude and Codex plugin version strings."""
    versions = []
    for path in _manifest_paths(root):
        version = _load_json(path).get("version")
        if not isinstance(version, str) or version == "":
            raise ValueError(f"{path} has no version string")
        versions.append(version)
    return tuple(versions)


def pin_release(root, tag):
    """Write one release tag string into both plugin manifests."""
    if not isinstance(tag, str) or tag == "" or tag != tag.strip():
        raise ValueError("release tag must be a non-empty string")
    for path in _manifest_paths(root):
        document = _load_json(path)
        document["version"] = tag
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _skill_roots(root):
    errors = []
    claude_root = (root / "skills").resolve()
    codex_manifest = root / CODEX_PLUGIN
    try:
        skills_field = _load_json(codex_manifest).get("skills")
    except (OSError, json.JSONDecodeError) as exc:
        return claude_root, None, [f"codex manifest: {exc}"]
    if not isinstance(skills_field, str) or not skills_field.startswith("./"):
        errors.append("codex skills path must be a relative ./ path")
        return claude_root, None, errors
    codex_root = (root / skills_field).resolve()
    if root.resolve() != codex_root and root.resolve() not in codex_root.parents:
        errors.append("codex skills path escapes the package")
        return claude_root, None, errors
    return claude_root, codex_root, errors


def _tree_bytes(directory):
    files = {}
    if directory is None or not directory.is_dir():
        return files
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        files[path.relative_to(directory).as_posix()] = path.read_bytes()
    return files


def _reference_errors(root, skill_root):
    errors = []
    if skill_root is None or not skill_root.is_dir():
        return errors
    package_root = root.resolve()
    for path in sorted(skill_root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"unreadable reference source: {path.relative_to(root)}")
            continue
        for match in _LINK.finditer(text):
            target = (match.group(1) or match.group(2) or "").strip()
            if target.startswith(("<",)):
                target = target.strip("<>")
            target = target.split("#", 1)[0].split("?", 1)[0].strip()
            if target == "" or "://" in target or target.startswith(("mailto:", "#")):
                continue
            # A character class in prose can look like a markdown link.
            # Skill file references do not contain these characters.
            if any(char in target for char in "{}[]^*"):
                continue
            resolved = (path.parent / target).resolve()
            relative = path.relative_to(root).as_posix()
            if package_root != resolved and package_root not in resolved.parents:
                errors.append(f"reference escapes the package: {relative} -> {target}")
            elif not resolved.is_file():
                errors.append(f"broken reference: {relative} -> {target}")
    return errors


def _packaged_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for name in filenames:
            if name == ".git":
                continue
            yield Path(dirpath) / name


def _content_errors(root):
    errors = []
    for path in _packaged_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(root).as_posix()
        if _ABSOLUTE_PATH.search(text):
            errors.append(f"absolute path: {relative}")
        if _ORCHESTRATOR_URL.search(text):
            errors.append(f"private orchestrator URL: {relative}")
    return errors


def check_package(root):
    """Return package errors. An empty list means the shared package checks pass."""
    root = Path(root)
    errors = []
    for relative in (CLAUDE_PLUGIN, CODEX_PLUGIN, CLAUDE_MARKET):
        if not (root / relative).is_file():
            errors.append(f"missing {relative.as_posix()}")
    if (root / CODEX_CATALOG).exists():
        errors.append("packaging must not create .agents/plugins/marketplace.json")
    if errors:
        return errors
    try:
        claude_version, codex_version = manifest_versions(root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]
    if claude_version != codex_version:
        errors.append(
            f"version mismatch: claude {claude_version} != codex {codex_version}"
        )
    claude_skills, codex_skills, skill_errors = _skill_roots(root)
    errors.extend(skill_errors)
    if codex_skills is not None and claude_skills != codex_skills:
        if _tree_bytes(claude_skills) != _tree_bytes(codex_skills):
            errors.append("divergent shared content")
    errors.extend(_reference_errors(root, claude_skills))
    if codex_skills is not None and codex_skills != claude_skills:
        errors.extend(_reference_errors(root, codex_skills))
    errors.extend(_content_errors(root))
    return errors


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = check_package(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    claude_version, _codex_version = manifest_versions(root)
    print(f"Package OK (version {claude_version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
