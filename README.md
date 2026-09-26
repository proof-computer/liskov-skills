# Liskov skills

Shared agent skills for Liskov V5+ applications, maintained by PROOF Computer.
One source serves Claude Code and Codex. Skills are organized by user task.

**Status: release `1.0.0`, git tag `v1.0.0`.** The shared source is
`skills/liskov-policy/`. Both plugin manifests carry version `1.0.0`. That
version is the skill release, not a policy schema version. V4 authoring and
migration are outside the scope. Install, removal, and downgrade steps are in
[docs/installation.md](docs/installation.md).

## Layout

- `skills/liskov-policy/`: canonical skill instructions, references and assets.
- `evals/`: one evaluation corpus exercised in both supported agents.
- `tests/`: deterministic repository and skill checks.
- `docs/`: authoring contract and installation for release `1.0.0`.
- `.claude-plugin/` and `.codex-plugin/`: thin tool manifests. They do not
  fork `skills/liskov-policy/`.
- `scripts/validate.py`: structural validation shared by CI and the Gas City gate.

Keep agent-specific installation metadata small. Do not maintain separate Claude
and Codex copies of the policy workflow. Keep references within the installed
skill directory. Add executable helpers only where they add deterministic value.

## Development

Python 3.12 or newer, standard library only for the scaffold:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

The current checks validate the scaffold and basic skill structure. They do not
prove policy semantics or agent behavior; implementation must add owner-backed
validation and evaluations before release. See [AGENTS.md](AGENTS.md).

## Compatibility and releases

Start with V5; add later schema pairs only with supported contracts and release
evidence. The skill's semantic release version is independent of policy schema
versions. One tagged release serves both agents, with separate installation
instructions and evaluations against the same fixtures. No release/tag workflow
is configured yet. Policy validation and execution authority remain with Liskov
and the supported `proof liskov` CLI.

The public package must work without access to a private orchestration repository.

## License

[Apache License 2.0](LICENSE).
