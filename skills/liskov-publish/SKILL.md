---
name: liskov-publish
description: Publish one retained V5 policy version for an Application manifest the user pointed at (schema proof.liskov.application-manifest, schemaVersion 5). Use when asked to preview or publish that version after local validation. It does not spend until the user confirms, and it does not repair the manifest.
---

# Publish one retained V5 policy version

This skill publishes one retained V5 policy version. Publication is the consent
gate. Until the user has said to publish, this skill does not spend. Showing
a command does not spend.

The consented publish is the spend-bearing step. The [authoring guide](https://docs.proof.computer/liskov/build/manifest-v5)
says publishing commits an immutable effective policy and begins a spend-bearing
deployment under the document's `spend`. No other command in this skill spends.
This skill does not repair a manifest, create an Application, bind source, or
attest. Drafting is liskov-policy. Attest is liskov-release. Reading a
published explanation is liskov-proof.

V5 only. Do not author version 4. Do not write
`proof.liskov.application-policy`. `application import` and `application
publish` are version 4 and out of scope.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow.

## 1. Validate before any server call

The user must point at the local file. If they did not, ask. Do not choose a
path for them.

Before any server call, run:

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

Stop unless all of these hold:

- validate stdout shows `manifestValid` true
- validate stdout shows `schemaVersion` 5
- the file's `schema` is `proof.liskov.application-manifest`

If they do not, stop and name liskov-policy. Do not repair the manifest in
this skill. Help text that says the command accepts v4 or retained V5 is not
this skill's support list.

`schemaVersion` 6 can still come back `manifestValid` true. That result is
out of scope. `firstPublicReady` is not admission and not launch. Do not
publish because that field is true.

Stdout of a completed run is one JSON object. Parsers use that object. If
`proof` is missing, exits before JSON, or returns no JSON object, say the
owner validator did not run. Do not publish. Do not build a replacement
checker.

## 2. Launched surface

Read [Limits](references/limits.md). If the document is outside the launched
surface, stop and report the limit. Do not rewrite the file to duck the
limit. Do not call publish, including `--dry-run`.

In particular, stop when `deployment.jobs` is greater than 2, when
`execution.mode` is `interval`, or when the schedule duration is under 60
seconds. Omitted `jobs` uses the reference default of 1. Do not write `1`
into the file.

## 3. Evidence

`APP_REF` must match the file's `applicationId`. If the user named a different
id, stop. Do not invent an id.

If a value is missing, do not invent it. Do not type a sample digest. Do not
assume a pointer version, a binding revision, a revocation epoch, a ref, a
commit, or a workflow identity.

| Release | Pass | Do not pass |
| --- | --- | --- |
| `release.mode` `source` | `--artifact-digest` from the attested build the user supplied, plus `--binding-revision`, `--revocation-epoch`, `--source-ref`, `--source-commit`, and `--workflow-identity` from that same build | A digest copied from a guide, from `authoredDigest`, or from `releaseIntentDigest` |
| `release.mode` `pinned` | `--artifact-digest` equal to the file's `release.artifact.digest` | The five build-evidence flags. Help says they are refused. |

Quote a digest in the reply only by copying it from the file, from validate
stdout just run, or from the attested digest the user already supplied.
`authoredDigest` and `releaseIntentDigest` are not the artifact digest.

There is no local explain. `application policy explain` reads a published
Application and is not this skill's preview. Do not run it here. That is
liskov-proof.

## 4. Show the gate

Before `--yes`, show the user all of these, taken from the file or from
values they already supplied:

- the schedule duration
- the spend cap (`perJob`, and `rate` when the file has one), in USD Service
  Credits
- the artifact digest
- the pointer version

The [spend-limits page](https://docs.proof.computer/liskov/configure/spend-limits)
says the per-job cap is authority you authored, the reserve is a temporary
hold of up to that cap for each job when a run starts, and the final charge
is settled usage. The cap is not a quote. Nothing is taken when the cap is
saved. This skill does not read a balance and does not invent one.

`--dry-run` only when the user asked to preview. `--yes` only when the user,
after you showed the schedule, the spend cap, the digest, and the pointer
version, said to publish. An earlier "publish it" does not replace that yes.

## 5. Publish or preview

`--yes` and `--dry-run` are mutually exclusive. Do not send both. Do not run
the command with neither. Do not wait on an interactive prompt.

Source, after the yes:

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --binding-revision REVISION --revocation-epoch EPOCH --source-ref REF --source-commit COMMIT --workflow-identity IDENTITY --expected-pointer-version POINTER --yes --json --no-analytics
```

Pinned, after the yes:

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --expected-pointer-version POINTER --yes --json --no-analytics
```

Preview, only when the user asked, uses the same evidence flags and replaces
`--yes` with `--dry-run`. `--dry-run` is still a server call. Help says it
previews without committing policy, pointer, or wakeup.

Pinned preview:

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --expected-pointer-version POINTER --dry-run --json --no-analytics
```

Source preview:

```sh
proof liskov application policy publish APP_REF --file PATH --artifact-digest DIGEST --binding-revision REVISION --revocation-epoch EPOCH --source-ref REF --source-commit COMMIT --workflow-identity IDENTITY --expected-pointer-version POINTER --dry-run --json --no-analytics
```

`--paused` requires `--reason`. Pass both only when the user asked to leave
the published Application paused and supplied the reason. Do not invent a
reason. Do not send one without the other. The reason must be 1 to 500
characters. If it is not, ask. Do not truncate it.
Put them with `--yes`, or with `--dry-run` when they asked to preview that
paused publication, never with both.

Add `--organization ORG_ID` only when the user named one organization for
this command. Run `organization use` only when they asked to change the
session default. Read the session with `whoami` only after validation, the
launch check, and the evidence check all pass, and before the mutation, so
the reply names the effective organization. Do not call `whoami` when
validation failed, the document is outside the launched surface, or the
required evidence is missing.
