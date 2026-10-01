# Limits

Day-to-day operation starts at the Application workspace.
[Deploy & operate](https://docs.proof.computer/liskov/operate/) is that map.
[Application status and Action Plan](https://docs.proof.computer/liskov/operate/status-action-plan)
defines posture. Session fields are on
[CLI](https://docs.proof.computer/liskov/reference/cli).

This skill only reads. It does not perform the actions those pages describe.

## Read bound

| Read | Bound |
| --- | --- |
| Organization | One organization. The effective one from whoami |
| List | One `application list` response. Help shows no limit flag and no page flag |
| Retired | `--retired` only when the user asked. Not a second page |
| Status | Names the user gave, or every entry in that one response when they named nobody |
| Money | Not read here. If status output has no charge field, do not invent a spend number |
| Mutations | None. No bulk pause, publish, retire, or retry |

Say the list bound in the reply. Do not invent pagination to look complete.
An empty `applications` array is an empty fleet, not a cue to try another
organization.

## Posture

Report only a posture the status command printed.

| Printed posture | Do not turn it into |
| --- | --- |
| Ready | Proof the workload is correct, or a spend total |
| In progress | A stall. Wait is the page's default |
| Needs action | Permission to retry, pause, or release a hold. The page's meaning is a Hold waiting for a decision |
| Inactive | Permission to resume or to cancel retirement |
| Absent | Ready. Say it was not in the output |

One Application can have an old job still running and a different overall
posture. Do not collapse those into one invented state.

The Console coverage strip reports intended versus effective capacity and
remaining charges. It is not a second Action Plan. This skill does not
compute remaining charges. A slots-in-use line is the plan's
application-slot quota. It is not a team seat and not a Service Credit
charge.

## What the reply must not add

- An organization the user did not select and whoami did not print.
- An Application id that was not named and was not in the list response.
- A next page, cursor, or `--limit`.
- A charge, price, or balance.
- A bulk pause, publish, retire, or retry.
- A claim that the fleet is healthy because the list command exited 0.

Pause, resume, retire, and Action Plan retry stay on their own pages and
are not run here. One Application's pause or retire is liskov-operate,
after its own yes. Money is liskov-spend.

`manifestValid` is liskov-policy. This skill does not validate a manifest.
