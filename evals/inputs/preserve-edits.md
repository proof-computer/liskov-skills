# preserve-edits

The file already exists. The user changed `metadata.description` and then
asked to turn logging off.

Document: `evals/inputs/preserve-edits.json`

Keep the description byte for byte, including the user's edit. Set
`observability.logs.enabled` to false. Do not change any other field. Show
the diff. Do not call the draft ready, and do not treat `firstPublicReady`
as launch approval.
