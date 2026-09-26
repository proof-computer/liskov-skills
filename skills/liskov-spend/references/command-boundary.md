# Command boundary

Read this while answering a money question. It is not a second workflow. This
skill is read only.

Reviewed help is the flag authority. Every fenced command passes `--json` and
`--no-analytics`. Do not add `--config`, `--slipway-url`, or `--liskov-url`
unless the user supplied that value. Do not invent a URL.

`ORG_ID` is an organization id or slug. Billing, service credits, and billing
transactions require one. The session organization is not a default for those
three reads. Use the selector the user gave. When they gave none, use the
effective organization id or slug whoami just printed. When that read printed
none, ask. Do not invent an organization id. `APPLICATION_ID` is the
Application id the user gave. `BEFORE` is a Unix time in milliseconds the
user gave or the previous JSON printed. `LIMIT` is a maximum the user asked
for. If you do not have the value, do not invent it, and omit the flag.

## Organization

```sh
proof liskov whoami --json --no-analytics
```

whoami is a read. Quote the organization fields it prints. That read separates
the effective organization from the persistent session organization. Do not
rename those fields.

Do not run billing, service credits, or billing transactions without `ORG_ID`.
Help's generic organization line mentions a session default. These three
commands do not use it. A missing selector fails before the read.

When the user gave `ORG_ID` for this command, pass it once. Prefer the
positional help prints. Do not also pass a different `--organization` value.

```sh
proof liskov organization billing ORG_ID --json --no-analytics
```

```sh
proof liskov organization service-credits ORG_ID --json --no-analytics
```

```sh
proof liskov organization billing transactions ORG_ID --json --no-analytics
```

Help on transactions prints `--limit` as the maximum number of transactions to
return and `--before` as a Unix time in milliseconds. Help does not print a
numeric default. Do not invent a page size or a cursor.

```sh
proof liskov organization billing transactions ORG_ID --limit LIMIT --before BEFORE --json --no-analytics
```

Use that second transactions command only with values the user supplied or a
cursor the previous JSON printed. Otherwise use the command without those
flags.

`--organization ORG_ID` or `LISKOV_ORGANIZATION` is the other way to scope one
command when you are not passing the positional:

```sh
proof liskov organization service-credits --organization ORG_ID --json --no-analytics
```

Run `organization use` only when the user asked to change the session default.
Help has no `--yes` flag. Do not invent one. Do not run it to scope one read.

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

## Optional plan cap

When the user named an Application, this read is allowed. It is still read
only. The cap in the policy is authority the user set. It is not the settled
charge. Do not call that cap a reserve or a final charge unless the JSON field
says so.

```sh
proof liskov application plans APPLICATION_ID --json --no-analytics
```

Help: plans reads execution plans. It does not settle a charge.

## Billing fields you may quote

Service credits help reads balances. Billing help reads billing state. If the
JSON includes `addFunds.checkoutAvailable` or `addFunds.checkoutAdmission`
(`enabled`, `configured`, `available`, `reason`), quote those fields. If an
older response omits them, that response does not report Checkout
availability. A displayed balance does not prove that purchases are enabled.

These reads do not fund, reserve, or charge.

## Commands this skill does not run

There is no CLI command to fund, change plan, or pay. Checkout is not a
supported customer action. Do not invent a command. Do not ask for a card
number or a bank detail.

Do not run these. Do not add flags, examples, or a procedure for them.

| Command | Rule |
| --- | --- |
| `admin` | Do not run. |
| `custody` | Do not run. |
| `delete` | Do not run. |
| `import` | Do not run. |
| V4 `application publish` | Do not run. |
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
| pause, resume, retire, retry | Do not run. |
| SSH and `runtime-ssh` | Do not run. |

Do not implement a second validator. Do not follow an internal signer command.
