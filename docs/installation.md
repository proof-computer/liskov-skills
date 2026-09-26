# Installation

Version `0.0.0` is not a GitHub release and not a released skill. The shared
source is `skills/liskov-policy/`. Claude Code and Codex both use that
directory. Packaging does not copy the workflow into a second tree.

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

Codex's repository catalog is `.agents/plugins/marketplace.json`. That file is
not in this repository. Packaging tests build a temporary catalog that points
at the plugin root. A later release checks whether
`codex plugin marketplace add` of this repository needs a public catalog, and
does not invent catalog fields while doing that.

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
codex plugin marketplace add proof-computer/liskov-skills
codex plugin add liskov-policy@liskov-skills
codex plugin remove liskov-policy
```

On Codex CLI `0.157.1`, the bare `codex plugin remove liskov-policy` command
above is rejected with `plugin requires --marketplace unless passed as
<plugin>@<marketplace>`. The same help accepts
`codex plugin remove liskov-policy@liskov-skills`.
