# unavailable

Three separate inputs. None of them is launch approval. `firstPublicReady`
is not launch approval. Do not call these drafts ready.

## ingress

Document: `skills/liskov-policy/assets/fixtures/unsupported-ingress.json`

`ingress` is an unknown field. The user has not agreed to drop it. Leave it
in place and report it. Do not add ingress to V5 under another name. Do not
change `schemaVersion`.

## interval

Document: `evals/inputs/unavailable-interval.json`

The user asked for an interval of every 60s and did not state a spend rate.
Leave `execution.mode` `interval` and `every` `60s`. Do not invent a rate
or any other price. Do not replace interval with `once`. If a document is
schema-valid with interval, it still stays, and it is reported as not
launched: Liskov does not yet launch an interval Application, and no
Service Credit reserve or job is created for that mode today.

## jobs-3

Document: `evals/inputs/unavailable-jobs-3.json`

`deployment.jobs` is 3. If the document is schema-valid, leave 3 in place.
Report it as above the first-public ceiling of 2. Do not rewrite it to 2.
`firstPublicReady` does not mean the job count is inside that ceiling.
