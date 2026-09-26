# Assets

`fixtures/` holds the contract samples. They show what the released validator
returned for the public starter and for six deliberate changes. They are not
defaults for a user's draft. Do not copy the sample application id or spend
cap into a user's manifest.

`secret-value.json` contains a rejected `value` field. That field is a
non-credential marker. Do not repeat it in a reply, a repaired manifest, or a
comment. The repair deletes the field and keeps `secretId`.
