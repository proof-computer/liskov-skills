# Command boundary

Read this while deciding. It is not a second workflow.

## No command

This skill runs no `proof` command and no `proof liskov` command. It does not
write a manifest, so it does not validate one. It does not publish, deploy,
reserve, or charge.

Do not copy a schema into the skill. Do not implement a validator. A refusal
to run a command is not a validate result.

`liskov-policy` is the later skill that drafts the manifest. `liskov-runtime`
is the later skill that writes the job. Naming them is allowed. Doing their
work is not.

## Commands that are not this decision

Do not run any of these. Do not invent an Application id in order to call one.
A dry run is still not this decision.

| Command | Why it is not this skill |
| --- | --- |
| `application manifest validate` | Reads a manifest. This skill does not write one. |
| `application create` | Creates an Application record. |
| `application import` | Imports a manifest. Out of scope. |
| `application publish` | V4 publication verb. Out of scope. |
| `application policy publish` | Publishes a policy version, including a dry run. |
| `source-binding set` | Server source binding. Not this decision. |
| `application run` | Launch path. Out of scope. |
| `application execution` | Out of scope. |
| `application hold` | Out of scope. |
| `application artifact-pin restore` | Out of scope. |
| `application deployment import` | Out of scope. |

Also do not run `admin`, `custody`, `application delete`,
`application backfill-identities`, `application retirement-census`,
`application runtime-image`, `application devtools`, or
`application lockbox`. `blackbox` is not a command in this plugin. Do
not invent one.

Reviewed help is not permission to run a command this skill does not own.
There is no flag to add to make one of them a fit decision.
