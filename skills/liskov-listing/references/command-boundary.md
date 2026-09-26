# Command boundary

Read this while preparing a listing. It is not a second workflow. Do not implement a second validator.

Reviewed help is `@proof-computer/proof-cli-liskov` `0.16.0` on
`@proof-computer/proof-cli` `0.1.2`. Public examples often omit
`--no-analytics`. This skill does not. Flag order is command, then
`--organization` only when scoping one command, then `--json`, then
`--no-analytics`.

## No launch command

There is no Marketplace browse command and no launch command. Do not invent
`marketplace`, `listing`, or a launch flag. Do not send the user through a
Console form while the release gate stands.

The only commands this skill runs are the three reads below. Run them only
after the user says the Console launch finished, and only with the
Application id they give.

| Command | Role | Not this |
| --- | --- | --- |
| `application status` | Read customer posture for `APP` | Not a launch, not a spend figure |
| `application policy explain` | Read the retained explanation | Does not recompute policy, spend, or eligibility |
| `application artifact-pin list` | Read pin evidence and compare digests | Not `artifact-pin restore` |

```sh
proof liskov application status APP --json --no-analytics
```

```sh
proof liskov application policy explain APP --json --no-analytics
```

```sh
proof liskov application artifact-pin list APP --json --no-analytics
```

`APP` is the id the user gave. Do not invent an application id. Help for each
command lists `--json`. Always pass `--json` and `--no-analytics`.

Reviewed flags for all three: `--config`, `--json`, `--organization`,
`--slipway-url`, and global `--no-analytics`. Do not pass `--slipway-url` or
`--config` unless the user supplied that value. Do not invent a URL.

`application list` has no limit flag and no page flag. Do not use it to
invent a Marketplace catalog. Do not invent `--limit`.

## One organization

`--organization ORGANIZATION` or `LISKOV_ORGANIZATION` scopes that one
command. `ORGANIZATION` is the exact id or slug the user gave. Do not invent
an organization. Do not run `organization use` unless the user asked to
change the session default. `organization use` is persistently mutating.

```sh
proof liskov application status APP --organization ORGANIZATION --json --no-analytics
```

Use the same selector on the other two reads when the user asked to scope
them. Do not pass a `key=value` form the user did not type. The selector is
one id or slug.

## Digest check

Compare a digest the artifact-pin JSON actually prints to the digest the
public listing page prints when you read it. Do not type a digest from
memory into the command or the manifest. If either side has no digest, the
check is incomplete. Do not invent the expected digest.

## Commands that are not this skill

Do not run any of these. A dry run is still not a listing launch.

| Command | Why it is refused |
| --- | --- |
| Marketplace browse or launch | No such command. Do not invent one |
| `application create` | Creates an Application. Not a Marketplace launch |
| `application import` | V4 import path. Out of scope |
| `application publish` | Publication path. Out of scope |
| `application policy publish` | Publishes policy, including `--dry-run` |
| `application pause`, `resume`, `retire` | Lifecycle. One Application belongs to liskov-operate, after its own yes |
| `application run` | Authorizes another occurrence. Out of scope |
| `application hold` | Hold release. Out of scope |
| `application execution` | Out of scope |
| `admin`, `custody`, `delete` | Out of scope |
| `lockbox`, `devtools`, `blackbox`, `runtime-image` | Out of scope |
| `artifact-pin restore` | Mutation. This skill only lists pins |
| `organization use` | Changes the session default. Only when the user asked |

Money figures are liskov-spend. The prober page prints no price. Do not
invent one. Do not approve Marketplace spend from this skill.

This skill does not read a secret back and does not repeat a pasted token.
Do not send the user to type one into a form while the gate stands.
