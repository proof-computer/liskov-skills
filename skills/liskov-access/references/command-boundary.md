# Command boundary

Read this while operating managed Runtime SSH. It is not a second workflow.
Do not implement a second validator.

Reviewed help is `@proof-computer/proof-cli-liskov` `0.16.0`. Public page
examples omit `--no-analytics` and sometimes `--json`. This skill does not.
Fenced commands pass `--no-analytics`. Pass `--json` as well, except on an
open that uses `--accept-host-key`. That open omits `--json` so it is not a
silent pin. Flag order puts the remaining output flags last.

`APP`, `NAME`, `PUBLIC_KEY_FILE`, `IDENTITY_PATH`, `KEY_ID`, `FINGERPRINT`,
`WITHDRAWAL_ID`, `ATTACHMENT_ID`, `DEPLOYMENT`, `JOB`, and `ORGANIZATION`
are substituted from the user or from JSON a command just printed. Do not
invent them. Do not invent a host key.

`--organization ORGANIZATION` or `LISKOV_ORGANIZATION` scopes that one
command. The selector is the exact id or slug the user gave. Do not run
`organization use` unless the user asked to change the session default.

Do not pass `--config` or `--slipway-url` unless the user supplied that
value. Do not pass `--reason` unless the user supplied the text.

## Operator keys

Help for add lists `--name` (required), `--identity`, `--public-key-file`,
`--json`, `--organization`, `--config`, `--slipway-url`. It does not list
`--yes`. Do not invent `--yes`. It does not list a flag that takes a public
key as a command argument. `--public-key-file -` reads stdin.

`--identity` is a filesystem path the user supplies. The command sends the
public half. Do not echo file contents. do not generate a key. Do not write
a private key into the repo or the reply.

```sh
proof liskov runtime-ssh operator-key list --json --no-analytics
```

```sh
proof liskov runtime-ssh operator-key add --name NAME --public-key-file PUBLIC_KEY_FILE --json --no-analytics
```

```sh
proof liskov runtime-ssh operator-key add --name NAME --identity IDENTITY_PATH --json --no-analytics
```

Pass exactly one of `--public-key-file` or `--identity`. Register before the
first launch. Add authorizes new attachments, not an existing one.

Help for remove says remove withdraws access. New connection requests and
tickets are refused, unused tickets are revoked, and a session already open
drains. Nothing is republished. Run only after an explicit yes. `KEY_ID`
comes from `operator-key list`.

```sh
proof liskov runtime-ssh operator-key remove KEY_ID --json --no-analytics
```

Reviewed remove flags: optional organization argument, optional `KEY_ID`
argument, `--json`, `--organization`, `--config`, `--slipway-url`. No
`--yes` on the command. The yes is the user's words, before you run it.

## Withdrawals

Use only the flags help prints.

| Command | Flags help prints | Effect |
| --- | --- | --- |
| `withdrawn-key add` | `--fingerprint` or `--identity`, optional `--reason`, `--json`, `--organization`, `--config`, `--slipway-url` | Add withdraws. Unused tickets are revoked. An open session drains |
| `withdrawn-key list` | `--json`, `--organization`, `--config`, `--slipway-url` | List withdrawn fingerprints |
| `withdrawn-key remove` | `WITHDRAWAL_ID` argument, `--json`, `--organization`, `--config`, `--slipway-url` | Remove lifts a withdrawal and does not by itself re-register a key |

```sh
proof liskov runtime-ssh withdrawn-key add --fingerprint FINGERPRINT --json --no-analytics
```

```sh
proof liskov runtime-ssh withdrawn-key add --identity IDENTITY_PATH --json --no-analytics
```

```sh
proof liskov runtime-ssh withdrawn-key list --json --no-analytics
```

```sh
proof liskov runtime-ssh withdrawn-key remove WITHDRAWAL_ID --json --no-analytics
```

Run add and remove only after an explicit yes. Pass `--reason REASON` on add
only when the user supplied `REASON`. For a registered key, prefer
`operator-key remove`, which withdraws as part of removal. Use
`withdrawn-key add` for a key that has no registry row. Lifting a withdrawal
does not put the key back into the registry.

## Attachments

```sh
proof liskov runtime-ssh attachment list --json --no-analytics
```

```sh
proof liskov runtime-ssh attachment list --include-terminal --json --no-analytics
```

`--include-terminal` includes attachments that have already stopped. Use it
only when the user asked for those. `ATTACHMENT_ID` comes from the list.

```sh
proof liskov runtime-ssh attachment revoke ATTACHMENT_ID --json --no-analytics
```

Revoke cuts one attachment. It does not end the job. Unused tickets are
revoked. An established session drains. The customer's process, health
reporting, and schedule are unaffected. Run it only after an explicit yes.
Help does not list `--yes`. Do not invent it. There is no channel that cuts
an established relay. This skill does not end the job to hurry the drain.

## Verify and open

`--print-command` resolves and verifies without opening SSH. Help says
`--json` is most useful with `--print-command`.

Managed SSH rejects a run that omits `--identity`, including
`--print-command`. The path must be one the user already has. If they have
none, ask. Do not generate a key.

```sh
proof liskov ssh APP --identity IDENTITY_PATH --print-command --json --no-analytics
```

Opening a real shell is the same command without `--print-command`, only
when the user asked to open a shell. Pass the identity path they supplied.
Do not echo it.

```sh
proof liskov ssh APP --identity IDENTITY_PATH --deployment DEPLOYMENT --print-command --json --no-analytics
```

```sh
proof liskov ssh APP --identity IDENTITY_PATH --job JOB --print-command --json --no-analytics
```

`DEPLOYMENT` and `JOB` must be ids the previous command printed. The V5 page
says to select one when multiple jobs are ready. Do not invent either id.

Reviewed ssh flags: `--accept-host-key`, `--config`, `--deployment`,
`--identity`, `--job`, `--json`, `--organization`, `--print-command`,
`--slipway-url`, and global `--no-analytics`. No others.

## Host key

Help describes `--accept-host-key` as accepting and pinning a first-use
managed runtime host key without prompting. The V5 page says it also covers
the re-pin after a relaunched sandbox and never accepts any other mismatch.
This skill is narrower. Pass it only when the user explicitly accepts a new
key after the product told them the sandbox restarted, and the reply names
both fingerprints from the command output. Do not pass it for every
mismatch. Do not pass it for `RUNTIME_SSH_HOST_KEY_MISMATCH`.

```sh
proof liskov ssh APP --identity IDENTITY_PATH --accept-host-key --no-analytics
```

That command omits `--print-command` because a verify does not pin. It also
omits `--json`. `--json` never runs the host-key prompt. `--json` together
with `--accept-host-key` pins the key with no prompt. The accepting open
must omit `--json`. Do not use this command as the default open.

## Out of scope

Do not run these. Do not teach them.

| Topic | Rule |
| --- | --- |
| `runtime-ssh integration` | Customer-owned Tailscale setup. Do not teach it |
| V4 `ingress.ssh` authorized keys | Not this skill. Do not write that policy |
| `admin`, `custody`, `delete` | Out of scope |
| `application import`, `application publish` | Out of scope |
| `application lockbox`, `application devtools`, `application runtime-image` | Out of scope. `blackbox` is not a command in this plugin |
| `application execution`, `application hold`, `application run` | Out of scope |
| Ending the job | This skill does not end the job |

Pause or retire of one Application is liskov-operate, after its own yes.
Money figures are liskov-spend. Relay traffic draws on included log volume.
Do not invent a byte charge.
