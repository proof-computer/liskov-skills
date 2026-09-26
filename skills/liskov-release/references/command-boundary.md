# Command boundary

Read this while writing the workflow. It is not a second workflow.

## No command in the workflow

This skill runs no `proof` command and no `proof liskov` command. The
workflow file must not contain one either. It has no spend credential. It
does not publish, import, deploy, reserve, or charge.

Do not copy a schema into the skill. Do not implement a validator.

`liskov-policy` drafts the manifest. `liskov-bind` is the later admin step
for the server source binding. Publication is `liskov-publish`. Naming those
skills is allowed. Doing their work is not.

## Commands that are not this workflow

Do not run any of these. Do not invent an Application id in order to call one.
Do not put one in the workflow. A dry run is still not this skill.

| Command | Why it is not this skill |
| --- | --- |
| `application manifest validate` | Reads a manifest. This skill does not write one. |
| `application create` | Creates an Application record. |
| `application import` | Out of scope. |
| `application publish` | V4 publication verb. Out of scope. |
| `application policy publish` | Publishes a policy version. |
| `source-binding set` | Server source binding. `liskov-bind` owns that later step. Do not run it. |
| `artifact-pin list` | The actions guide shows this read. Reviewed help includes `--json` and global `--no-analytics`. The guide's example omits `--no-analytics` and uses a sample Application id. This skill does not run the read and does not copy that example. |
| `artifact-pin restore` | Out of scope. |
| `application run` | Launch path. Out of scope. |
| `application execution` | Out of scope. |

Also do not run `admin`, `custody`, `application delete`,
`backfill-identities`, `deployment import`, `retirement-census`,
`runtime-image`, `devtools`, `blackbox`, or `lockbox`. The last two are
compatibility command names. Do not type them.

The actions guide's pin-list example is not a workflow step. Do not "fix"
it by adding flags and running it from this skill.

## What the file may contain

| Piece | Rule |
| --- | --- |
| `permissions.contents` | `read`, copied from the actions page. |
| `permissions.id-token` | `write`, GitHub OIDC. Not a spend credential. |
| `uses` | The actions page's workflow path at `@v1`, or that path at the reviewed commit when the user asked for the security-sensitive pin. |
| `with` | Only keys the page's caller shows, and only values the user stated. |
| Secrets | None by default. No Liskov API token. No service-credit key. No pasted key value. |
| Publish, create, import, source-binding | Absent. |
