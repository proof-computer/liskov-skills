---
name: liskov-configure
description: Edit managed variables, secret references, logging, schedule, and spend caps on an existing local V5 manifest the user pointed at (schema proof.liskov.application-manifest, schemaVersion 5). Use when asked to change that configuration. It does not publish, create, bind, or spend.
---

# Edit local V5 configuration

This skill edits configuration on one existing local V5 manifest the user
pointed at: managed variables, secret references, Liskov logging, schedule,
and spend caps. It then validates that file. It does not publish, create an
Application, bind source, or spend. It does not call any command except
validate.

Drafting a new manifest is liskov-policy. Publication is liskov-publish.
Creating and binding are liskov-bind.

V5 only. Do not author version 4. Do not write
`proof.liskov.application-policy`. Do not add `ingress`.

Before editing, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow.

## 1. Requirements

The user must point at an existing local file. If they did not, ask. Do not
choose `.liskov/application-manifest.json` for them.

Read the file. Continue only when it is one JSON object whose `schema` is
`proof.liskov.application-manifest` and whose `schemaVersion` is 5. Otherwise
stop and name liskov-policy. Do not convert version 4 or version 6 into
version 5. If two values for the same JSON key disagree, stop and ask. Do
not keep the last key.

If a value is missing, do not invent it. Write a literal only when the user
supplied that literal. A value you write is never a credential: a password,
token, private key, or connection string that contains credentials is refused.

## 2. Edit

Preserve every field the user did not ask to change, including an empty
string, `"0"`, `false`, `[]`, and explicit null. Show the diff in the reply.
Edit only the file they pointed at.

| Change | Write | Do not write |
| --- | --- | --- |
| Managed variable | The name they stated. `source` `managed`. `required` or `default` only when they stated them. | A literal value. A sample URL. A credential in `default`. |
| Literal variable | `source` `literal`, `name`, and the value they supplied, including `""` and `"0"`. | `required` or `default`. A value they did not supply. A credential. |
| Secret | `secretId` and `destination` (`environment` with `name`, or `file` with an absolute path), both from the user. | A `value` field. The credential itself. |
| Logging | `observability.logs.enabled` true or false, as they asked. | Any other logging field. Omitting `observability` to mean off. |
| Schedule | The duration they stated, one integer and a unit. | A unit they did not state. A longer duration that ducks a launch limit. |
| Spend | `unit` `service_credit_micros` when you write `deployment.spend`. `perJob` is a decimal string, never a JSON number. | A sample amount. A JSON number. `30d` unless they stated that window. |

`false` is off, and it is not the same document as omitting `observability`.
If they disable logging and the object is already present, set `enabled` to
`false`. If `observability` is absent, ask whether they want explicit `false`
or to leave it omitted. Do not decide for them.

`state.mode` stays what the file already says. The only accepted V5 value is
`off`. Do not invent another mode. Do not add `ingress`.

If a secret object has `value`, delete that field. Do not copy the rejected
credential into the reply, the file, or a comment. Tell the user the value is
entered in the Console secret store, which this skill does not call. The same
deletion applies to a credential sitting in a variable `value` or `default`:
remove it without copying it, and use a secret reference instead.

Managed variable values are names in the manifest. The variables page says
the `vars` commands are not in a released package. Set a non-secret managed
value in the Console. Do not run `application vars set`. Empty string and
`"0"` are real values. Do not drop them.

`"0"` on `perJob` is a zero cap, not a missing cap. For `continuous` and
`interval`, `rate.amount` is required only when the user is writing that mode
and has stated the amount. Do not invent `30d`.

## 3. Validation and repair

The only command is:

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

`PATH` is the file the user pointed at. Always pass `--json` and
`--no-analytics`. Run it at most three times. Repair only from a diagnostic
it returns (`code` and `pointer`), and only inside the edit the user asked
for, plus deleting a secret or variable credential as required above. Stop
when the same `code` and `pointer` repeat. Do not invent a repair. Field
repairs are in [Limits](references/limits.md).

Accept the edit as contract-valid only when all of these hold:

- `manifestValid` is true
- `schemaVersion` is 5
- the file's `schema` is `proof.liskov.application-manifest`

`schemaVersion` 6 with `manifestValid` true is out of scope. Do not deliver
it as a successful edit. `firstPublicReady` is not admission and not launch.
`manifestValid` is not a launch. When `execution.mode` is `interval`, or
`deployment.jobs` is greater than 2, say the file can validate and still not
launch or be admitted. Do not rewrite the user's mode or job count.

Stdout of a completed run is one JSON object. Parsers use that object. If
`proof` is missing, exits before JSON, or returns no JSON object, the edit
is not validated. Say that the owner validator did not run. Do not mark the
edit contract-valid. Do not build a replacement checker.

## 4. Explanation

Explain the diff, the units the document uses, and every fact you left
absent. Do not claim the file can publish, that a job will launch, or that
spend was consented. A cap is not a reserve and not a final charge.

Publication stays liskov-publish. This skill does not publish.
