# Command boundary

Read this while operating. It is not a second workflow.

Reviewed help is the flag authority. Fenced commands pass `--no-analytics`.
Pass `--json` as well, except on `application logs` when the command includes
`--follow`, `--from-start`, `--ndjson`, or `--event`. The installed CLI
rejects that combination. Help does not print the exclusion. Do not add `--config`,
`--slipway-url`, or `--liskov-url` unless the user supplied that value. Do not
invent a URL.

`APP_REF` and `APPLICATION_ID` are both the Application identifier the user
gave. Help prints `APPLICATION_ID` on status and plans, and `APP_REF` on the
other Application commands below. Do not put a deployment id or a job id in
that position. `ORG_ID` is an organization id or slug the user gave.
`REASON` is the user's words. `DECISION_ID` is the decision id from the
action-plan JSON just read. If you do not have the value, do not invent it,
and omit the flag.

Flag order is the command's own flags, then `--organization ORG_ID` only when
the user scoped this command, then `--json --no-analytics`. The fences omit
`--organization` unless that is the point of the fence.

## Organization

```sh
proof liskov whoami --json --no-analytics
```

whoami is a read. Quote the organization fields it prints. That is how you
separate the effective organization for a command from the persistent session
organization. Do not rename those fields.

`--organization ORG_ID` or `LISKOV_ORGANIZATION` scopes one command. It does
not change the session default. One scoped read looks like this, and only when
the user gave `ORG_ID`:

```sh
proof liskov application status APPLICATION_ID --organization ORG_ID --json --no-analytics
```

`organization use` changes the persistent session default. Run it only when
the user asked for that change. Help has no `--yes` flag. Do not invent one.
The user's ask is the confirmation.

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

## Reads

A read does not spend. It does not publish, reserve, or charge.

```sh
proof liskov application list --json --no-analytics
```

Pass `--retired` only when the user asked to see retired Applications. Help
calls `--deleted` a deprecated alias for `--retired`. Do not pass it. It is
not a delete.

```sh
proof liskov application list --retired --json --no-analytics
```

```sh
proof liskov application status APPLICATION_ID --json --no-analytics
```

Help also returns the canonical retained V5 policy explanation with status.
Quote it. It is not a local unpublished file and it is not a launch.

```sh
proof liskov application action-plan APP_REF --json --no-analytics
```

```sh
proof liskov application activity APP_REF --json --no-analytics
```

Help's optional activity flags are `--limit` and `--before`. `--limit` is a
maximum number of events. `--before` is an epoch millisecond timestamp. Pass
either only with a value the user gave or a cursor the previous JSON printed.
This command has no `--follow` and no `--from-start`.

```sh
proof liskov application logs APP_REF --json --no-analytics
```

That logs command is the recent window, not full history. Optional flags, and
only the ones that apply:

| Flag | Pass it only when |
| --- | --- |
| `--deployment DEPLOYMENT_ID` | That deployment id was given by the user or printed just now |
| `--job JOB_ID` | That job id was given by the user or printed just now |
| `--event GLOB` | The user asked for that event glob |
| `--origin ORIGIN` | `ORIGIN` is `all`, `customer`, `runtime-ssh`, or `runtime_ssh` |
| `--limit LIMIT` | The user asked for that maximum |
| `--from-start` | The user asked for the full retained history, oldest first |
| `--ndjson` | The user asked for one raw record per line |
| `--follow` | The user asked to watch |

Do not invent a deployment id, a job id, or an event name. `--origin` has no
other values. Pass `--follow` only when the user asked to watch. Omit
`--json` on that command, and also when passing `--from-start`, `--ndjson`,
or `--event`:

```sh
proof liskov application logs APP_REF --follow --no-analytics
```

```sh
proof liskov application plans APPLICATION_ID --json --no-analytics
```

```sh
proof liskov application deployment status APP_REF --json --no-analytics
```

Help prints one argument, `APP_REF`. There is no deployment-id positional and
no `--deployment` flag on this command.

## Mutations

