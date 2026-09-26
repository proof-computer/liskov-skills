# Command boundary

Read this while editing configuration. It is not a second workflow.

## The one command

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

Reviewed help: "Strictly validate an authored Application manifest v4 or
retained V5 file without publishing it." That help text is not this skill's
support list. This skill edits only `proof.liskov.application-manifest` at
`schemaVersion` 5.

| Flag | Rule |
| --- | --- |
| `--file` | Required. The file the user pointed at. |
| `--json` | Always. |
| `--no-analytics` | Always. Help says this means do not report this command invocation to Liskov product analytics. |
| `--organization` | Not printed. The CLI page says local manifest validation does not accept it. Do not add it. |
| `--yes`, `--dry-run` | Not printed. Do not add them. |

Flag order is `--file`, then `--json`, then `--no-analytics`. There is no
YAML flag. The command parses JSON. Do not add a YAML parser. Do not copy a
schema into the skill and do not implement a second validator.

Stdout of a completed run is one JSON object. An `EEXIT` banner is not the
verdict. Parsers use the JSON object. Exit `0` when `errors` is empty. Exit
`1` when `errors` is non-empty. Exit `1` with a JSON object is a diagnostic,
not a missing validator.

With `--no-analytics`, the process reads the local file and writes a verdict
to stdout. It does not create an Application, publish, deploy, reserve, or
charge. This skill does not publish.

Run the command at most three times.

## Organization

This skill does not select an organization and does not call the network.

[Configuration and environment precedence](https://docs.proof.computer/liskov/reference/configuration-precedence)
says `--organization` and `LISKOV_ORGANIZATION` select one organization for
one network-backed command. They are not saved to the session, copied into a
manifest, or installed in a runtime environment. `LISKOV_ORGANIZATION` is a
CLI invocation input, not a runtime contract. Do not declare it as a variable.

`organization use` changes the persistent session organization. Do not run
it. The [CLI](https://docs.proof.computer/liskov/reference/cli) page says
`whoami` distinguishes the effective organization and the persistent session
organization. Do not run `whoami` from this skill.

`organization list` is unscoped and its help has no `--organization` flag.
Do not run it here, and do not invent that flag.

Do not pass `--slipway-url`, `--liskov-url`, or a Slipway, Blackbox, or
Lockbox identifier to validate. Those names are compatibility identifiers
the user must type on a command that prints the flag. They are not manifest
fields. Leave them out of the file.

## Commands that are not configuration

Do not run any command except the validate command above. In particular:

| Command | Rule |
| --- | --- |
| `application create`, `source-binding set`, `source-binding revoke` | Name liskov-bind. Do not run. |
| `application policy publish`, including `--dry-run` | Name liskov-publish. A dry run is still a server call. Do not run. |
| `application policy explain` | Name liskov-proof. There is no local explain. Do not run. |
| `application import`, `application publish` | Version 4. Out of scope. |
| `application vars set`, `application vars unset`, `application vars list` | The variables page says these commands are not in a released package. Set non-secret managed values in the Console. Do not run them. |
| `application secrets` | The secrets page says the public CLI can inspect requirements and does not write or reveal values. Do not run it. The value is entered in the Console secret store, which this skill does not call. |
| `application delete`, `application run`, `application hold`, `application execution` | Out of scope. |
| pause, resume, custody, admin | Do not run. |
| `backfill-identities`, `deployment import`, `artifact-pin restore` | Out of scope. |
| `lockbox`, `devtools`, `blackbox`, `runtime-image`, `retirement-census` | Out of scope. |

Editing the file does not reserve a USD Service Credit and does not create a
final charge. Showing a diff is not permission to publish.
