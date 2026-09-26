---
name: liskov-workload
description: Decide whether a program fits the Liskov phone fleet before anyone writes a manifest. Use when asked if a check, probe, server, batch, or schedule can run on this fleet. Does not write a manifest, does not publish, and runs no proof command.
---

# Decide whether a program fits this fleet

This skill decides fit before anyone writes a manifest. This skill does not write a manifest and does not publish.
It writes no workflow and runs no `proof` command. It does not deploy, reserve, or charge.

The fleet is ARM, residential, memory-constrained, intermittently reachable,
and outbound-only. One job is one phone. Public parallelism above 1 is not a
recipe. There is no public inbound HTTP product. V5 durable state accepts only
`state.mode` `off`.

Manifest work, when a later skill does it, is schema
`proof.liskov.application-manifest` at `schemaVersion` 5. Do not author version
4. Do not write schema `proof.liskov.application-policy`.

Before deciding, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a validator.

## 1. Ask

Ask for the result the job returns, how that result leaves the phone, and any
schedule or cap the user already stated.

Do not pick `once` or a duration. Do not invent an application id, a digest, a
price, a spend cap, a schedule, a commit, a ref, or budget consent. Keep an
explicit zero or empty value as the user wrote it. Leave every unknown absent
and list it as unresolved.

## 2. Judge fit

A fit is one phone doing outbound work.

| Shape | Decision |
| --- | --- |
| Scheduled check | Fits when the result leaves by outbound HTTP or a log line. |
| Outbound probe | Fits. |
| Fan-out fetch that returns a result | Fits on one phone. Not one job per request. |
| Batch item | Fits when the output leaves by outbound HTTP or a log line. |
| Inbound HTTP or websocket server | Does not fit. |
| Shared disk | Does not fit. |
| GPU training or tensor-parallel serving | Does not fit. |
| Program that needs peers on the fleet | Does not fit. |

There is no public inbound product. Do not design a listen socket, a public
hostname, or a websocket server.

Do not raise the job count to split work across phones. Two jobs are not a
parallel recipe. Do not shop for a processor. Open-market placement chooses
the processor. There is no processor catalog.

Interval execution can be schema-valid and still not launch. Do not describe
it as a launch, a reserve, or a final charge. Cron, calendar, and local-time
schedules are not a schedule this skill can assign. Record the user's words.
Do not translate "every morning" into a duration or a cron expression.

`state.mode` other than `off` does not fit. Ephemeral storage on one phone is
not a shared disk. Do not promise durable state, a volume, or a peer.

The capabilities page does not list a GPU or tensor-parallel product. Do not
treat that silence as a hidden product. Those programs do not fit.

## 3. What the pages support

Quote only the pages below. Do not add a rule they do not state.

[Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities)
lists Liskov-hosted HTTP/SSH ingress as not v1, open-market processor
selection as v1, and manager, static, placement-group, and topology selection
as internal. It says retained V5 is v1 at one or two jobs, and that higher
schema ceilings are not availability. Fixed-interval execution is release-gated:
the schema accepts `every` and an optional `until`, but no interval run has
been observed in production and Liskov does not yet launch an interval
Application. It stops before any Service Credit reserve or job is created.
Cron, calendar, and local-time schedules are not v1.

[Liskov and Acurast](https://docs.proof.computer/liskov/concepts/product-boundaries)
says: "Liskov does not execute your process on its own servers and does not
provide a general hosted HTTP or SSH ingress product in v1." Processors are
phones that accept time-boxed jobs. A curated WebView or Tunnel path belongs
to that offering, not to every workload.

[Runtime resources and outbound networking](https://docs.proof.computer/liskov/configure/resources-networking)
says: "The public v1 repository path can call allowlisted public endpoints over
outbound networking. It does not receive a stable public IP, custom hostname,
Liskov HTTP endpoint, or Liskov SSH endpoint." Storage for the job is
ephemeral. Processor identity and assignment can change at renewal. Store
durable results outside the processor.

[Retained Application Manifest V5](https://docs.proof.computer/liskov/reference/manifest-v5)
says state is required and has only mode off, which opts out of durable
storage. Public ingress, cohort discovery, and durable volumes are absent.
Omitting exact processor selection uses open-market selection. This skill
still does not write that file.

The pages fetched here do not say the words ARM or residential. Those two
words are this skill's fleet rule, not a sentence copied from those pages.

## 4. Say what happens next

Point the user at `liskov-policy` to draft the manifest and `liskov-runtime`
to write the job. Do not draft either one here. Do not publish.

A log line still needs `liskov-policy` to own logging in the manifest and
`liskov-runtime` to emit it. Do not set that field here.

List every unresolved fact. If the result, the way it leaves the phone, or a
schedule the user thinks they stated is missing, the decision is incomplete.
Do not fill the gap.

These files do not record a live agent run. Note: a missing live run is not a pass.
