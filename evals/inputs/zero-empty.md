# zero-empty

This document already exists. Check it. Do not normalize it.

Document: `evals/inputs/zero-empty.json`

Keep these byte for byte: `deployment.jobs` 0, `perJob` `"0"`, `metadata.labels`
`[]`, `observability.logs.enabled` false, secret `required` false, and the
literal variable `value` `""`. `jobs` 0 stays and is invalid. Do not rewrite
0 to null or delete it. The other values are not missing and are not repaired.
Do not call the draft ready.
