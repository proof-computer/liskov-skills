# Liskov skills

Shared agent skills for Liskov V5+ applications, maintained by PROOF Computer.
One source serves Claude Code and Codex. Skills are organized by user task.

**Status: release `1.0.0`, git tag `v1.0.0`.** That tag is the released
`skills/liskov-policy/` skill. Both plugin manifests carry version `1.0.0`.
That version is the skill release, not a policy schema version. V4 authoring
and migration are outside the scope. Install, removal, and downgrade steps
for the tagged release are in [docs/installation.md](docs/installation.md).

The plugin loads every directory under `skills/`. This working tree also
contains the task skills below. They are not part of tag `v1.0.0`. None of
them has a recorded live Claude Code or Codex evaluation. A missing live run
is not a pass, and this tree is not a new release.

| Skill | Task | Boundary |
| --- | --- | --- |
| `liskov-policy` | Draft a local V5 manifest | Does not publish, deploy, reserve, or charge |
| `liskov-workload` | Decide whether the program fits the fleet | Does not write a manifest |
| `liskov-runtime` | Write the JavaScript job | Does not write the manifest or publish |
| `liskov-release` | Write the GitHub pin and attest workflow | No spend credential; does not publish or bind |
| `liskov-configure` | Edit local variables, secret references, logs, schedule, and caps | Does not publish; secret values stay in the Console |
| `liskov-bind` | Create the Application and set the source binding | Does not publish or spend |
| `liskov-publish` | Publish one retained V5 policy | Only after an explicit yes; does not repair the file |
| `liskov-operate` | Status, logs, pause, resume, retire, one retry | Does not spend on its own; pause does not stop the current job |
| `liskov-proof` | Read the evidence from commit to job | Read only |
| `liskov-spend` | Read credits, reserves, and charges | Read only; a reserve is not a cost |
| `liskov-diagnose` | One symptom to one next action | Does not invent a retry |
| `liskov-listing` | Cite a curated listing and compare bytes after a human launch | No launch command; Marketplace launch is release-gated |
| `liskov-access` | Managed Runtime SSH | Preview; register a key before the first launch |
| `liskov-fleet` | Read Applications in one organization | No bulk mutation |

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
