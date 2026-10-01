---
name: liskov-proof
description: "Answer whether the running Liskov Application is the code the user thinks it is. Read-only source binding, artifact pins, published policy explanation, deployment status, plans, and status. Does not publish, spend, or SSH."
---

# Check the running code

This skill is read only. It answers "is this the code I think is running?" for
one Application id the user gave. It does not publish, reserve, charge, pause,
or SSH.

A digest proves bytes. It does not prove the workload is safe or that a
runtime instance booted. A source binding proves which repository, ref,
workflow, and manifest path the organization admin bound. A policy explanation
is the published effective policy, not a local unpublished file. A deployment
is Liskov's attempt. A job is the time-boxed network registration. A runtime
instance is one process boot. Chain assignment is not runtime readiness.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. Use their Application id

Run these reads only for an Application id the user gave. If they did not give
one, ask. Do not pick one from a list. Do not invent an application id, a
deployment id, a job id, a digest, or a processor id.

Run whoami when the organization is in question. That read separates the
effective organization from the persistent session organization.
`--organization` or `LISKOV_ORGANIZATION` scopes one command. Run
`organization use` only when the user asked to change the session default.

## 2. Read the chain

Run the reads in the command boundary. For each result, say what that record
proves and what it does not prove. Use the table in
[Limits](references/limits.md). Quote the JSON fields the command returned. Do
not relabel a field you did not see.

Processor identity in that evidence is not a catalog. There is no processor
list or search command. Do not invent one. The organization's own processor
history is the Console record described in
[Inspect a processor your organization used](https://docs.proof.computer/liskov/operate/processors).
That page is not fleet-wide search.

## 3. Stop

Do not claim a processor is attested beyond fields present in the JSON. Do not
run SSH. Do not publish. Do not treat a local unpublished file as the
explanation. Spend wording belongs to liskov-spend. Daily pause, resume, and
retire belong to liskov-operate. One symptom to one next action belongs to
liskov-diagnose. Manifest drafting belongs to liskov-policy.

A missing live agent run is not a pass.
