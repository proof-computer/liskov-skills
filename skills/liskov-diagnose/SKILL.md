---
name: liskov-diagnose
description: "From one Liskov symptom to one next action. Read status, the Action Plan, deployment status, and a bounded log window. Wait, retry one returned decision after an explicit yes, or name one human step. Does not run, delete, or loop."
---

# One symptom, one next action

Start from one symptom on one Application the user named. End at exactly one
next action. Do not propose a second action in the same breath.

The one next action is one of these:

- wait, because the evidence shows normal progress
- one `action-plan retry`, using the decision id the plan just returned, and
  only after the user then says yes
- one human step: a Console secret value, a balance check that then stops,
  source binding, or an operator key

Reads do not spend. Do not run `application run`. Do not delete. Do not invent
a decision id, an application id, a deployment id, a job id, or a reason.

`manifestValid` is not a launch. Chain assignment is not runtime readiness.
Pause does not stop the current job. An interval schedule can validate and
still not launch.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. Bound the question

Use the Application identifier the user named. If they did not name one, ask.
Do not pick a row. Take every other id from the user or from JSON a command
just printed.

Run whoami when the organization is in question. That read separates the
effective organization from the persistent session organization.
`--organization` or `LISKOV_ORGANIZATION` scopes one command. Run
`organization use` only when the user asked to change the session default.

## 2. Read

Run status, the Action Plan, deployment status, and the recent log window.
Pass `--limit` only when the user named a count. Do not pass `--follow`
unless the user asked to watch, and then omit `--json`. Do not page the full
history. Quote the JSON fields. The public customer postures are ready, in
progress, needs action, and inactive. Do not relabel a field you did not see.

## 3. Choose one ending

Use [Limits](references/limits.md). Normal progress ends in wait. A missing
managed secret, source binding, or operator key ends in that one human
step. Short credit ends in a balance check, then a stop. Do not send the
user to buy credits. Do not retry those in the same breath. Retry cannot
correct a missing secret, an invalid policy, or an insufficient balance.

Retry only when the plan just returned a decision id, the blocker is one retry
can address, and the user has said yes. Use their reason. One retry. Do not
loop.

If the evidence is only `manifestValid`, or only an interval schedule that
validated, say that is not a launch and do not retry it into existence.

## 4. Stop

Say the one next action and the evidence for it. Do not add a pause, a
resume, a retire, a publish, a hold command, or a second read as a second
action. Operation commands belong to liskov-operate. Money words belong to
liskov-spend. Byte-for-byte proof belongs to liskov-proof. Manifest drafting
belongs to liskov-policy.

A missing live agent run is not a pass.
