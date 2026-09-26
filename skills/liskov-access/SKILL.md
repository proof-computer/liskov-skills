---
name: liskov-access
description: Operate managed Runtime SSH for one retained V5 Application. Use when asked to register an operator key, withdraw a key, revoke one attachment, or open a shell. Preview on Developer and above, native image only. Does not generate a key, teach Tailscale, or end the job.
---

# Use managed Runtime SSH

This skill registers keys and opens managed Runtime SSH for a retained V5
Application. It is not public ingress. It does not change workload health,
replacement, schedule, or spend. It does not end the job.

Availability, and do not widen it: Preview on Developer and above, native
image only, provider `liskov_managed`. Customer-owned Tailscale is a separate
preview. One sentence in [Limits](references/limits.md) points at the public
page and stops. Do not teach `runtime-ssh integration`.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator. Manifest drafting is liskov-policy.

## 1. Register before the first launch

Register the operator key before the first launch. V5 snapshots the
organization registry into the next attachment. A key added later does not
enter an attachment that already exists. An empty registry makes attachment
preparation fail closed, and a job that already started against an empty
registry keeps a degraded access block for that whole run.

The public key comes from a path or value the user already has.
Otherwise do not generate a key.
Do not write a private key into the repo or the reply. If they paste a
private key, do not store it and do not repeat it.
`--identity` is a filesystem path the user supplies. Do not echo file
contents.

## 2. Reads

List keys, withdrawals, and attachments before changing them. `KEY_ID`,
`WITHDRAWAL_ID`, `ATTACHMENT_ID`, and `FINGERPRINT` come from those JSON
results or from the user. Do not invent a key, a host key, or an
organization.

```sh
proof liskov runtime-ssh operator-key list --json --no-analytics
```

```sh
proof liskov runtime-ssh withdrawn-key list --json --no-analytics
```

```sh
proof liskov runtime-ssh attachment list --json --no-analytics
```

## 3. Mutations wait for a yes

`operator-key remove` withdraws access. Run it only after an explicit yes.
`withdrawn-key add` withdraws. `withdrawn-key remove` lifts a withdrawal and
does not by itself re-register a key. `attachment revoke` cuts one
attachment. It does not end the job. Unused tickets are revoked. An
established session drains. Run revoke only after an explicit yes.

Help for `operator-key add` has no `--yes`. Do not invent that flag. Add
only when the user asked to register that key, with `--name` and exactly one
of `--public-key-file` or `--identity`.

## 4. Verify, then open only if asked

This verifies without opening a session and without minting a ticket.
Managed SSH, including `--print-command`, requires `--identity` with a path
the user already has. If they have none, ask. Do not generate a key. Do not
echo the file.

```sh
proof liskov ssh APP --identity IDENTITY_PATH --print-command --json --no-analytics
```

`APP` is the Application id the user gave. If more than one job is ready,
add `--deployment` or `--job` only with an id the command printed.

Opening a real shell omits `--print-command`. Do that only when the user
asked to open a shell. Do not pass `--json` on that open. Help says `--json`
is most useful with `--print-command`, and the public procedure leaves it
off the open. Relay traffic counts against the plan's included log volume
and is charged at the log overage rate above it.

## 5. Host key pin

`--accept-host-key` accepts a host-key pin. Use it only when the user
explicitly accepts a new key after the product told them the sandbox
restarted, and the reply names both fingerprints from the command output.
Do not tell the user to pass it for every mismatch. `RUNTIME_SSH_HOST_KEY_MISMATCH`
stops. Do not delete the known-hosts file.

## 6. Scope

`--organization` or `LISKOV_ORGANIZATION` scopes one command. Do not run
`organization use` unless the user asked to change the session default.

A missing live agent run is not a pass.
