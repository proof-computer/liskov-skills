# Command boundary

Read this while diagnosing. It is not a second workflow. End at one next
action. The reads do not spend.

Reviewed help is the flag authority. Fenced commands pass `--no-analytics`.
Pass `--json` as well, except on `application logs` when the command includes
`--follow`, `--from-start`, `--ndjson`, or `--event`. The installed CLI
rejects that combination. Help does not print the exclusion. Do not add `--config`, `--slipway-url`, or `--liskov-url`
unless the user supplied that value. Do not invent a URL.

`APPLICATION_ID` and `APP_REF` are the Application identifier the user gave.
Help prints `APPLICATION_ID` on status and `APP_REF` on the Action Plan,
deployment status, logs, and retry. Do not put a deployment id or a job id in
that position. `DECISION_ID` is the decision id in the action-plan JSON just
read. `REASON` is the user's words. `ORG_ID` is an organization id or slug the
user gave. If you do not have the value, do not invent it.

## Organization

```sh
proof liskov whoami --json --no-analytics
```

whoami is a read. Quote the organization fields it prints. That read separates
the effective organization from the persistent session organization.

`--organization ORG_ID` or `LISKOV_ORGANIZATION` scopes one command. Run
`organization use` only when the user asked to change the session default.
Help has no `--yes` flag. Do not invent one.

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

```sh
proof liskov application status APPLICATION_ID --organization ORG_ID --json --no-analytics
```

The scoped status command is only when the user gave `ORG_ID` for this
command. Otherwise omit `--organization`.

## Reads

These four Application reads are the diagnosis. Do not add activity, plans,
or secrets as another diagnosis read. Quote the JSON.

```sh
proof liskov application status APPLICATION_ID --json --no-analytics
```

```sh
proof liskov application action-plan APP_REF --json --no-analytics
```

```sh
proof liskov application deployment status APP_REF --json --no-analytics
```

Help prints one deployment-status argument, `APP_REF`. There is no
deployment-id positional.

The recent window is the logs default. It is not a count of 100. The logs
page uses `--limit 100` as an example cap. Pass `--limit` only when the user
named a count. Do not pass `--from-start`. Pass `--follow` only when the user
asked to watch, and still end at one next action. Omit `--json` when the
command includes `--follow`, `--from-start`, `--ndjson`, or `--event`.

```sh
proof liskov application logs APP_REF --json --no-analytics
```

```sh
proof liskov application logs APP_REF --follow --no-analytics
```

The `--follow` command is only when the user asked to watch.

Optional logs flags, only with values the user gave or JSON just printed:
`--deployment`, `--job`, `--event`, `--origin`, and `--ndjson`. `--origin` is
only `all`, `customer`, `runtime-ssh`, or `runtime_ssh`. Do not invent an id
or an event name.

## The one mutation

Retry is the only mutation in this skill. Run it only when all of these are
true: the action-plan JSON just read includes that decision id, the limits say
retry is the one next action, and the user has said yes. Help requires
`--decision-id` and `--reason`. It does not call a missing `--yes` a dry run.
Do not omit `--yes`. One retry. Do not loop. Do not invent the id or the
reason.

```sh
proof liskov application action-plan retry APP_REF --decision-id DECISION_ID --reason REASON --yes --json --no-analytics
```

Showing that command is not itself a retry. Do not run it in the same breath
as a human step.

## Commands this skill does not run

Do not run `application run`. Re-running a completed Application is
release-gated, and that CLI path is not supported yet. Do not delete.

Do not run these. Do not add flags, examples, or a procedure for them.

| Command | Rule |
| --- | --- |
| `admin` | Do not run. |
| `custody` | Do not run. |
| `delete` | Do not run. |
| `import` | Do not run. |
| V4 `application publish` | Do not run. |
| `application policy publish` | Do not run. |
| `backfill-identities` | Do not run. |
| `deployment import` | Do not run. |
| `artifact-pin restore` | Do not run. |
| `lockbox` | Do not run. |
| `devtools` | Do not run. |
| `blackbox` | Do not run. |
| `runtime-image` | Do not run. |
| `application execution` | Do not run. |
| `application hold` | Do not run. |
| `application run` | Do not run. |
| `retirement-census` | Do not run. |
| `source-binding set` | Do not run. The human step names the binding. It does not perform it. |
| SSH and `runtime-ssh` | Do not run. The human step names the operator key. It does not install one. |
| pause, resume, retire | Do not run them as the next action. Pause behavior is a limit, not a second command. |

Do not implement a second validator. Do not print a managed secret value.
