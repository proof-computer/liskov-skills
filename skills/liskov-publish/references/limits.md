# Limits

Use these before any publish command. They are not a second validator. If a
check fails, stop and report it. Do not rewrite the file to duck the limit.
`firstPublicReady` is not admission and not launch.

Availability is the [capabilities page](https://docs.proof.computer/liskov/reference/capabilities).
Field shape is the [manifest reference](https://docs.proof.computer/liskov/reference/manifest-v5).
The authoring procedure is [Author a retained Application Manifest V5](https://docs.proof.computer/liskov/build/manifest-v5).

## Stop before publish

| Check | Stop when | What the pages say |
| --- | --- | --- |
| Jobs | The file writes `deployment.jobs` greater than 2 | Capabilities: retained V5 is v1 at one or two jobs, and higher schema ceilings are not availability. The manifest reference: first-public admission maximum 2. The authoring guide: the first public capability and entitlement limit is exactly 2, and three or more fails before spend. |
| Interval | `execution.mode` is `interval` | Capabilities: fixed-interval execution is release-gated v1. The schema accepts `every` and an optional `until`, but no interval run has been observed in production and Liskov does not yet launch an interval Application: it stops before any Service Credit reserve or job is created. |
| Duration | The authored duration is shorter than 60 seconds | Capabilities: job schedule v1 requires `durationMs >= 60000`. The authoring guide: the marketplace refuses a job registration below its 60-second provider minimum. Local schema validation alone does not prove that a schedule can launch. |

Also stop when the capabilities page marks a feature the document uses as
not launched, including Liskov-hosted ingress, which that page marks Not v1.
Do not publish that document. Do not delete the field here. Name liskov-policy
if the user wants the file changed.

Omitted `deployment.jobs` is the reference default of 1, which is inside the
ceiling. Do not write `1` unless the user asked. Do not lower a written `3`
to `2`.

| Duration | Under 60 seconds |
| --- | --- |
| `Ns` with N less than 60, or `Nms` with N less than 60000 | Yes. Stop. |
| `0m`, `0h`, or `0d` | Yes. Stop. |
| `60s`, `60000ms`, `1m`, or a longer single-unit duration | No. This row is not the stop. |
| Bare, compound, or unknown unit | The document is not valid. Stop and name liskov-policy. Do not repair it. |

`60s` meets the minimum. It is still not a default. Use the duration the
file already has.

## Release evidence

Help: a source release carries `--binding-revision`, `--revocation-epoch`,
`--source-ref`, `--source-commit`, and `--workflow-identity` from the
attested build. A pinned release must use an `--artifact-digest` equal to
`release.artifact.digest` and must not send those build-evidence flags.

The manifest reference says a pinned artifact digest has the form `sha256:`
plus 64 lowercase hex digits. Copy that field. Do not type a sample digest.
Do not pass the contract RC named on the capabilities page as
`--artifact-digest`. `authoredDigest` and `releaseIntentDigest` from validate
are not the artifact digest.

Do not assume the authoring guide's sample pointer version, binding revision,
or revocation epoch. If the user has not supplied the pointer version, stop.
The guide's example is not an observation.

## Spend is the consent gate

`deployment.spend.unit` is `service_credit_micros`: USD Service Credits in
micros. The [spend-limits page](https://docs.proof.computer/liskov/configure/spend-limits)
says 1,000,000 micros is USD 1.00. Amounts are
non-negative decimal strings, never JSON numbers. The per-job cap, the
reserve, and the final charge are three different amounts. Liskov does not
show a separate estimate of what a run will cost before launch.

Show the cap that is already in the file. Do not copy a sample amount and do
not raise or lower it in this skill. Nothing is taken when a cap is saved.
The consented publish is what begins a spend-bearing deployment. Until that
yes, this skill does not spend.

`--yes` and `--dry-run` are mutually exclusive. See
[Command boundary](command-boundary.md).
