# Working on Liskov skills

This public repository owns customer-facing agent skills for Liskov V5+.
Read README.md first. Keep implementation and examples usable without private
repositories, machine-local paths, credentials or internal operator commands.

## Design

- Maintain one skill source per user task. The first is
  `skills/liskov-policy/SKILL.md`; it is intentionally absent until implemented.
- Keep shared instructions, references and assets in that skill's directory.
  Tool-specific metadata and packaging must not fork the workflow.
- V5 and later supported versions only. Select an exact schema pair, preserve
  released contracts and distinguish validation from publication/execution.
- Consume the supported Liskov CLI and authoritative validators. Do not copy a
  private schema or implement a competing policy compiler here.
- Drafting must not publish, deploy or spend. Use secret references, not values.
- A release must pass the same evaluation cases in Claude Code and Codex.
  Missing live-agent evidence is a release limitation, never a passing result.

## Changes and validation

Use a dedicated worktree under `.worktrees/<name>` on `agent/<name>`; never
stage another session's work in a shared clone. One coherent change per pull
request. Read the scoped work item supplied by the orchestrator when present.

Run all of these on the final tree before pushing:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Extend those checks as implementation adds capabilities. Keep CI and the
repository-owned validation commands in sync. The scaffold gate is not a claim
that policy semantics or both agents have been evaluated.

Main is protected by the `validate` check and pull requests. Push the agent
branch, open a pull request and arm auto-merge; use a bounded script to wait for
CI rather than an agent polling loop. Publication of tags/releases is a separate
release action; a merge alone does not announce skill availability.
