---
name: liskov-fleet
description: Read Applications in one organization. Use for a fleet picture, the effective organization, or status of Applications the user named or that one list returned. Read only. No bulk pause, publish, retire, or retry, and no spend figures.
---

# Read one organization's Applications

This skill is a read only picture of Applications in one organization. It
does not pause, publish, retire, retry, or spend. There is no bulk action
here.

Before reading, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. Name the organization first

Start with whoami so the reply names the effective organization and whether
it differs from the persistent one.

```sh
proof liskov whoami --json --no-analytics
```

Use `organizationContext.effective` and `organizationContext.sessionDefault`
from that JSON. Say whether they differ. `organizationContext.source` says
why. If `organizationContext` is absent, say the comparison is incomplete.
Do not invent an organization.

The picture is one organization, the effective one. Do not walk other
organizations. `--organization` or `LISKOV_ORGANIZATION` scopes this command
only. Do not run `organization use` unless the user asked to change the
session default.

## 2. List once

```sh
proof liskov application list --json --no-analytics
```

Reviewed help shows no limit flag and no page flag. Do not invent `--limit`,
a cursor, or a next page. The one JSON response is the whole read. Say that
bound. Use `--retired` only when the user asked for retired Applications.
Do not pass `--deleted`.

When the user scoped whoami with an organization selector, pass the same
`--organization ORGANIZATION` on this list. `ORGANIZATION` is their selector.
Do not invent one.

## 3. Status only for named rows or that response

If the user named Applications, read status only for those names. If they
named none and asked for the fleet, read status for entries on the first
page `list` returned. That page is the one response. Do not status an id
that is neither named nor present there. Do not status the rest of the page
when they named a subset.

```sh
proof liskov application status APP --json --no-analytics
```

`APP` is that id. Prefer the uid when the response prints one. The public
CLI reference says a row's lifecycle is Current, Retiring, or Retired, with
the stored status beside it. Report the posture the status command prints.
Do not translate a missing posture into Ready.

| Posture the operate page defines | Meaning |
| --- | --- |
| Ready | Current evidence satisfies the desired state |
| In progress | Liskov or Acurast is advancing or waiting |
| Needs action | A current Hold on the organization Action Plan is waiting for a decision |
| Inactive | Paused, retiring, retired, or otherwise not admitting new execution |

Posture is not a raw job state. Do not open the organization Action Plan
from this skill, and do not retry.

## 4. No mutations and no invented money

Do not run a mutation inside a loop. There is no bulk pause, publish,
retire, or retry. A pause or retire of one Application is liskov-operate,
after its own yes. This skill does not run it.

Money figures are liskov-spend. If status output has no charge field, do
not invent a spend number. Slots in use are the plan's application-slot
quota, not a team seat and not a charge.

## 5. Reply

Name the effective organization, whether it differs from the persistent one,
the list bound, and the status you actually read. Otherwise do not invent
ids, pages, or charges. A missing live agent run is not a pass.
