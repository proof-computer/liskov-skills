# Limits

Use these while editing the manifest. They are not a validator. The only
validator is the command in [Command boundary](command-boundary.md).

Pages used here:

- [Variables](https://docs.proof.computer/liskov/configure/variables)
- [Secrets](https://docs.proof.computer/liskov/configure/secrets)
- [Spend limits](https://docs.proof.computer/liskov/configure/spend-limits)
- [Logging and diagnostics](https://docs.proof.computer/liskov/configure/logging-diagnostics)
- [Configuration and environment precedence](https://docs.proof.computer/liskov/reference/configuration-precedence)
- [Manifest reference](https://docs.proof.computer/liskov/reference/manifest-v5)

## Variables

Variables are named, non-secret strings. Do not use a variable for a
password, token, private key, or connection string that contains credentials.
A value you write is never a credential.

| Source | Write | Do not write |
| --- | --- | --- |
| `literal` | `name` and `value` they supplied | `required` or `default`. A literal accepts only `name` and `value`. |
| `managed` | `name`. `required` or `default` only when the user stated that field | A literal `value`. A credential in `default` |

A literal that includes `required` or `default` is `unknown_field`. Do not
add either field to a literal, even when the user asked. Tell them those
fields belong on `source: managed`.

The variables page says a managed variable may declare `required` and a public
`default`, and that a missing required value blocks configuration delivery.
Omitting managed `required` means the schema default, which is true. Do not
write `required: true` unless the user stated it.
Empty strings and the string `"0"` are values. Precedence for a managed
variable is the current Application-managed value if set, otherwise the
authored `default` if present, otherwise missing. An explicit empty string
must not be collapsed into missing. A literal uses the exact authored value.

Environment names match `[A-Z_][A-Z0-9_]{0,127}`. A name may be claimed only
once across variables and secret destinations. `variables` holds at most 64
entries. If the user asks for a collision or a 65th entry, stop and ask. Do
not drop another entry.

Do not copy a sample URL or a sample name from the variables page. Managed
values are set in the Console. This skill does not call the Console.

## Secrets

A secret object has `secretId` and `destination`. `destination.kind` is
`environment` with `name`, or `file` with an absolute `path`. The manifest
reference says `secretId` is 1–127 letters, digits, dot, underscore, or
hyphen. `required` defaults to true when absent. Write `required` only when
the user stated it. Explicit `false` is not the same document as omitting it.

A `value` field is invalid. If one is present, delete it. Do not copy the
rejected credential into the reply, the file, or a comment. Tell the user the
value is entered in the Console secret store, which this skill does not call.

The secrets page says the manifest contains identifiers and destinations
only. Never add plaintext, a ciphertext copied from another system, or a
secret in a variable `default`. Customer secrets work independently of Liskov
logging. Disabling logs does not disable secret grants. `secrets` holds at
most 64 entries.

Do not invent `secretId`, an environment name, or a file path. A relative
file path is not a V5 absolute destination. Ask. Do not invent an absolute
path.

## Spend

`deployment.spend.unit` is `service_credit_micros`. Every amount is USD
Service Credits in micros. The spend-limits page says 1,000,000 micros is
USD 1.00. Amounts are safety caps, not predicted prices.

The manifest reference says money values are decimal strings matching
`0|[1-9][0-9]{0,24}`. `perJob` is a decimal string, never a JSON number. No
decimal point and no leading zero except the single digit `0`. `"0"` is a
zero cap, not a missing cap. An empty string is not zero. Do not copy a
sample amount.

| Field | When to write it |
| --- | --- |
| `unit` | `service_credit_micros` when the user asked to write `deployment.spend` and the unit is missing or already that value. Do not convert another unit. |
| `perJob` | The amount the user stated, as a decimal string. |
| `rate.amount` | For `continuous` and `interval`, only when the user is writing that mode and has stated the amount. Same decimal string. |
| `rate.window` | Only the duration the user stated. |

The reference says `continuous` and `interval` require `rate`, and the
organization guard is not a fallback for an omitted authored rate. If the
user is writing that mode and has not stated the amount, ask and leave
`rate` absent. The reference says `rate.window` defaults to `30d`. Do not
invent `30d`. Omitting `window` is not the same document as writing `30d`.
Label that default in the reply instead of writing it.

Nothing is taken when a cap is saved. The reserve is a later hold of up to
the per-job cap for each job. The final charge is settled usage. This skill
does not reserve and does not publish.

If the user states USD rather than micros, convert only by the published
rule that 1,000,000 micros is USD 1.00, and write the integer micros as a
decimal string. If the conversion is not an integer number of micros, ask.
Do not round. If you cannot tell which unit they meant, ask. Do not pick a
sample.

## Logging, state, and schedule

`observability.logs.enabled` is the only logging switch. The manifest
reference says it is the only authored logging field. The logging page says
`enabled` is the only logging field needed for new manifests, and that
logging is optional and disabled by default unless policy enables it. Do not
add `runtimeDiagnostics`. If the file already has a field the user did not
mention, preserve it until a diagnostic says it is unknown, then remove it
only with the user's agreement.

| Authored logging | Meaning |
| --- | --- |
| `observability` omitted | Not the same document as logging on, and not the same document as explicit off. |
| `observability.logs.enabled` `true` | Liskov logging on. |
| `observability.logs.enabled` `false` | Liskov logging off. Not omitted. |

`state.mode` stays what the file already says. The only accepted V5 value is
`off`. The reference says that opts out of durable storage and does not pause
the Application. Do not invent another mode. If the user asks for durable
state, refuse and leave the file's mode unchanged. Do not add `ingress`.
Public ingress is not a V5 field.

Schedule `duration` is one integer plus `ms`, `s`, `m`, `h`, or `d`. Write
the duration the user stated. Do not invent a unit. Do not lengthen a
duration so a later publish will pass. The [authoring guide](https://docs.proof.computer/liskov/build/manifest-v5)
says the marketplace refuses a job registration below its 60-second provider
minimum. Report that. Do not rewrite it here. Publication limits are
liskov-publish.

## Repair

Repair only from a diagnostic the validate command just returned, and only
inside what the user asked to change. Deleting a secret `value`, or a
credential in a variable `value` or `default`, is required even before the
first validate. At most three validate runs. Stop when the same `code` and
`pointer` repeat.

| Diagnostic | Repair |
| --- | --- |
| `unknown_field` at a secret `value` | Delete `value`. Keep `secretId` and `destination`. Do not copy the credential. |
| `invalid_manifest` at `perJob` because it is a JSON number, and the user asked to change that spend | If that number is `0` or digits without a leading zero, write those digits as a decimal string. Do not change the amount. If it is not that integer, report it. Do not round. |
| `invalid_manifest` at `duration` for a bare number, and the user already stated the unit | Write that unit. Do not invent a unit. |
| `unknown_field` at `/ingress` | Report it. Remove `ingress` only when the user agrees. Do not add it under another name. |
| Any other diagnostic | Report it. Do not invent a replacement. Do not change `schemaVersion`. |

Do not rewrite `jobs`, `execution.mode`, or a cap to satisfy a launch limit.
Preserve a written `jobs` of `0` or of `3`. Report `jobs` `0` if validate
rejects it. Do not replace it. `jobs` greater than 2 can still return
`manifestValid` true. Say that count is above the first-public admission
maximum of 2 and is not a launch. `execution.mode` `interval` can validate
and still not launch: Liskov does not yet launch an interval Application.
Do not call either file ready to publish.
