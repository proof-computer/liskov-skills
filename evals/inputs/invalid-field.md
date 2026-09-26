# invalid-field

The duration field is the bare string "60". The user already said the unit
is seconds.

Document: `skills/liskov-policy/assets/fixtures/invalid-duration.json`

Repair only from the owner-validator diagnostic at
`/deployment/schedule/duration`, using that stated unit. Sixty seconds is
`60s`. Do not invent a different unit. Do not change any other field.
