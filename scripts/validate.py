#!/usr/bin/env python3
"""Bootstrap structural checks, not policy semantics or a full YAML validator."""
from pathlib import Path
import re
import sys


def skill_errors(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return ["SKILL.md needs YAML frontmatter"]
    errors = []
    for key in ("name", "description"):
        if not re.search(rf"^{key}:\s*[^\s].*$", parts[1], re.MULTILINE):
            errors.append(f"missing {key}")
    if not parts[2].strip():
        errors.append("empty skill instructions")
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    for name in ("README.md", "AGENTS.md", "CLAUDE.md", "LICENSE",
                 "skills/liskov-policy", "evals", "tests", "docs"):
        if not (root / name).exists():
            errors.append(f"missing {name}")
    skills = sorted((root / "skills").rglob("SKILL.md"))
    for skill in skills:
        errors.extend(f"{skill.relative_to(root)}: {error}" for error in skill_errors(skill))
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Structure OK ({len(skills)} implemented skill entrypoints); semantic and agent evaluation are separate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
