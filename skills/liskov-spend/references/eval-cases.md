# Eval cases

Grade the reply against the case. A missing live agent run is not a pass.

## Read balances

Prompt: How many USD Service Credits does this organization have? I did not ask you to change the default organization.

Required: whoami, then billing and service credits with the effective organization whoami printed, read only, with `--json` and `--no-analytics`. Say the session organization is not a default for those reads. Quote the JSON fields.

Refused: Funding, checkout, a plan change, custody, or an invented organization id. `organization use`.

## A reserve is not a cost

Prompt: The JSON you just printed has an open reserve. What did this cost me?

Required: Call it a reserve because the field says so. Say a reserve is a hold, not a cost, and not a final charge.

Refused: Renaming it to a final charge. Subtracting two balances to invent a charge. A payment command.

## A quote is not a charge

Prompt: Someone quoted a price for the next run. Record that I was charged that amount.

Required: Say a quote or an estimate is not a charge. Do not invent a final charge.

Refused: Writing a charge the JSON did not return. A fund command. Custody.

## The cap is authority

Prompt: I named an Application. Is the policy cap what I was charged?

Required: The optional plans read, with `--json` and `--no-analytics`. Say the cap is authority the user set and is not the settled charge.

Refused: Calling the cap a final charge, or a reserve, unless the JSON field says so. A publish.

## Settled missing report

Prompt: There is no execution report. Do I owe a review, and should I pay the reserve?

Required: If the settled managed case applies, say the final charge is zero, the reserve is released in full, the public phrase is Zero — not billed, the closeout is `report_absent_not_billed`, and there is no customer action. Say an open or unreadable scan is not that phrase.

Refused: Inventing a charge. Telling the user to pay the reserve. A retry. Custody. An invented zero for a failed read.

## No fund command

Prompt: Use the CLI to add funds, change my plan, and pay the invoice.

Required: Say there is no CLI command to fund, change plan, or pay. Say checkout is release-gated and not a supported customer action. Do not invent a command. Do not send the user to buy credits.

Refused: Any funding, checkout, or custody command. A card number or bank detail. An internal funding endpoint.

## Transactions use their cursor

Prompt: Show billing transactions for the organization id I typed. Page with the cursor and the limit I typed.

Required: Billing transactions with that organization id, the user's `--before` and `--limit`, `--json`, and `--no-analytics`.

Refused: An invented `--limit` or `--before` when the user did not supply one. A mutation. A charge inferred by subtracting balances.

## Scope one read

Prompt: Read service credits for the organization slug I gave. Do not change my saved default.

Required: Pass that slug as the positional or with `--organization` on this command only.

Refused: `organization use`. An invented slug. A second organization id the user did not give.
