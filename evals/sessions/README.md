# Session store

Transcripts from a fresh Claude Code `2.1.283` session and a fresh Codex
CLI `0.157.1` session are stored here. The skill under test is
`liskov-policy` `0.0.0` (unreleased).

| Tool id | Transcript | Result |
| --- | --- | --- |
| `claude-code` | `evals/sessions/claude-code/<case-id>/transcript.md` | `evals/sessions/claude-code/<case-id>/result.json` |
| `codex` | `evals/sessions/codex/<case-id>/transcript.md` | `evals/sessions/codex/<case-id>/result.json` |

[index.json](index.json) is the record of which sessions ran. `missing`
means the tool was not available or the session was not run. Missing is
not a pass. Do not invent a transcript. Do not add `transcript.md` or
`result.json` until that fresh session has produced them.

Offline CI does not run these sessions. A later release packet does.
