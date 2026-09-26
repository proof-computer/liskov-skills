# Evaluations

Shared corpus for `liskov-policy`. Offline checks load this directory.
They do not run Claude Code or Codex, and they do not invent a transcript.

Skill version `0.0.0` (unreleased). The same cases are for:

- Claude Code `2.1.283`
- Codex CLI `0.157.1`

No fresh session has been run. [Session index](sessions/index.json) records
every case as `missing`. Missing is not a pass.

| Path | What it is |
| --- | --- |
| [corpus.json](corpus.json) | Case id, input, expected class, rubric |
| [inputs/](inputs/valid-v5.md) | Prompts and documents the session would see |
| [runners/claude-code.md](runners/claude-code.md) | Fresh Claude Code session |
| [runners/codex.md](runners/codex.md) | Fresh Codex session |
| [sessions/](sessions/README.md) | Where a real transcript would be stored |

A transcript belongs at
`evals/sessions/<tool>/<case-id>/transcript.md` only after that session
ran. `<tool>` is `claude-code` or `codex`. The structured result, when a
session ran, would be `evals/sessions/<tool>/<case-id>/result.json`.
Do not add either file for a session that was not run.

Case ids, in contract order: `valid-v5`, `refuse-v4`, `refuse-v6`,
`refuse-other`, `ambiguous`, `missing-evidence`, `invalid-field`,
`unavailable`, `zero-empty`, `secret-ref`, `validator-outage`,
`preserve-edits`, `no-mutation`, `misleading-instructions`.

There is no positive later-version success case. `schemaVersion` other
than 5 is out of scope. Invalid or incomplete outputs are not ready.
`firstPublicReady` is not launch approval.

The skill source is [skills/liskov-policy/SKILL.md](../skills/liskov-policy/SKILL.md).
The authoring rules are the
[implementation contract](../docs/implementation-contract.md).
