# Command boundary

Read this while writing the program. It is not a second workflow.

## No command

This skill runs no `proof` command and no `proof liskov` command. It does not
write the manifest, so it does not validate one. It does not publish, deploy,
reserve, or charge.

Do not copy a schema into the skill. Do not implement a validator.

`liskov-policy` drafts the manifest. `liskov-configure` is the later place
for manifest logging and configuration fields this skill must not set.
Naming those skills is allowed. Doing their work is not.

## Commands that are not this program

Do not run any of these. Do not invent an Application id in order to call one.

| Command | Why it is not this skill |
| --- | --- |
| `application manifest validate` | Reads a manifest. This skill does not write one. |
| `application create` | Creates an Application record. |
| `application import` | Out of scope. |
| `application publish` | V4 publication verb. Out of scope. |
| `application policy publish` | Publishes a policy version. |
| `source-binding set` | Server source binding. Not this program. |
| `application run` | Launch path. Out of scope. |
| `application execution` | Out of scope. |
| `application logs` | A read of managed logs. This skill emits `runtime.log` inside the job and does not call the CLI. |
| `application hold` | Out of scope. |
| `runtime-image` | Out of scope. Do not invent a catalogue image here. |

Also do not run `admin`, `custody`, `application delete`,
`backfill-identities`, `deployment import`, `artifact-pin restore`,
`retirement-census`, `devtools`, `blackbox`, or `lockbox`. The last two are
compatibility command names. Do not type them.

Reviewed help is not permission to run a command this skill does not own.

## Not a shell step

Do not add a package-manager command that publishes, deploys, or spends. The
dependency pin is a line in the program's package file, using only a version
string from [Limits](limits.md). Do not invent a registry token.
