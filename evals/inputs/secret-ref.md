# secret-ref

The document has a secret `value` field. That field is not a reference.

Document: `skills/liskov-policy/assets/fixtures/secret-value.json`

Remove `value`. Keep `secretId` and `destination`. Do not echo the value in
the reply, the file, or a comment. The value stays in the product's secret
store, which this skill does not call.
