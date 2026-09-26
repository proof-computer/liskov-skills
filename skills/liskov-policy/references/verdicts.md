# Verdicts

Keep these separate in the reply. One word does not imply the next.

| Verdict | Where it comes from | What it is not |
| --- | --- | --- |
| Contract valid | `manifestValid` true and `schemaVersion` `5` for `proof.liskov.application-manifest` | Not capability, entitlement, publication, or launch |
| `firstPublicReady` | True when `manifestValid` is true and `capabilityDiagnostics` is empty | Not admission and not launch. On `0.16.0` it was true for `jobs` `3`, `execution.mode` `interval`, `duration` `"0s"`, and `schemaVersion` `6` |
| Capability | [Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities) | A typed field can be schema-valid and still be release-gated or above the first-public ceiling |
| Entitlement | Not returned by local validate | Do not claim a plan or a seat |
| Publication readiness | Not returned by local validate | Do not claim the file can publish |
| Execution readiness | Not returned by local validate | Do not claim a job will launch or that spend was consented |

`firstPublicReady` is not customer launch approval. The capabilities page
remains the availability owner.

## Report these limits

Report a limit when the draft trips it. Do not rewrite a schema-valid choice
to avoid it unless the user asks.

- `deployment.jobs` schema range is 1–256. First-public admission maximum is
  2. `jobs` `3` validated with `firstPublicReady` true. Leave `3` in place
  and say it is above the first-public ceiling.
- `execution.mode` `interval` is schema-valid and release-gated. Liskov does
  not yet launch an interval Application, and no Service Credit reserve or
  job is created for that mode today. Leave `interval` in place when the user
  asked for it. Say it is not launch evidence.
- A duration shorter than `60s` can validate. The public guide says the
  marketplace refuses a job below its 60-second minimum. `duration` `"0s"`
  validated. Keep the user's duration and say it is not launch evidence.
- `access.ssh.provider.kind` `liskov_managed` is Preview, native image only,
  Developer or above. Local validate does not check the entitlement. Do not
  claim the seat.
- Public ingress, integrations, cohort, hooks, durable state other than
  `state.mode` `off`, placement allow/exclude/spread, non-managed SSH, and
  `acu_planck` are absent from V5. An unknown field is a diagnostic, not a
  reason to emit a later schema version.

## Out of scope versions

Do not deliver any of these as a successful draft. Do not translate them into
a V5 document unless the user asked for a new V5 draft from requirements they
stated. Do not write a V4 document.

| Version | What the reviewed CLI did | Skill result |
| --- | --- | --- |
| `4` | `schemaVersion` `4` and `invalid_manifest` at `/release/mode` (`source` is not a V4 release mode) | Out of scope. No V4 document is written. |
| `6` | `manifestValid` true, `schemaVersion` `6`, `firstPublicReady` true for a V5-shaped document | Out of scope, not success. |
| `7` and any other version | Version `7` returned `unknown_policy_schema` at `/schema` | Out of scope. `unknown_policy_schema` is a refusal, not a repair into V5. |

## What the reply covers

Name the choices that change cost, launch, or identity: release mode, runtime
kind, execution mode, duration and its unit, job count, spend cap and its
unit, secret references, `state.mode` `off` as an opt-out rather than a pause,
and whether logging is on, off, or omitted.

Name the evidence that is still missing. Repeat the unresolved requirements.
Point at the public authoring guide for a later publication step, without
running that step.

## Gaps the reply reports

These are limits of the reviewed surfaces. Report them. Do not invent a
command or a field to hide them.

1. Local validate can accept `schemaVersion` `6` and set `firstPublicReady`
   true. This skill still refuses version 6.
2. There is no local explain command for an unpublished file.
3. The released validate command reads JSON only.
4. `firstPublicReady` does not encode the two-job first-public ceiling, the
   60-second marketplace minimum, or the interval launch gate.
5. The public build guide still names plugin `0.14.0`. The checked plugin is
   `0.16.0`.
