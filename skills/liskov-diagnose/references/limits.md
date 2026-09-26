# Limits

Read this with the [Command boundary](command-boundary.md). It is not a second
workflow. Pick one next action. Then stop.

If a decision id was not in the action-plan JSON just read, do not invent one.

## Five distinctions

| Distinction | What the public pages agree | The one next action is not |
| --- | --- | --- |
| A chain assignment is not a runtime-ready job | Processor assignment is not runtime readiness. The job can still be fetching, starting, and bootstrapping | A retry, or a claim the runtime is ready |
| Pause does not stop the current job | Pause does not force-stop an Acurast job. The current job continues to schedule end and may keep logging | A claim that pause killed it, or a second mutation to force the stop |
| `manifestValid` is not a launch | A valid local manifest is not a deployment, a job, or a runtime instance | A launch. Do not run `application run` |
| An interval schedule can validate and still not launch | Capabilities: no interval run has been observed in production, and Liskov does not yet launch an interval Application. It stops before any USD Service Credit reserve or job is created | A retry meant to force a launch |
| A missing execution report is not, by itself, a failure the user must retry | Only when the charges page's settled case applies. See below | A retry of that closeout |

Sources: [Deployments, jobs, and timelines](https://docs.proof.computer/liskov/operate/deployments-jobs),
[Attestation and the proof chain](https://docs.proof.computer/liskov/concepts/attestation),
[Pause and resume](https://docs.proof.computer/liskov/operate/pause-resume),
[Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities),
and [Per-job caps, reserves, and final charges](https://docs.proof.computer/liskov/organizations/charges).

## When the missing report is already settled

Use the charges page, not a guess. If the final evidence shows no report was
filed, the charge is zero and the whole reserve is released. That managed
closeout is not billed. It carries `report_absent_not_billed`. It is closed,
not an amount in review, and it needs no customer action. The deployment
troubleshooting page names the same row **Not billed — no report filed**.

The one next action is wait. Do not retry it. Do not tell the user to pay the
reserve.

If the deadline is still open, the scanner is unavailable or outside coverage,
the evidence conflicts, or the read failed, settlement stays deferred. Do not
call that a zero charge. Do not invent a decision id for it. Stronger
signed-fatal or disagreement evidence keeps its own Action Plan treatment.
Follow that typed condition, still as one next action.

## Normal progress is wait

Do not resubmit a normal wait. The deployment troubleshooting page maps this
evidence to waiting, not to a customer retry:

| Evidence | Read it as |
| --- | --- |
| Policy or deployment created, no submission yet | Liskov can still be preparing funding, configuration, or launch authority |
| Submitted, no processor | Market assignment is pending |
| Processor assigned, no runtime contact | The current job can still be fetching, starting, and bootstrapping |
| Runtime configuring | Identity, configuration, managed secrets, or Liskov logging are advancing |
| Runtime ready, no Application output | The workload's own tick or external service, not a failed launch |

A failure after contact can stay in progress and non-actionable while Liskov
waits for terminal facts. The first public policy waits to schedule end rather
than registering a fresh job on runtime failure. Coverage is not a second
Action Plan. Quiet is not stalled. Evidence unavailable is not a confirmed
absence. A missing processor identity does not prove no processor took the
job. An unreadable charge is not a zero charge.

`processorAtMatchCap` means Liskov is excluding that processor and trying the
next candidate inside its own retry budget. That is not your retry. Platform
uncertainty is not a customer decision.

Source: [Deployment waiting or needs action](https://docs.proof.computer/liskov/troubleshooting/deployment).

## Retry, or a human step, never both

Retry can create new work or spend. It cannot correct a missing managed
secret, an invalid policy, or an insufficient balance. One confirmed retry is
enough. Do not loop.

| Evidence | One next action |
| --- | --- |
| Normal progress, or the settled no-report closeout | Wait |
| The plan offers a retry, the cause is one retry can address, and the user has said yes | That one retry, with the decision id just returned and the user's reason |
| The plan offers a retry and the user has not said yes | Stop on that decision id and wait for yes. Do not run it |
| A required managed secret is missing | One human step: set the secret value in the Console. Do not print the value. Do not put it in a variable or a repository |
| Funding or the cap blocks spend | One next action: verify the balance with liskov-spend and stop. Checkout is release-gated and not a supported customer action. Do not send the user to fund, check out, or buy a plan |
| No source binding | One human step: an organization admin binds repository, ref, workflow, and manifest path. Do not run the binding command |
| An operator key is required | One human step: the operator key. Do not run SSH and do not install a key |
| `authoringFault` or another invalid policy | Do not retry the same policy. One human step is to correct the reported schedule, then stop. Manifest editing belongs to liskov-policy. Do not do it here |

A configuration save does not mutate the process that is already running.
Read the new runtime instance, not a predecessor still running to schedule
end. An empty string the user set is an explicit value, not a missing one.
`job_grant_not_found` during signed discovery can be the runtime's own bounded
retry. Do not add a customer retry on top of it unless the Action Plan just
returned a decision id and the user said yes.

The deployment page's schedule corrections, when the plan names
`authoringFault`, are at least 60 seconds for `durationMs`, at most one hour
for `maxStartDelayMs`, and no start more than 24 hours ahead. Report the
pointer the plan returned. Do not invent a new schedule.

Sources: [Diagnose and retry](https://docs.proof.computer/liskov/operate/diagnose-retry)
and [Variables, secrets, and runtime bootstrap](https://docs.proof.computer/liskov/troubleshooting/config-bootstrap).

## Holds are not this command

A held job is not a paused Application. This skill does not run `application
hold`. If the only offered customer control is a Console release, name that
control and stop. Do not also retry. A release can spend. Do not perform it
from here.
