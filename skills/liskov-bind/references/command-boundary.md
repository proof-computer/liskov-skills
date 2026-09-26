# Command boundary

Read this while creating an Application or setting its source binding. It is
not a second workflow. Flags below are the ones installed help prints. Do not
add a flag help does not print.

The public [CLI](https://docs.proof.computer/liskov/reference/cli) page still
tells readers to install `@proof-computer/proof-cli-liskov` `0.14.0`. Its
examples omit `--no-analytics`. This skill does not. Do not install or switch
plugins from this skill.

Always pass `--no-analytics`. Help says that flag means do not report this
command invocation to Liskov product analytics. Always pass `--json` on the
commands below. Help lists it for each of them.

A mutation needs an explicit user yes in this conversation. Showing a command
is not that yes. Where help prints `--yes`, pass it only after that yes.
Create does not print `--yes`. Do not invent it.

## Organization

[Configuration and environment precedence](https://docs.proof.computer/liskov/reference/configuration-precedence)
gives the selection order for a network-backed organization-scoped command:

1. the command's existing positional selector, when supplied
2. `--organization SELECTOR`
3. `LISKOV_ORGANIZATION`
4. the persistent organization attached to the CLI session

The first three are exact organization ids or case-sensitive slugs. They are
invocation inputs. They are not saved to the session, copied into a manifest,
or installed in a runtime environment. `LISKOV_ORGANIZATION` is a CLI
invocation input, not a runtime contract. Do not declare it as a variable.

The [CLI](https://docs.proof.computer/liskov/reference/cli) page says `whoami`
reads current identity, the effective organization, and the persistent session
organization. Under an override, human output labels both. JSON includes
`organizationContext.source`, `organizationContext.effective`, and
`organizationContext.sessionDefault`. The override is never written to the
local session or an Application runtime environment.

`organization use` replaces the persistent session organization. Run it only
when the user asked to change that default, with the selector they named. Do
not pass a different `--organization` on that same command.
`organization list` is unscoped. Its help has no `--organization` flag. Do
not add one.

Do not copy a session token into the reply.

| Command | When |
| --- | --- |
| `whoami` | Read, before a write. |
| `organization list` | Read, when the user asked which organizations exist. Do not pick one. |
| `organization use` | Only when the user asked to change the session default. |

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

Pass `--config` only when the user pointed at a session file. Do not invent a
path. Pass `--slipway-url` or `--liskov-url` only when the user typed that
compatibility URL. Create, `whoami`, `organization list`, and `organization
use` print `--slipway-url`. Source-binding commands print `--liskov-url`. Do
not invent a host. Slipway, Blackbox, and Lockbox are compatibility
identifiers the user must type. Do not start those flows.

## Create

Help: "Create a Liskov Application from identity alone — no manifest of any
schema version." The authoring guide says creation writes no draft and spends
nothing. It is still a platform write. Run it only after the user said to
create that exact id.

| Flag or argument | Rule |
| --- | --- |
| `APPLICATION_ID` | The id the user stated. Not a sample. |
| `--repository` | Required for a GitHub App session. Pass the owner/name the user stated. |
| `--display-name` | Only when the user stated that name. |
| `--organization` | One organization for this command, when they named it. |
| `--json` | Always. |
| `--no-analytics` | Always. |
| `--yes` | Not printed. Do not invent it. |
| `--file` | Not printed. Create does not take a manifest. |

```sh
proof liskov application create APPLICATION_ID --json --no-analytics
```

```sh
proof liskov application create APPLICATION_ID --repository OWNER/NAME --organization ORG_ID --json --no-analytics
```

Omit `--repository` or `--organization` when the user did not supply that
value. Do not invent either one.

## Source binding

`APP_REF` on these commands is a Liskov Application uid, name, or legacy id.
Use the application id the user stated. Do not invent a second identifier.

Show is a read. Run it before every set when a binding may exist. Help says a
404 `source_binding_not_found` means the Application is not bound yet.

```sh
proof liskov application source-binding show APP_REF --json --no-analytics
```

Set creates or rotates the binding. Help says it requires an organization
admin with `application.source_binding.manage`. The authoring guide says a
maintainer cannot retarget source.

| Flag | Rule |
| --- | --- |
| `--repository` | Required. `owner/name` the user stated. |
| `--allowed-ref` | Required, repeatable, no default. One flag per ref the user stated. |
| `--workflow-identity` | Required. The exact identity the user stated. |
| `--manifest-path` | Required. The safe relative path the user stated. |
| `--yes` | Required by help. Pass it only after the user said to bind. |
| `--expected-revision` | Omit on create. On rotation, the revision `show` just returned. Help says `0` means update revision 0 and conflicts. |
| `--reason` | Optional. Only the reason the user supplied. |
| `--organization` | One organization for this command, when the user named it. Show and revoke accept it too. |
| `--json` | Always. |
| `--no-analytics` | Always. |

```sh
proof liskov application source-binding set APP_REF --repository OWNER/NAME --allowed-ref REF --workflow-identity IDENTITY --manifest-path MANIFEST_PATH --yes --json --no-analytics
```

```sh
proof liskov application source-binding set APP_REF --repository OWNER/NAME --allowed-ref REF --workflow-identity IDENTITY --manifest-path MANIFEST_PATH --expected-revision REVISION --yes --json --no-analytics
```

The authoring guide says the first binding is revision 1. That sentence is
not a value to pass. Omit `--expected-revision` on create, then read the
revision back with show if a later command needs it.

Revoke only when the user asked to revoke. Help requires `--expected-revision`,
`--reason`, and `--yes`, and says revoke advances the revocation epoch. A
later set must name that revision. The same admin permission applies.

```sh
proof liskov application source-binding revoke APP_REF --expected-revision REVISION --reason REASON --yes --json --no-analytics
```

Do not retry a failed set by inventing a revision. Show again only to read
what the server printed.

## Commands that are not this skill

Do not run these. A dry run is still not binding. There is no `--dry-run` on
create or source-binding. Do not invent one.

| Command | Rule |
| --- | --- |
| `application manifest validate` | Local draft check. Name liskov-policy. Do not run it here. |
| `application policy publish` | Consent gate. Name liskov-publish. Do not run it. |
| `application policy explain` | Reads a published Application. Name liskov-proof. Do not run it. |
| `application import`, `application publish` | Version 4. Out of scope. |
| `application delete` | Out of scope. |
| `application run`, `application hold`, `application execution` | Spend or lifecycle paths. Do not run. |
| `pause`, `resume`, custody, admin | Do not run. |
| `backfill-identities`, `deployment import`, `artifact-pin restore` | Out of scope. |
| `lockbox`, `devtools`, `blackbox`, `runtime-image`, `retirement-census` | Out of scope. |

This skill does not push a branch and does not attest. The authoring guide
says to create and bind before the first push whose workflow attests, and
that a successful local build does not create a binding. Naming that order
is allowed. Performing the push, the attest, or the publish is not.
