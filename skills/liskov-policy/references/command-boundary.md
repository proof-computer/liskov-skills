# Command boundary

Read this while drafting. It is not a second workflow.

## The one drafting command

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

Reviewed help, plugin `@proof-computer/proof-cli-liskov` `0.16.0`: "Strictly
validate an authored Application manifest v4 or retained V5 file without
publishing it." That help text is not this skill's support list. This skill
drafts only `proof.liskov.application-manifest` at `schemaVersion` `5`.

Required flag: `--file`. Optional flag the skill always passes: `--json`.
Global flag the skill always passes: `--no-analytics`. Flag order is `--file`,
then `--json`, then `--no-analytics`.

`PATH` is the draft file. The default path, when the user did not state one,
is `.liskov/application-manifest.json`.

With `--no-analytics`, the process reads the local file and writes a verdict
to stdout. It does not create an Application, publish, deploy, reserve, or
charge. Omitting `--no-analytics` lets a saved session `POST
/api/telemetry/cli-invocation` with the command id and an exit class. Do not
drop the flag to match the public guide's example. The guide's example omits
it. This skill does not.

Stdout of a completed run contains one JSON object. On failure, oclif may also
print an `EEXIT` banner. Parsers use the JSON object. Exit `0` when `errors`
is empty. Exit `1` when `errors` is non-empty.

There is no YAML flag. A YAML file returns `invalid_manifest` because the
command parses JSON. Do not add a YAML parser. Write JSON.

The skill helper `scripts/validate_manifest.py` accepts only `--file PATH` and
executes the command above. Any other argument is refused before execution.
Use the helper when a caller might append another command. Its refusal is not
a manifest verdict.

Do not copy a schema into the skill and do not implement a second validator.
Quote digests only from the command just run.

## Pair this command checks

| Role | Schema | Version |
| --- | --- | --- |
| Authored file | `proof.liskov.application-manifest` | `5` |

Release identity of that pair. These digests name the pair. They are not
values to write into `release.artifact` or any other field of the user's file.

| Artifact | Value |
| --- | --- |
| Domain | `proof.liskov.policy-v5-rc.v1` |
| RC digest | `sha256:549272988045e9357c4945850706569ed8dc7f0c6f419b7cf5c57d54b294bb10` |
| Authored schema digest | `sha256:38ca88eefe599d9a13b0906fb7ae86be002fb7aa15767925a2fe11908fec95da` |
| Effective schema digest | `sha256:5907054022521f9926164d1e899fa89ecf931ea916da5d7989a6c58015053c30` |
| Public field guide | [Retained Application Manifest V5](https://docs.proof.computer/liskov/reference/manifest-v5) |
| Availability | [Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities). Retained Manifest V5 / Policy V5 is v1. |
| Authoring guide | [Author a retained Application Manifest V5](https://docs.proof.computer/liskov/build/manifest-v5) |

The stored pair `proof.liskov.application-policy` at version `5` is the
server's effective policy. Do not write it. On the reviewed CLI, that `schema`
fails validate with `invalid_manifest` at `/schema` and the message `schema
must be "proof.liskov.application-manifest"`.

No later version is supported. The CLI bundle's supported pairs are not this
skill's support list. A document is in scope only when its `schema` is
`proof.liskov.application-manifest` and its `schemaVersion` is `5`.

## Recorded starter readback

`assets/fixtures/retained-v5-starter.json` is the public starter, unchanged.
On plugin `0.16.0` the drafting command exited `0` and returned:

```json
{
  "ok": true,
  "manifestValid": true,
  "schemaVersion": 5,
  "authoredDigest": "f70cbce1bcd00d84241d022f654e5f49f000e0cb214296c93c5e3b1b9c084873",
  "releaseIntentDigest": "854fa5568c55b627b85d3cdc79ff56bf798d12a8450a96245edb7d76ecb3315b",
  "firstPublicReady": true,
  "errors": [],
  "capabilityDiagnostics": [],
  "deprecationDiagnostics": []
}
```

Those digests are outputs of that CLI for that sample. Do not type them into
a user's file. The sample's `applicationId` and `perJob` are not defaults.

The other files in `assets/fixtures/` show a bare duration, an `ingress`
field, a missing `applicationId`, a secret `value`, `jobs` `0`, and
`schemaVersion` `6`. They are not templates.

## Commands that are not drafting

Do not run any of these. A dry run is still not drafting. Do not invent an
Application id in order to call one.

| Command | Side effect | Rule |
| --- | --- | --- |
| `application create` | Creates an Application record from identity. Help says no spend. It is still a platform write. | Do not run. Say creation is a separate product step. |
| `application import` | Imports a manifest as a server draft. | Do not run. |
| `application policy publish` | With `--yes`, `POST /api/applications/{id}/policy-versions`. `--dry-run` is still a server preview. `--yes` and `--dry-run` are mutually exclusive. Nothing is sent when both are absent: the command asks for confirmation. | Do not run, including `--dry-run`. |
| `application policy explain` | Authenticated read of one existing Application's published explanation. It does not explain a local unpublished file. | Do not run. |
| `application publish` | Publication path. | Do not run. |
| `source-binding set` | Binds repository, ref, workflow, and manifest path on the server. | Do not run. Leave those facts out of the manifest. |
| `pause`, `resume`, `application run` | Lifecycle or spend paths. | Do not run. |
| custody execution | Spend path. | Do not run. |

There is no local explain command for an unpublished file. This skill's
explanation is the reply plus the local validate JSON.

Publication remains the user's later action through the public authoring
guide. Naming the guide is allowed. Performing the action is not.

## Validation outage

If `proof` is missing, exits before JSON, or returns no JSON object, the
draft is not validated. Say that the owner validator did not run. Do not mark
the draft contract-valid. Do not build a replacement checker. That case is
not a pass.
