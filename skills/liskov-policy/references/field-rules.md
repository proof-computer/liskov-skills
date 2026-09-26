# Field rules

Use these while writing the V5 manifest. They are not a validator. The only
validator is the drafting command in [Command boundary](command-boundary.md).
If the user asks for a nested field this page does not define, use the
[public V5 reference](https://docs.proof.computer/liskov/reference/manifest-v5).
If that reference does not list the field, it is absent. An unknown field is
a diagnostic, not a reason to raise `schemaVersion`.

Unknown fields fail closed. Duplicate JSON keys fail. The reviewed CLI rejects
a duplicate `applicationId` with `invalid_manifest` and a message that one
document must state each key once. If two values disagree, stop and ask. Do
not keep the last key.

## Required shape

A complete draft has `schema`, `schemaVersion`, `applicationId`, `release`,
`runtime`, `execution`, `deployment`, and `state`. Write `schema` and
`schemaVersion` `5` for a new V5 draft the user asked for. Leave every other
missing required fact absent and list it as unresolved.

| User fact | Document | If missing |
| --- | --- | --- |
| Application slug | `applicationId`, pattern `^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$` | Leave absent. Incomplete. Never invent a slug. `hello-liskov` belongs only to the sample fixture. |
| New versus existing | Not a manifest field | Do not call `application create`. Say creation is a separate product step. |
| Source release | `release.mode` `source` and no other release fields | Repository, ref, workflow, and manifest path stay out of the file. They are the server source binding. |
| Pinned artifact | `release.mode` `pinned` and `release.artifact.digest` of the form `sha256:` plus 64 lowercase hex digits | If the user has no digest, leave the release incomplete. Never invent a digest. |
| JavaScript | `runtime.kind` `javascript`, `engine` `nodejs` when they asked for Node, `entrypoint.file` relative to the artifact | Ask for the entrypoint file. The sample uses `bundle.js`. Do not copy it unless they named that file. The file must not begin with `/` and must not contain a `..` segment. |
| Native image | `runtime.kind` `native_image` and the image and entrypoint they name | Do not invent a catalogue image. The public reference names `image.catalog`, `image.name`, `image.version`, `entrypoint.executable`, and `entrypoint.args`. Use only values the user supplied. |
| Once, continuous, or interval | `execution.mode` | If they were ambiguous, including a schedule described only as "sometimes", ask. Do not pick `once` for them. Leave `execution.mode` absent. For `interval`, write `every` only as a duration the user stated. Do not invent one. |
| Paid window | `deployment.schedule.duration`, one integer and `ms`, `s`, `m`, `h`, or `d` | Ask. Do not copy the sample's `60s`. |
| Job count | `deployment.jobs` | Omit unless they gave a count. See explicit values below. |
| Spend cap | `deployment.spend.unit` is `service_credit_micros`. `perJob` is a decimal string. `rate` is required for `continuous` and `interval`. | Ask for the cap they want. Never copy the sample's `"50000"`. `"0"` is a real zero cap, not a missing cap. |
| Variables | `configuration.variables` | Literal `value` is part of the document. Managed variables are names, not values. |
| Secrets | `configuration.secrets[].secretId` plus `destination` | A reference only. Never a credential value. |
| Logging | `observability.logs.enabled` | Omit unless they chose. |
| Durable state | `state.mode` | The only accepted value is `off`. Write it only after the user accepts that V5 opt-out. Say that this is the explicit opt-out, not a pause. |

`deployment.spend.perJob` is an integer written as a decimal string: `0`, or
digits without a leading zero, at most 25 digits. No decimal point and never
a JSON number. For `continuous`
and `interval`, the public reference also requires `rate.amount` (the same
decimal string). `rate.window` is a duration and is optional. Do not write
`30d` unless the user stated that window. Omitting `window` is not the same
document as writing the guide's default. Label the default instead of
inventing it.

`metadata` is optional. `metadata.description` is at most 500 characters.
`metadata.labels` holds at most 32 labels matching
`[a-z0-9][a-z0-9._-]{0,62}`. Metadata does not enter the effective policy.

Secret `destination.kind` is `environment` with `name`, or `file` with an
absolute `path`. Environment names match `[A-Z_][A-Z0-9_]{0,127}`. A name may
be claimed only once across variables and secret destinations. `required`
defaults to true when absent. A secret object rejects a `value` field with
`unknown_field` at `/configuration/secrets/0/value`.

`debug` is reserved for diagnostic fixtures, not an ordinary customer draft.
Do not add it unless the user asked for that fixture hold.

## Explicit zero and empty values

On plugin `0.16.0`, distinct written forms validated as distinct documents.
Preserve the form the user wrote.

| Written form | Meaning to keep |
| --- | --- |
| `deployment.jobs` omitted | Schema default applies on the owner side. Not the same document as an explicit count. |
| `deployment.jobs` `null` | Explicit null. Not the same document as omitted. |
| `deployment.jobs` `1` | Explicit one. Not the same document as omitted. |
| `deployment.jobs` `0` | Invalid. Diagnostic `invalid_manifest` at `/deployment/jobs`: a job count must be between 1 and 256. Do not rewrite `0` to `null` or delete it. |
| `perJob` `"0"` | Valid exact zero. Not a missing price. |
| `perJob` `""` | Invalid. Empty is not zero. |
| `metadata.labels` `[]` | Valid empty list. Not omitted labels. |
| `metadata.labels` `null` | Not the same document as `[]` or omitted. |
| `metadata.description` `""` | Valid empty string. Not omitted and not null. |
| `configuration` `{}` | Not the same document as omitted configuration. |
| `configuration.variables` `[]` and `secrets` `[]` | Not the same document as omitted configuration or as `configuration` `{}`. |
| `observability` omitted | Not the same document as logging on. |
| `observability.logs.enabled` `true` | Logging on. |
| `observability.logs.enabled` `false` | Logging off. Not omitted. |
| secret `required` omitted | Schema says absent means required. The authored digest still differs from explicit `true`. |
| secret `required` `true` | Keep the explicit true. |
| secret `required` `false` | The job may start without that secret. Do not drop the field. Dropping it changes the meaning toward required. |
| literal variable `value` `""` | Valid empty string. Keep it. |
| `state` `{}` | Invalid. `invalid_manifest` at `/state`, missing `mode`. Do not invent `off` unless the user accepted the V5 opt-out. |
| `duration` `"60"` | Invalid. `invalid_manifest` at `/deployment/schedule/duration`. Repair only when the user has already said the unit. |

`jobs` `0`, `perJob` `"0"`, `labels` `[]`, `logs.enabled` `false`, secret
`required` `false`, and a literal `value` `""` stay byte for byte when the
user wrote them. Only `jobs` `0` is the invalid one. Report it. Do not "fix"
the others.

## Repair

Repair only from a diagnostic the drafting command just returned, and only
inside what the user asked for. At most three validate runs. Stop when the
same `code` and `pointer` repeat.

| Diagnostic | Repair |
| --- | --- |
| `invalid_manifest` at `/deployment/schedule/duration` for a bare number such as `"60"`, and the user already stated the unit | Write that unit. Sixty seconds becomes `"60s"`. Do not invent a unit. |
| `unknown_field` at `/ingress` | Public ingress is not in V5. Report it. Remove `ingress` only when the user agrees to drop that field. Do not add it under another name and do not change `schemaVersion`. |
| `invalid_manifest` naming missing `applicationId`, pointer `""` | Leave the id absent. Ask. Do not invent one. |
| `unknown_field` at `/configuration/secrets/0/value` | Delete `value`. Keep `secretId` and `destination`. Do not copy the rejected credential into the reply, the file, or a comment. Tell the user the value stays in the product's secret store, which this skill does not call. |
| `invalid_manifest` at `/deployment/jobs` for `0` | Leave the zero. Report it. |
| `schemaVersion` other than `5`, including a validate result with `manifestValid` true | Out of scope. Do not repair it into version 5 unless the user asked for a new V5 draft from requirements they stated. |

An existing draft keeps every value the user did not ask to change. A request
to turn logging off changes `observability.logs.enabled` to `false` and does
not rewrite `metadata.description` or any other field.

## Absent from V5

Do not emit these, and do not smuggle them in under a different name:

- public or provider-owned ingress
- provider integration blocks
- cohort membership and discovery
- join/drain hooks and health probes
- durable volumes, snapshot, restore, or `state.mode` other than `off`
- placement allow/exclude, diversity, spread, or distribution
- a non-managed SSH provider
- `acu_planck` or any self-custody spend unit

Capability minimums and exact `processorSelection` are in the public
reference. Write a minimum or a processor id only when the user supplied it.
Do not invent a processor id. Placement allow and exclude are still absent.