Run a mutation only after an explicit yes in the conversation.

Pause without `--yes` is a dry run. Help: without `--yes` the server returns
a dry run. Say that. Do not claim the Application paused.

```sh
proof liskov application pause APP_REF --json --no-analytics
```

After yes, pause. Omit `--reason` unless the user gave the words. `--owner`
exists only to disambiguate a legacy Application id. Pass it only when the
user supplied that owner. Do not invent an owner or a reason.

```sh
proof liskov application pause APP_REF --yes --json --no-analytics
```

```sh
proof liskov application pause APP_REF --reason REASON --yes --json --no-analytics
```

Pause changes future Liskov planning. The current job keeps running until
schedule end. Do not claim pause stopped it. A held job is not a paused
Application. This command does not release a hold.

Resume without `--yes` is a dry run. The same help rule: the server returns a
dry run. It does not resume.

```sh
proof liskov application resume APP_REF --json --no-analytics
```

```sh
proof liskov application resume APP_REF --yes --json --no-analytics
```

```sh
proof liskov application resume APP_REF --reason REASON --yes --json --no-analytics
```

`--override-replacement-hold` is legal only together with `--reason` and
`--yes`, and only when the user asked to override that hold. Do not add it to
an ordinary resume.

```sh
proof liskov application resume APP_REF --override-replacement-hold --reason REASON --yes --json --no-analytics
```

Resume lets Liskov evaluate desired state again. It can open a new successor
and reserve new USD Service Credits. A reserve is not a final charge. Resume
does not revive an ended job and does not clear a hold.

Retire without `--yes` is read only. Help: without `--yes` the command is read
only. It does not start retirement.

```sh
proof liskov application retire APP_REF --json --no-analytics
```

After yes, retire starts retirement. Help: `--yes` pauses the Application and
starts retirement. Optional `--reason` is the user's words. Help limits that
reason to 500 characters. If their words are longer, ask. Do not invent a
shorter reason.

```sh
proof liskov application retire APP_REF --yes --json --no-analytics
```

```sh
proof liskov application retire APP_REF --reason REASON --yes --json --no-analytics
```

Existing schedules continue to their chain-owned end. The result the user
waits for is the retirement receipt, not an immediate delete.

Cancel only after an explicit yes. Help does not call a missing `--yes` a read
or a dry run. Do not omit `--yes`. Cancel leaves the Application paused. Do
not claim it resumed. The same 500-character limit applies to this optional
reason.

```sh
proof liskov application retire cancel APP_REF --yes --json --no-analytics
```

```sh
proof liskov application retire cancel APP_REF --reason REASON --yes --json --no-analytics
```

Retry only after an explicit yes, and only once. Help requires `--decision-id`
and `--reason`. It does not call a missing `--yes` a dry run. Do not omit
`--yes`. Do not loop. Do not invent the id or the reason.

```sh
proof liskov application action-plan retry APP_REF --decision-id DECISION_ID --reason REASON --yes --json --no-analytics
```

One retry does not mean keep trying, and it does not bypass a spend limit. If
the same blocker remains, stop.

## Commands this skill does not run

Do not run these. Do not add flags, examples, or a procedure for them.

| Command | Rule |
| --- | --- |
| `admin` | Do not run. |
| `custody` | Do not run. |
| `delete` | Do not run. Retirement is not a delete. |
| `import` | Do not run. |
| V4 `application publish` | Do not run. |
| `application backfill-identities` | Do not run. |
| `application deployment import` | Do not run. |
| `application artifact-pin restore` | Do not run. |
| `application lockbox` | Do not run. |
| `application devtools` | Do not run. |
| `application runtime-image` | Do not run. `blackbox` is not a command in this plugin. |
| `application execution` | Do not run. |
| `application hold` | Do not run. A hold is not a pause. |
| `application run` | Do not run. |
| `application retirement-census` | Do not run. |
| `application policy publish` | Do not run. |
| `source-binding set` | Do not run. |
| SSH and `runtime-ssh` | Do not run. |

Do not implement a second validator.
