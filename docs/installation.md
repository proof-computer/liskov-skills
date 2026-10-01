# Installation

Release `1.0.0` is git tag `v1.0.0`. PROOF Computer maintains the repository
and this release. The tagged source for that release is `skills/liskov-policy/`.
Claude Code and Codex both use that directory. Packaging does not copy the
workflow into a second tree. The skill release version is not a policy schema
version.

The plugin's skill path is `skills/`. A checkout of tag `v1.0.0` contains
`liskov-policy` only. A checkout of a later commit on the default branch also
loads every other task skill present in that commit. Those skills are not part
of tag `v1.0.0` until a later tag says so. `--ref v1.0.0` below selects the
tagged release.

## Prerequisites

- `proof liskov` from `@proof-computer/proof-cli-liskov` `0.16.0`
- Claude Code `2.1.283`
- Codex CLI `0.157.1`

The skill supports only `proof.liskov.application-manifest` version `5`.
Writing a local draft is not publication and not spend. Install is this public
git repository plus the commands below. It does not use the private
liskov-agent-orchestrator repository, an absolute machine path, or a copied
schema compiler. The released `proof liskov` command remains the validator.

## Marketplace source

`.claude-plugin/marketplace.json` sets the single plugin `source` to `.`,
the marketplace root. `claude plugin validate --strict` on Claude Code
`2.1.283` accepts that spelling. The marketplace `description` is set because
that same strict check warns when the field is absent. The marketplace
reference lists `description`. No other field was added to satisfy the check.

Codex CLI `0.157.1` adds this repository with
`codex plugin marketplace add proof-computer/liskov-skills` and installs
`liskov-policy@liskov-skills` without a `.agents/plugins/marketplace.json`
file. That catalog is not part of this release.

## Claude Code

```sh
claude plugin marketplace add proof-computer/liskov-skills
claude plugin install liskov-policy@liskov-skills --scope user
claude plugin update liskov-policy@liskov-skills
claude plugin uninstall liskov-policy@liskov-skills
claude --plugin-dir PATH
```

`--scope user` is the documented default. `PATH` stands for a plugin directory
passed to one session. It is not a machine path checked into this repository.

## Codex CLI

```sh
codex plugin marketplace add proof-computer/liskov-skills --ref v1.0.0
codex plugin add liskov-policy@liskov-skills
codex plugin remove liskov-policy@liskov-skills
```

On Codex CLI `0.157.1`, the bare `codex plugin remove liskov-policy` command
is rejected with `plugin requires --marketplace unless passed as
<plugin>@<marketplace>`. Use the qualified form above.

`codex plugin marketplace add proof-computer/liskov-skills` was checked
against `main` before this tag. `--ref v1.0.0` selects this release after
the tag exists. A later commit on `main` does not move a checkout pinned to
the tag.

## Removal and a broken release

Remove the plugin with the uninstall command for the tool you installed.
That removes this skill only. It does not delete an unrelated marketplace,
an unrelated plugin, or your editor settings outside this plugin's own entry.

```sh
claude plugin uninstall liskov-policy@liskov-skills
codex plugin remove liskov-policy@liskov-skills
```

This is the first tag, so there is no older skill release to install in its
place. After removal, a local manifest file you already wrote stays on disk.
It was never published by the skill. Do not publish that file to recover
from a broken skill release. To use the tagged source without the
marketplace, check out `v1.0.0` and pass that directory to
`claude --plugin-dir`.
