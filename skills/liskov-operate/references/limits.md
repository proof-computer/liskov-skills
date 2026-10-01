# Limits

Read this with the [Command boundary](command-boundary.md). It is not a second
workflow. Quote JSON. Do not relabel a field you did not see.

## Customer posture

The public postures are ready, in progress, needs action, and inactive. Use
one of those words only when the status JSON says it. Posture is not a raw
job state. One Application can have an old job still running and a successor
in progress.

| Posture | What the status page says | What you do |
| --- | --- | --- |
| Ready | Current evidence satisfies the desired Application state | Quote it. Do not start a mutation |
| In progress | Liskov or Acurast is advancing work or waiting for an expected external fact | Wait. Do not retry a normal wait |
| Needs action | The Application has a current Hold on the organization Action Plan that is waiting for a decision | Read that plan. Retry only under the command boundary |
| Inactive | Paused, retiring, retired, or not admitting new execution | Read the lifecycle reason the JSON states |

Source: [Application status and Action Plan](https://docs.proof.computer/liskov/operate/status-action-plan).

The Action Plan lists work Liskov has stopped on. Platform uncertainty is not
a customer decision. A retry is a bounded mutation for the decision id the
plan returned. It does not mean keep trying until it works. After one retry,
stop if the same blocker remains.

## Pause, resume, and the current job

| Action | What changes | What does not |
| --- | --- | --- |
| Pause dry run | Nothing. Omission of `--yes` is a dry run | Not a pause |
| Pause after yes | Future Liskov planning. The Application is inactive for new planning | The current job. It keeps running to schedule end and may keep logging |
| Resume dry run | Nothing. Omission of `--yes` is a dry run | Not a resume |
| Resume after yes | Liskov may evaluate desired state again. It can reserve new USD Service Credits | An ended job. A hold. A reserve is not a final charge |
| Override | Only the replacement hold the user named, with `--reason` and `--yes` | Any other hold |

Pause does not force-stop an Acurast job, revoke a managed secret, or undo
money already committed. A held job is not a paused Application. Resume does
not clear a hold, and releasing a hold does not resume a paused Application.
This skill does not run `application hold`.

Fixed-interval execution is release-gated. The capabilities page says Liskov
does not yet launch an interval Application: it stops before any USD Service
Credit reserve or job is created. Do not treat a validated interval manifest
as a running job. The pause page's accepted interval behavior, when that gate
is not the question, is that a paused interval Application starts no new
occurrence and resume does not catch up missed boundaries.

Sources: [Pause and resume](https://docs.proof.computer/liskov/operate/pause-resume)
and [Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities).

## Retirement

| Step | Result |
| --- | --- |
| Retire without `--yes` | Read only. Quote blockers and schedule ends the JSON returns |
| Retire with `--yes` | Pauses and starts retirement. Does not stop an existing job. Does not erase evidence |
| While it runs | Quote the phase the JSON returns. Do not assign a phase it omitted |
| Done | The retirement receipt, not an immediate delete |
| Cancel with `--yes` | Leaves the Application paused. Does not resume it |

The customer-facing words are Current, Retiring, and Retired. A persisted
`status` of `deleted` is a compatibility detail, not the customer word and not
an immediate delete. Current and Retiring hold an Application slot. Retired
releases it. Pausing is not retirement and does not free the slot.

The public phases while retirement is active are `terminalizing_local`,
`waiting_for_schedule_end`, `waiting_for_financial_tail`, and `blocked`. Most
obligations need nothing from the user. An obligation waiting on a chain
schedule is progress. If cancel returns `retirement_already_completed` with
the receipt, that is success: retirement finished and there was nothing left
to cancel.

A `safe_retirement` receipt proves a zero gate at completion. A
`legacy_immediate_tombstone` is a historical deletion from before safe
retirement. It is not proof of that zero gate. Quote whichever kind the JSON
returns. Do not invent a receipt digest.

Source: [Retire an Application](https://docs.proof.computer/liskov/operate/retire).

## Liskov logging and activity

Logs answer what customer code reported. They are not an authoritative
lifecycle ledger. Activity answers what changed in Liskov. A deployment
timeline answers where a deployment is. Do not treat one as the other.

The default logs command is the recent window. Full history is `--from-start`,
and only when the user asked. Retained history depends on the plan already in
force: Free 24 hours, Developer 3 days, Pro 14 days, Business 30 days, Scale
90 days, Enterprise 90 days. A visible plan does not by itself change the
current allowance. Export is the user's action. Do not invent a longer window.

If an activity record carries `report_absent_not_billed`, the public meaning
is **Not billed — no report filed**: zero charged, full reserve release,
closed financial state, and no customer action. It is settled. It is not a
missing-report review and not a retry. Do not copy a credential out of a log
line. Managed secrets stay references. Never print a secret value.

Source: [Monitor logs and activity](https://docs.proof.computer/liskov/operate/logs-activity).

## Deployments, jobs, and runtime instances

| Word | What it is | What it is not |
| --- | --- | --- |
| Deployment | Liskov's recorded attempt or generation | Not the chain-owned job |
| Job | The time-boxed Acurast registration, with a schedule and a processor | Not a runtime instance |
| Runtime instance | One process boot within that job | Not proof the next boot is the same process |
| Chain assignment | A processor was assigned on the network | Not runtime readiness. The job can still be fetching, starting, or bootstrapping |

A successor does not mutate the registered job. Desired replacement is not
proof the successor was submitted, assigned, or ready. A plan row is not an
execution. A missing amount is not a zero charge. Reserved credits are not
charged credits. Quote the words the JSON uses.

Source: [Deployments, jobs, and timelines](https://docs.proof.computer/liskov/operate/deployments-jobs).

## Money words, only if the JSON says them

This skill does not settle money. A read does not spend. A confirmed resume can
reserve USD Service Credits. Call that a reserve only when the JSON says so.
Do not call it a final charge. Spend questions belong to liskov-spend.
