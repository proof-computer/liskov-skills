# Limits

Read this with the [Command boundary](command-boundary.md). It is not a second
workflow. This skill is read only. For each record, say what it proves and
what it does not prove. Quote the JSON. Do not relabel a field you did not see.

## What each record proves

| Record | Proves | Does not prove |
| --- | --- | --- |
| Source binding | The repository, ref, workflow, and manifest path the organization admin bound, when those fields are in the JSON | That those bytes are the process that booted. That the binding is safe. A missing binding: `source_binding_not_found` means not bound yet |
| Artifact pin | A digest proves bytes. The proof-chain page says the CID and digest identify bytes | That the code is safe. That a runtime instance booted. GitHub or Marketplace provenance is a separate fact. Neither alone proves the code is safe |
| Policy explain | The published effective policy explanation. Help does not recompute policy, spend, or eligibility | A local unpublished file. A draft that was never published. A launch |
| Deployment status | Liskov's attempt: the deployment record the command returns | That the attempt is a chain-owned job, a runtime instance, or runtime readiness |
| Plans | The execution plans the command returns, including a policy digest when that field is present | That a job was registered, that a runtime instance booted, or that a cap was charged |
| Status | The status JSON. Help also returns the canonical retained V5 policy explanation | Bytes on a processor. Attestation beyond fields in the JSON. A launch |

A job is the time-boxed network registration. A runtime instance is one
process boot. A process restart is a new runtime-instance id, not the same
boot. Chain assignment is not runtime readiness. The attestation page says
assignment supports that a processor accepted the job and is not runtime
readiness. The deployments page says the same about processor assignment: the
job can still be waiting to boot, fetch configuration, obtain managed-secret
grants, or report health.

Do not assert a policy schema version the JSON did not return. The proof-chain
page says the effective policy is server-materialized and immutable and is not
the source manifest. Help calls explain the retained V5 explanation. Quote the
returned fields rather than forcing those two sentences into one version.

Sources: [Inspect the proof chain](https://docs.proof.computer/liskov/operate/proof-chain),
[Attestation and the proof chain](https://docs.proof.computer/liskov/concepts/attestation),
and [Deployments, jobs, and timelines](https://docs.proof.computer/liskov/operate/deployments-jobs).

## Attestation stays inside the JSON

Attestation is a signed statement about specific facts. Do not promote one
field into a universal badge.

| Evidence in the JSON | You may say | You may not say |
| --- | --- | --- |
| A digest or CID | Those bytes were identified | The code is secure, or every operation succeeded |
| Build provenance fields | An allowed workflow reported those bytes, when the fields say that | The code was reviewed and found safe |
| A processor id on a deployment or job | That identifier was recorded | The processor is attested, unless an attestation field is present and you quote it |
| Assignment or registration | A processor accepted the time-boxed job, when the JSON says so | The runtime is ready |
| Signed runtime fields | Quote the Application, policy, deployment, job, processor, and runtime-instance ids that are present | Facts the active record does not bind |
| No record | Not observed through this channel | It did not happen |

Missing evidence means not observed through this channel. Do not fill the gap.
A stale last-contact time is stale. Do not call it fresh.

## Processors

There is no processor list or search command. Do not invent one. Do not claim
fleet-wide search.

The Console page for the organization's own processor history is
[Inspect a processor your organization used](https://docs.proof.computer/liskov/operate/processors).
Open it only from a processor id a deployment or execution already returned.
The page does not provide a processor directory or search. It does not expose
fleet inventory. Opening it does not create a deployment, submit a chain
transaction, reserve USD Service Credits, or add a final charge.

| Scope the page labels | How to read it |
| --- | --- |
| your org | That organization's deployments and runtime contact. A handful of runs is history, not a reliability score |
| whole fleet | A chain-published fact or a register result. Enterprise adds register intelligence. It is not a search box |

Do not merge those scopes. An unknown processor and a processor this
organization has never used return the same not-found result. Do not probe
ids. Do not replace a processor id with one from another organization. Redaction
on a non-Enterprise plan is not the same as data that was not reported. Do not
call either state a failed attestation unless the JSON says so.

Chain-published hardware is a set of facts with one observation time.
`storageBytes` on that page is free space at that observation, not device
capacity. Quote it only when the record shows it. Register liveness is not the
runtime heartbeat.

## Money and mutation

A cap in the plans JSON is authority, not a settled charge. Do not call it a
reserve or a final charge unless that field says so. Spend wording belongs to
liskov-spend. This skill does not publish and does not run SSH.
