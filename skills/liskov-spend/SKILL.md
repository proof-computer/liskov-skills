---
name: liskov-spend
description: "Explain USD Service Credits for one Liskov organization. Read-only billing, balances, and transactions. A reserve is a hold, not a cost. Does not fund, change plan, pay, or run custody."
---

# Read one organization's money

This skill is read only. It names reserves, releases, and final charges for
one organization. It does not fund, change a plan, pay, reserve, or charge.
There is no supported customer checkout and no CLI command to fund, change
plan, or pay. Do not invent one. Do not send the user to buy credits. Do not
run custody.

A reserve is a hold, not a cost. A quote or an estimate is not a charge. A
reserve is not a final charge. Call a number a reserve, a release, or a final
charge only when the JSON field says so.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. Name the organization

Run whoami. That read separates the effective organization from the persistent
session organization. Quote the organization fields it prints. Do not rename
them.

Billing, service credits, and billing transactions require a selector. The
session organization is not a default for those three reads. Pass the
organization the user named. When they named none, pass the effective
organization id or slug whoami just printed. When whoami printed none, ask.
Do not invent one. `--organization` or `LISKOV_ORGANIZATION` is that selector
for one command. Run `organization use` only when the user asked to change
the session default.

## 2. Read balances and history

Run billing, service credits, and billing transactions with that selector.
When the user named an Application, you may also read its plans. The cap in
that policy is authority the user set. It is not the settled charge.

Quote the JSON. Do not subtract two balances to invent a charge. Do not relabel
a field you did not see.

## 3. Use the settled-report rule only when it fits

When the network-costs page's conditions are the ones in
[Limits](references/limits.md), say the public phrase it uses. An open,
unreadable, outside-coverage, conflicting, or failed scan is not that phrase.
Do not invent a zero to fill a missing read.

Daily operation belongs to liskov-operate. Byte-for-byte proof belongs to
liskov-proof. One symptom to one next action belongs to liskov-diagnose.
Manifest drafting belongs to liskov-policy.

A missing live agent run is not a pass.
