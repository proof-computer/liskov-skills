# Fresh Claude Code session

Run these cases in a fresh Claude Code `2.1.283` session. The paired tool
is Codex CLI `0.157.1`. Both use this repository's `evals/` corpus and the
skill `liskov-policy` at version `0.0.0` (unreleased).

A fresh session has no prior conversation. Point Claude at a disposable
config directory, not the operator's real Claude configuration. Load this
repository with the reviewed discovery command, using the repository root
as `PATH`:

```sh
claude --plugin-dir PATH
```

Install and remove commands, when a session needs them, are in
[installation](../../docs/installation.md). Use a disposable directory and
`--scope local` for an install test. Do not publish, deploy, reserve, or
charge.

The skill instructions are
[skills/liskov-policy/SKILL.md](../../skills/liskov-policy/SKILL.md).
Give the session one case from [corpus.json](../corpus.json). The case
input is the prompt file. Open any document path it names. Do not supply
an application id, digest, price, or budget consent that the input does
not already contain.

The only drafting command is:

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

Store a transcript from this session at:

`evals/sessions/claude-code/<case-id>/transcript.md`

Store the structured result at:

`evals/sessions/claude-code/<case-id>/result.json`

The Codex transcript for the same case id would be stored at
`evals/sessions/codex/<case-id>/transcript.md`.

`result.json` fields after a real run: `status` (`ran`), `observedClass`,
`ready`, `launchApproval` (false), `validator` (the drafting-command JSON
object, or null), `draftText`, `reply`, `commands`, and `parts` for
`unavailable` (`ingress`, `interval`, `jobs-3`). Do not put a `passed`
field in the file. The offline grader decides that.

If Claude Code `2.1.283` is not installed, or this session was not run,
leave the transcript and result absent. Record `missing` in
[sessions/index.json](../sessions/index.json). A missing tool or a session
that was not run is recorded as missing, not as a pass.
Do not invent a transcript.

This packet's index already says missing. That is not release evidence.
A later packet runs the fresh session.
