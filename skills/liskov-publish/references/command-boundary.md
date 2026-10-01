# Command boundary

Read this while publishing. It is not a second workflow. Flags below are the
ones installed help prints. Do not add a flag help does not print.

The public [CLI](https://docs.proof.computer/liskov/reference/cli) page still
tells readers to install `@proof-computer/proof-cli-liskov` `0.14.0`. Its
examples omit `--no-analytics`. This skill does not. Do not install or switch
plugins from this skill.

Always pass `--no-analytics`. Help says that flag means do not report this
command invocation to Liskov product analytics. Always pass `--json`. Help
lists it on every command this skill runs.

A mutation needs an explicit user yes in this conversation and the command's
`--yes`. Showing a command is not that yes. `--dry-run` is still a server
call. Help says it previews the registered publication without committing
policy, pointer, or wakeup.

## The local command

Run this before any server call. It reads the local file and writes a verdict
to stdout. It does not create an Application, publish, reserve, or charge.

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

| Flag | Rule |
| --- | --- |
| `--file` | Required. The path the user pointed at. |
| `--json` | Always. |
| `--no-analytics` | Always. |
| `--organization` | Not printed. The CLI page says local manifest validation does not accept it. Do not add it. |
| `--yes`, `--dry-run` | Not printed. Do not add them. |

Flag order is `--file`, then `--json`, then `--no-analytics`. There is no
YAML flag. Do not add a parser. This skill does not repair the file.

## Organization

[Configuration and environment precedence](https://docs.proof.computer/liskov/reference/configuration-precedence)
gives the selection order for a network-backed organization-scoped command:

1. the command's existing positional selector, when supplied
2. `--organization SELECTOR`
3. `LISKOV_ORGANIZATION`
4. the persistent organization attached to the CLI session

The first three are exact organization ids or case-sensitive slugs. They are
invocation inputs. They are not saved to the session, copied into a manifest,
or installed in a runtime environment. Do not copy a selector into the
manifest.

The [CLI](https://docs.proof.computer/liskov/reference/cli) page says `whoami`
reads current identity, the effective organization, and the persistent session
organization. Under an override, human output labels both. JSON includes
`organizationContext.source`, `organizationContext.effective`, and
`organizationContext.sessionDefault`. The override is never written to the
local session or an Application runtime environment.

`organization use` replaces the persistent session organization. Run it only
when the user asked to change that default. `organization list` is unscoped.
Its help has no `--organization` flag. Do not add one. Do not pick an
organization from the list.

```sh
proof liskov whoami --json --no-analytics
```

```sh
proof liskov whoami --organization ORG_ID --json --no-analytics
```

```sh
proof liskov organization list --json --no-analytics
```

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

Call these only after the local validate result and the launch check both
pass. A failed check means no server call.

Pass `--config` only when the user pointed at a session file. Do not invent a
path. `whoami`, `organization list`, `organization use`, and `policy publish`
print `--slipway-url`. Pass it only when the user typed that compatibility
URL. Do not invent a host. Slipway, Blackbox, and Lockbox are compatibility
identifiers the user must type. Do not start those flows. Do not copy a
session token into the reply.

## Policy publish

Help: `APP_REF` is the exact Liskov Application id and must match
`document.applicationId`. Required flags are `--file`, `--artifact-digest`,
and `--expected-pointer-version`.

| Flag | Rule |
| --- | --- |
| `--file` | The validated file the user pointed at. |
| `--artifact-digest` | Pinned: the file's `release.artifact.digest`. Source: the attested artifact digest the user supplied. Never a sample. |
| `--expected-pointer-version` | The active pointer version the user observed. Do not assume one. |
| `--binding-revision`, `--revocation-epoch`, `--source-ref`, `--source-commit`, `--workflow-identity` | Source releases only, from the attested build the user supplied. Refused on a pinned release. |
| `--yes` | Confirms the mutation. Only after the user said to publish, having seen the schedule, the spend cap, the digest, and the pointer version. |
| `--dry-run` | Only when the user asked to preview. Still a server call. |
| `--paused` | Requires `--reason`. Only when the user asked to leave the Application paused and supplied a reason of 1 to 500 characters. |
| `--reason` | With `--paused` only. Do not send it alone. Do not invent it. |
| `--organization` | One organization for this command, when they named it. |
| `--json` | Always. |
| `--no-analytics` | Always. |

`--yes` and `--dry-run` are mutually exclusive. The CLI page says preview and
confirmation are mutually exclusive. The manifest reference says `dryRun`
compiles and resolves the document and release evidence, then rolls back
without committing policy, pointer, or wakeup. `postPublishStatus` `paused`
plus a reason commits a paused Application in the same transaction as
publication. The reference says those pause fields must be provided together.

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --binding-revision REVISION --revocation-epoch EPOCH --source-ref REF --source-commit COMMIT --workflow-identity IDENTITY --expected-pointer-version POINTER --yes --json --no-analytics
```

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --expected-pointer-version POINTER --yes --json --no-analytics
```

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --binding-revision REVISION --revocation-epoch EPOCH --source-ref REF --source-commit COMMIT --workflow-identity IDENTITY --expected-pointer-version POINTER --dry-run --json --no-analytics
```

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --expected-pointer-version POINTER --dry-run --json --no-analytics
```

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --binding-revision REVISION --revocation-epoch EPOCH --source-ref REF --source-commit COMMIT --workflow-identity IDENTITY --expected-pointer-version POINTER --paused --reason REASON --yes --json --no-analytics
```

Placeholders are not values. Do not type a sample digest. The authoring
guide's sample pointer, revision, epoch, ref, and commit are not observations.

## Commands that are not this skill

| Command | Rule |
| --- | --- |
| `application policy explain` | Reads a published Application. There is no local explain. Name liskov-proof. Do not run it. |
| `application create`, `source-binding set`, `source-binding revoke` | Name liskov-bind. Do not run them here. |
| `application import`, `application publish` | Version 4. Out of scope. |
| `application delete` | Out of scope. |
| `application run`, `application hold`, `application execution` | Do not run. Re-arm is not publication. |
| pause, resume, custody, admin, billing checkout | Do not run. This skill does not spend by those commands. |
| `organization billing`, `organization service-credits` | Do not run. A balance read is liskov-spend. This skill does not invent a balance. |
| `application backfill-identities`, `application deployment import`, `application artifact-pin restore` | Out of scope. |
| `application lockbox`, `application devtools`, `application runtime-image`, `application retirement-census` | Out of scope. `blackbox` is not a command in this plugin. |

Do not run `source-binding show` here to fill evidence. The source flags come
from the attested build the user supplied. If they are missing, name
liskov-release and stop.
