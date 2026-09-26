#!/usr/bin/env python3
"""Run the one local V5 manifest drafting command.

Accepts only ``--file PATH``. Any other argument is refused and is not
executed. This process does not publish, import, create, or explain, and it
does not judge the manifest itself.
"""

from __future__ import annotations

import shutil
import subprocess
import sys

DRAFTING_COMMAND = (
    "proof liskov application manifest validate --file PATH --json --no-analytics"
)


def refuse() -> int:
    print(
        f"refused: the only drafting command is {DRAFTING_COMMAND}",
        file=sys.stderr,
    )
    return 2


def command_for(path: str) -> list[str]:
    if path == "" or path.startswith("-") or "\x00" in path or "\n" in path:
        raise ValueError(path)
    command = [
        "proof",
        "liskov",
        "application",
        "manifest",
        "validate",
        "--file",
        path,
        "--json",
        "--no-analytics",
    ]
    if command[:6] != [
        "proof",
        "liskov",
        "application",
        "manifest",
        "validate",
        "--file",
    ]:
        raise ValueError(path)
    if command[6] != path or command[7:] != ["--json", "--no-analytics"]:
        raise ValueError(path)
    return command


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] != "--file":
        return refuse()
    try:
        command = command_for(args[1])
    except ValueError:
        return refuse()
    proof = shutil.which("proof")
    if proof is None:
        print("owner validator did not run: proof is not on PATH", file=sys.stderr)
        return 127
    command[0] = proof
    completed = subprocess.run(command, check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
