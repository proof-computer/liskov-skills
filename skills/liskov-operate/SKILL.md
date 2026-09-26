---
name: liskov-operate
description: "Operate one named Liskov Application. Read status, the Action Plan, activity, Liskov logging, plans, and deployment status. Pause, resume, retire, or retry only after an explicit yes. A read does not spend."
---

# Operate one Application

Operate the one Application the user named. A read does not spend. It does not
publish, reserve, or charge. A mutation waits for an explicit yes in the
conversation and then passes `--yes`.

Pause changes future Liskov planning and leaves the current job running until
schedule end. Do not claim pause stopped that job. A reserve is not a final
charge. Chain assignment is not runtime readiness.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. Use their identifiers

Take the Application identifier from the user. Take a decision id, deployment
id, job id, digest, organization, or reason only from the user or from JSON a
command just printed. Otherwise do not invent it.

If they did not name an Application, list and ask. Do not pick a row.

Run whoami when the organization is in question. That read separates the
effective organization from the persistent session organization.
`--organization` or `LISKOV_ORGANIZATION` scopes one command. Run
`organization use` only when the user asked to change the session default.

## 2. Read

Run the reads in the command boundary. Quote the JSON fields the command
returned. The public customer postures are ready, in progress, needs action,
and inactive. Do not relabel a field you did not see.

Liskov logging defaults to the recent window, not full history. Pass
`--follow` only when the user asked to watch.

## 3. Mutate only after yes

If the user has not said yes, stop at the read or the dry run. Say which.

Without `--yes`, pause and resume are a dry run. The server returns that
preview. It does not pause or resume. Without `--yes`, retire is read only.

After an explicit yes, run one mutation from the command boundary. Pause does
not stop the current job. Resume does not revive an ended job and can reserve
new USD Service Credits. Retire with `--yes` pauses and starts retirement.
Existing schedules continue to their chain-owned end. Wait for the retirement
receipt, not an immediate delete. `retire cancel` with `--yes` leaves the
Application paused.

Retry once. The decision id is the id in the action-plan JSON just read. The
reason is the user's words. Do not loop.

## 4. Say what the JSON showed

Quote fields. Name the current job only when the JSON identifies it. Do not
claim a final charge, a stopped job, or a posture the JSON did not show.

Spend wording belongs to liskov-spend. Whether the running bytes match belongs
to liskov-proof. One symptom to one next action belongs to liskov-diagnose.
Manifest drafting belongs to liskov-policy.

A missing live agent run is not a pass.
