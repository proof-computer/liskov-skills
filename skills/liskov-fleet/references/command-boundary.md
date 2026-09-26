# Command boundary

Read this while building the fleet picture. It is not a second workflow.
Do not implement a second validator.

Reviewed help is `@proof-computer/proof-cli-liskov` `0.16.0`. The public
CLI reference still names plugin `0.14.0` in its install example. Follow
these flags. Always pass `--json` and `--no-analytics`.

The picture is read only and one organization.

## Session, then list, then status

```sh
proof liskov whoami --json --no-analytics
```

```sh
proof liskov application list --json --no-analytics
```

```sh
proof liskov application status APP --json --no-analytics
```

`whoami` JSON on the reviewed CLI reference includes
`organizationContext.source`, `organizationContext.effective`, and
`organizationContext.sessionDefault`. Under an override, human output labels
both the effective organization and the persistent organization. The reply
must say whether those two differ. Do not invent a name when a field is
absent.

`application list` help flags are `--config`, `--deleted`, `--retired`,
`--json`, `--liskov-url`, `--organization`, and global `--no-analytics`.
There is no limit flag and no page flag. Do not invent pagination. Do not
invent `--limit` or `--before` on this command. Say the bound: one response,
whatever that JSON contains.

`--deleted` is a deprecated alias for `--retired`. Do not use `--deleted`.

```sh
proof liskov application list --retired --json --no-analytics
```

Use `--retired` only when the user asked for retired Applications. It
replaces the live view. It is not a second page.

`APP` is an id the user named, or an id printed in that list response when
they named nobody and asked for the fleet. The CLI reference says an
Application ref may be a uid, a name, or an id, and prefers the uid for
automation. Do not invent an application id. Do not status the rest of the
page when they named a subset. Do not status anything outside that set.

Reviewed status flags: `--config`, `--json`, `--organization`,
`--slipway-url`, and global `--no-analytics`. Do not pass `--config`,
`--slipway-url`, or `--liskov-url` unless the user supplied that value.

## One command's organization

```sh
proof liskov whoami --organization ORGANIZATION --json --no-analytics
```

```sh
proof liskov application list --organization ORGANIZATION --json --no-analytics
```

```sh
proof liskov application status APP --organization ORGANIZATION --json --no-analytics
```

Pass `--organization` only when the user asked to scope the read, and pass
the same selector on whoami, list, and status. `ORGANIZATION` is their exact
id or slug. `LISKOV_ORGANIZATION` is the same scope at lower precedence. Do
not run `organization use` unless the user asked to change the session
default. Do not call `organization list` to scan other organizations.

## No bulk and no mutation loop

Do not run a mutation inside a loop. Not even a dry run. A pause or retire
of one Application is liskov-operate, after its own yes. Money figures are
liskov-spend. If status output has no charge field, do not invent a spend
number.

| Command | Why it is refused here |
| --- | --- |
| `application pause`, `resume` | Lifecycle mutation. Not a fleet read |
| `application retire` and `retire cancel` | Retirement mutation even when `--yes` is absent is a preview this skill does not run |
| `application publish`, `application policy publish` | Publication. No bulk publish |
| `application action-plan retry` | No bulk retry. Do not retry from a loop |
| `application run` | Out of scope |
| `application hold` | Out of scope |
| `application execution` | Out of scope |
| `application import` | V4 import. Out of scope |
| `admin`, `custody`, `delete` | Out of scope |
| `lockbox`, `devtools`, `blackbox`, `runtime-image` | Out of scope |
| `organization use` | Changes the persistent organization. Only when the user asked |
| `organization billing`, `service-credits`, `billing transactions` | Money. liskov-spend |

Reading `application action-plan` is still a decision surface. This skill
does not open it and does not retry. The operate guide's retry command is
not a fleet action.

Status help says the command reads status and the canonical retained V5
policy explanation. That read is allowed. It does not recompute spend. Do
not treat a coverage line as a charge unless the JSON has a charge field.
If it does not, do not invent a spend number.
