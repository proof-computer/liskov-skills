# Limits

Read this with the [Command boundary](command-boundary.md). It is not a second
workflow. This skill is read only. USD Service Credits are the customer unit.
They are not a bank account, a stablecoin, a crypto token, or a withdrawable
wallet.

## Which word you may use

Call a number a reserve, a release, or a final charge only when the JSON field
says so. A quote or an estimate is not a charge.

| Word | Use it when | Do not |
| --- | --- | --- |
| Reserve | The JSON field says reserve. It is a hold set aside before settlement | Call it a cost, a quote, an estimate, or a final charge. A reserve is a hold, not a cost |
| Release | The JSON field says release. Unused reserve returned to available credit | Invent a release the field does not show |
| Final charge | The JSON field says that amount was charged or debited | Infer it by subtracting two balances |
| Policy cap | The plans JSON shows the cap the user authored | Call it the settled charge, or a reserve, unless that field says so |
| Quote or estimate | Never, as a charge. The charges page says there is no separate pre-launch cost estimate. The reserve is a bound, not a quote | Record a quote as money spent |

The charges page says a reserve is a ceiling, never an estimate and never a
cost. It is not proof of successful execution. A final charge can be below the
cap and below the reserve. While money is pending, available credit is the
balance minus open reserves. The charge appears at settlement.

Console labels on Billing & funding are Settled, Held, Available, Promo, and
Refundable. Held is set aside, not charged. Do not paste a Console label onto
a CLI field that does not use that word. A reserve, a review hold, or a
released reserve does not move the ledger's running balance. Quote the field
you have.

Never infer a final charge by subtracting two displayed balances. Match a
reserve, a final charge, and a release to the Application and deployment the
JSON names. A missing or failed read is unavailable, not zero.

Sources: [Per-job caps, reserves, and final charges](https://docs.proof.computer/liskov/organizations/charges)
and [Read USD Service Credits](https://docs.proof.computer/liskov/organizations/service-credits).

## Missing execution report

Use this only for the row the network-costs page states. For managed custody,
when the strict report deadline has passed and the finalized scanner proves no
report was filed, the final charge is zero and the reserve is released in
full. The public phrase on that row is **Zero — not billed**. The closeout is
`report_absent_not_billed`, with no unresolved amount and no customer action.

That is not a review and not a retry. An open deadline, or an unreadable,
unavailable, outside-coverage, conflicting, or failed scan, stays deferred.
Do not call that deferred case Zero — not billed. Do not invent a zero. The
charges page says the same settled case: no report filed, charge zero, whole
linked reserve released, no customer action. Unclear evidence stays held and
under review. Liskov does not guess.

Self-custody does not use this USD Service Credit rule. Do not invent an ACU
refund. Do not run custody.

Sources: [What each deployment outcome costs](https://docs.proof.computer/liskov/organizations/network-costs-and-outcomes)
and [Costs and custody model](https://docs.proof.computer/liskov/concepts/costs-custody).

## What the customer does not pay as a separate line

Do not invent a charge for an attempt the network refused, for Liskov's own
chain transaction fee, or for any amount above that deployment's reserve. A
registration that ended and returned nothing is not the same as missing chain
evidence. Missing chain evidence is deferred or in review, not a zero return.
Quote the JSON rather than choosing a row by guess.

Pause and retirement do not end a job the chain already owns. A reserve can
stay open after a pause, until that job settles. A renewal is new work with
its own reserve. Say that only when the JSON shows it.

## Funding is not a customer action

Customer Stripe checkout and issuance of new USD Service Credits are
release-gated. Checkout is not a supported customer action. Do not submit
payment details. Do not call an internal funding endpoint. There is no CLI
command to fund, change plan, or pay. Do not send the user to buy credits.
Do not invent a command.

A disabled or missing checkout control is not an invitation to a workaround. A
successful redirect does not prove credit was issued. Verify the ledger read.
The customer does not deposit USDC or ACU, manage an Acurast wallet, approve a
swap, or withdraw network settlement assets. Treasury movement is not a second
customer balance.

No single cap promises that work will run or that the final charge will equal
the cap.
