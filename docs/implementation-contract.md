# liskov-policy implementation contract

Reviewed 2026-09-26. This is the authoring contract for the shared
`skills/liskov-policy/` skill. It records the surfaces that existed that day.
It does not add a command, a schema field, or a policy version.

The skill creates a local Application manifest and validates it. Writing that
file does not publish, deploy, reserve, or charge. The skill does not create
an Application, bind source, or spend.

## Reviewed surfaces

| Surface | Identity | What was checked |
| --- | --- | --- |
| Released CLI plugin | `@proof-computer/proof-cli-liskov` `0.16.0`, git tag `v0.16.0` at `6fbe14510922d0150ff57ec8beb47bd51d5ad9ec` | Installed `proof liskov` help and live `application manifest validate` runs. npm `latest` was `0.16.0`. Host CLI was `@proof-computer/proof-cli` `0.1.2`. |
| CLI source | `proof-computer/proof-cli-liskov` `d68125925dde2a5cb1069e9a019f57a3e9b864a1` | No diff from the tag under `src/commands/liskov/application/manifest`, `src/commands/liskov/application/policy`, `src/application-policy.ts`, or `src/policy-client-bundle/policy-client-bundle.json`. |
| Schema owner | `proof-computer/liskov-rs` `b3def232865bfab843f086bd08bb8ee33c4e744e` | `crates/slipway-application-policy/releases/policy-release-catalogue.json` and the frozen V5 schema file. |
| Public docs | `proof-computer/docs` `2ae0855d58a2b1bf338de58ce4f843a7e6543f1d` | Retained V5 reference, capabilities, CLI reference, and the V5 authoring guide. |
| Live schema read | `GET https://console.liskov.proof.computer/api/application-manifest/v5/schema` | HTTP 200. Body is `{"schemaVersion": 5, "schema": <object>}`. The inner object parsed equal to the frozen manifest schema file. No credential was sent. |
| Claude Code | `2.1.283` | `claude plugin`, `claude plugin marketplace`, `claude plugin validate`, and `--plugin-dir` help. |
| Codex CLI | `0.157.1` | `codex plugin`, `codex plugin marketplace`, and `CODEX_HOME` as named by `codex --help`. |

`https://schemas.proof.computer` did not resolve from the review host. The
schema file's `$id` is not a second authority until it resolves. The frozen
file and the live route above are the checked schema sources.

The public build guide still tells readers to use plugin `0.14.0`. The plugin
whose help and validator were checked is `0.16.0`. Follow this contract, not
that older pin.

## Supported schema pair

The skill writes one document shape:

| Role | Schema | Version |
| --- | --- | --- |
| Authored file | `proof.liskov.application-manifest` | `5` |

Release identity for that pair:

| Artifact | Value |
| --- | --- |
| Domain | `proof.liskov.policy-v5-rc.v1` |
| RC digest | `sha256:549272988045e9357c4945850706569ed8dc7f0c6f419b7cf5c57d54b294bb10` |
| Authored schema file | `crates/slipway-application-policy/schema/application-manifest-v5.schema.json` |
| Authored schema digest | `sha256:38ca88eefe599d9a13b0906fb7ae86be002fb7aa15767925a2fe11908fec95da` |
| Effective schema file | `crates/slipway-application-policy/schema/application-policy-v5.schema.json` |
| Effective schema digest | `sha256:5907054022521f9926164d1e899fa89ecf931ea916da5d7989a6c58015053c30` |
| Catalogue | `schema` `proof.liskov.policy-release-catalogue.v1`, V5 `artifactPolicy` `frozen` |
| Public field guide | `docs/liskov/reference/manifest-v5.md` at the docs commit above |
| Availability | `docs/liskov/reference/capabilities.md` at the same commit. Retained Manifest V5 / Policy V5 is **v1**. |

The stored pair `proof.liskov.application-policy` at version `5` is the
server's effective policy. The skill does not write it. On the reviewed CLI,
a document whose `schema` is `proof.liskov.application-policy` fails
`manifest validate` with `invalid_manifest` at `/schema` and the message
`schema must be "proof.liskov.application-manifest"`.

The CLI bundle's `publicationPairs` contains one entry:
`proof.liskov.application-manifest` version `5`, labelled `releaseMode`
`source`. Source at `session.ts` also treats a V5 `pinned` release as a
registered publication pair. Registration is not permission for this skill to
publish.

No later version is supported. V6 is in the catalogue with `artifactPolicy`
`generated` and no `expectedDigest`. Its expected client surface is
`liskov-ui` opaque read, not CLI publication. Public
`docs/liskov/reference/manifest-v6.md` says V6 is not released and that
`schemaVersion: 6` is refused at publication. Capabilities do not list V6 as
v1. The bundle's `supportedPairs` includes versions 4, 5, and 6 for both
schema names. That list is not this skill's support list.

A later version enters this skill only after this contract is revised and all
of the following are true: the catalogue entry is `frozen` and has an
`expectedDigest`; public docs do not call the version unreleased; capabilities
list it as v1; and the released CLI's `publicationPairs` or its customer help
names it as a retained authoring version. A higher `schemaVersion` is not
itself support.

## Journey

The shared procedure in `skills/liskov-policy/SKILL.md` is this order.

1. **Requirements.** Read the user's request and any application files they
   point at. Collect identity, workload, source or pinned artifact, runtime,
   schedule, limits they state, configuration, and secret references. Label
   every default and every unknown. Do not fill an unknown from the sample
   fixture.
2. **Local draft.** Write one JSON document at the user-stated path, or at
   `.liskov/application-manifest.json` when they did not state one. That
   default is the path in the public V5 guide. JSON is required because the
   released validate command has no encoding flag and parses the file as JSON.
3. **Validation and repair.** Run the one drafting command below. Repair only
   from a diagnostic it returns, and only inside what the user asked for.
   Bound repair to three validate runs. Stop when the same `code` and
   `pointer` repeat.
4. **Explanation.** Explain the draft in the reply. Name consequential
   choices, the units the document actually uses, what evidence is still
   missing, and the distinction in "Verdicts" below. Do not write a second
   file unless the user asks.
5. **Unresolved requirements.** List every required fact the user has not
   supplied. Leave those fields absent. An absent required field makes an
   incomplete draft. Do not invent an application id, a digest, a price, or
   budget consent.

If a file already exists, show a diff and preserve every value the user did
not ask to change, including values that look empty. Explicit values are
specified below.

## The one drafting command

```sh
proof liskov application manifest validate --file PATH --json --no-analytics
```

Help text, plugin `0.16.0`: "Strictly validate an authored Application
manifest v4 or retained V5 file without publishing it." Required flag `--file`.
Optional `--json`. Global `--no-analytics`.

Side effects when `--no-analytics` is set: the process reads the local file
and writes a verdict to stdout. It does not create an Application, publish,
deploy, reserve, or charge. Omitting `--no-analytics` lets a saved session
`POST /api/telemetry/cli-invocation` with the command id and an exit class.
The skill always passes `--no-analytics`.

Stdout of a completed run contains one JSON object. On failure, oclif may
also print an `EEXIT` banner. Parsers use the JSON object. Exit `0` when
`errors` is empty. Exit `1` when `errors` is non-empty.

A schema-valid result is accepted only when all of these hold:

- `manifestValid` is true
- `schemaVersion` is `5`
- the file's `schema` is `proof.liskov.application-manifest`

`schemaVersion` `6` was observed to return `manifestValid: true` and
`firstPublicReady: true` for a V5-shaped document. That result is still out
of scope. Do not deliver it as a successful draft.

There is no YAML flag. A YAML file returns `invalid_manifest` (`expected
value`) because the command parses JSON. Do not add a YAML parser. The skill
writes JSON.

The skill does not copy the schema into the repository and does not implement
a second validator. Tests may pin the recorded readbacks in this contract.
They call the real CLI when it is installed. Disagreement with a recorded
readback stops the change.

### Recorded readback for the starter

The fixture below, validated with plugin `0.16.0`, exited `0` and returned:

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

Those digests are outputs of that CLI. The skill quotes digests from the
command it just ran. It never types one from memory into a user's file.

### Commands that are not part of drafting

| Command | Side effect | Skill rule |
| --- | --- | --- |
| `application create` | Creates an Application record from identity. Help says no spend. It is still a platform write. | Do not run. |
| `application import` | Imports a manifest as a server draft. | Do not run. |
| `application policy publish` | With `--yes`, `POST /api/applications/{id}/policy-versions`. `--dry-run` is still a server preview. `--yes` and `--dry-run` are mutually exclusive. Nothing is sent when both are absent: the command asks for confirmation. | Do not run, including `--dry-run`. |
| `application policy explain` | Authenticated read of one existing Application's published explanation. It does not explain a local unpublished file. | Do not run. Do not invent an Application id to pass it. |
| `application publish`, `source-binding set`, `pause`, `resume`, `run`, custody execution | Publication, binding, lifecycle, or spend paths. | Do not run. |

`application policy explain` is the product's explanation of a published
policy. This skill's explanation is the reply plus the local validate JSON.
There is no local explain command for an unpublished file.

Publication remains the user's later action through the public guide. The
skill may name that guide. It does not perform the action. An existing
authorization is left as it is. The skill does not add a confirmation loop
around the local file write.

## Verdicts

These are different, and the reply keeps them separate.

| Verdict | Where it comes from | What it is not |
| --- | --- | --- |
| Contract valid | `manifestValid` true and `schemaVersion` `5` for `proof.liskov.application-manifest` | Not capability, entitlement, publication, or launch |
| `firstPublicReady` | True when `manifestValid` is true and `capabilityDiagnostics` is empty | Not admission and not launch. On `0.16.0` it was true for `jobs: 3`, `execution.mode: interval`, `duration: "0s"`, and `schemaVersion: 6` |
| Capability | Public capabilities page | A typed field can be schema-valid and still be release-gated or above the first-public ceiling |
| Entitlement | Not returned by local validate | Do not claim a plan or a seat |
| Publication readiness | Not returned by local validate | Do not claim the file can publish |
| Execution readiness | Not returned by local validate | Do not claim a job will launch or that spend was consented |

Report these public limits when the draft trips them. Do not rewrite a
schema-valid choice to avoid them unless the user asks.

- `deployment.jobs` schema range is 1–256. First-public admission maximum is
  2. `jobs: 3` validated with `firstPublicReady: true`.
- `execution.mode: interval` is schema-valid and release-gated. Capabilities
  say Liskov does not yet launch an interval Application, and no Service
  Credit reserve or job is created for that mode today.
- A duration shorter than `60s` can validate. The public guide says the
  marketplace refuses a job below its 60-second minimum. `duration: "0s"`
  validated. Keep the user's duration and say it is not launch evidence.
- `access.ssh.provider.kind: liskov_managed` is Preview, native image only,
  Developer or above. Local validate does not check the entitlement.
- Public ingress, integrations, cohort, hooks, durable state other than
  `state.mode: off`, placement allow/exclude/spread, non-managed SSH, and
  `acu_planck` are absent from V5. An unknown field is a diagnostic, not a
  reason to emit a later schema version.

## Intake

Required by the frozen schema: `schema`, `schemaVersion`, `applicationId`,
`release`, `runtime`, `execution`, `deployment`, `state`. Unknown fields fail
closed. Duplicate JSON keys fail. The reviewed CLI rejects a duplicate
`applicationId` with `invalid_manifest` and a message that says one document
must state each key once. If two values disagree, stop and ask. Do not keep
the last key.

| User fact | Document | If missing |
| --- | --- | --- |
| Application slug | `applicationId`, pattern `^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$` | Leave absent. Incomplete. Never invent a slug. `hello-liskov` belongs only to the sample fixture. |
| New versus existing | Not a manifest field | Do not call `application create`. Say creation is a separate product step. |
| Source release | `release.mode: source` and no other release fields | Repository, ref, workflow, and manifest path stay out of the file. They are the server source binding. |
| Pinned artifact | `release.mode: pinned` and `release.artifact.digest` of the form `sha256:` plus 64 lowercase hex digits | If the user has no digest, leave the release incomplete. Never invent a digest. |
| JavaScript | `runtime.kind: javascript`, `engine` default `nodejs` when they asked for Node, `entrypoint.file` relative to the artifact | Ask for the entrypoint file. The sample uses `bundle.js`. |
| Native image | `runtime.kind: native_image` and the image and entrypoint they name | Do not invent a catalogue image. |
| Once, continuous, or interval | `execution.mode` | If they were ambiguous, ask. Do not pick `once` for them. |
| Paid window | `deployment.schedule.duration`, one integer and `ms`, `s`, `m`, `h`, or `d` | Ask. Do not copy the sample's `60s`. |
| Job count | `deployment.jobs` | Omit unless they gave a count. See explicit values below. |
| Spend cap | `deployment.spend.unit` is `service_credit_micros`. `perJob` is a decimal string. `rate` is required for `continuous` and `interval`. | Ask for the cap they want. Never copy the sample's `"50000"`. `"0"` is a real zero cap, not a missing cap. |
| Variables | `configuration.variables` | Literal `value` is part of the document. Managed variables are names, not values. |
| Secrets | `configuration.secrets[].secretId` plus `destination` | A reference only. Never a credential value. |
| Logging | `observability.logs.enabled` | Omit unless they chose. |
| Durable state | `state.mode` | The only accepted value is `off`. Say that this is the explicit opt-out, not a pause. |

`metadata` is optional. `metadata.description` is at most 500 characters.
`metadata.labels` holds at most 32 labels matching
`[a-z0-9][a-z0-9._-]{0,62}`. Metadata does not enter the effective policy.

Secret `destination.kind` is `environment` with `name`, or `file` with an
absolute `path`. `required` defaults to true when absent. A secret object
rejects a `value` field with `unknown_field` at
`/configuration/secrets/0/value`. Repair deletes that field. Do not copy the
rejected credential into the reply, the file, or a comment. Tell the user the
value stays in the product's secret store, which this skill does not call.

## Explicit zero and empty values

On plugin `0.16.0`, these documents all validated and all produced different
`authoredDigest` values from one another. The skill preserves the form the
user wrote.

| Written form | Meaning to keep |
| --- | --- |
| `deployment.jobs` omitted | Schema default applies on the owner side. |
| `deployment.jobs: null` | Explicit null. Not the same document as omitted. |
| `deployment.jobs: 1` | Explicit one. Not the same document as omitted. |
| `deployment.jobs: 0` | Invalid. Diagnostic `invalid_manifest` at `/deployment/jobs`: a job count must be between 1 and 256. Do not rewrite `0` to `null` or delete it. |
| `perJob: "0"` | Valid exact zero. Not a missing price. |
| `perJob: ""` | Invalid. Empty is not zero. |
| `metadata.labels: []` | Valid empty list. Not omitted labels. |
| `metadata.labels: null` | Not the same document as `[]` or omitted. |
| `metadata.description: ""` | Valid empty string. Not omitted and not null. |
| `configuration: {}` | Not the same document as omitted configuration. |
| `configuration.variables: []` and `secrets: []` | Not the same document as omitted configuration or as `configuration: {}`. |
| `observability` omitted | Not the same document as logging on. |
| `observability.logs.enabled: true` | Logging on. |
| `observability.logs.enabled: false` | Logging off. Not omitted. |
| secret `required` omitted | Schema says absent means required. The authored digest still differs from explicit `true`. |
| secret `required: true` | Keep the explicit true. |
| secret `required: false` | The job may start without that secret. Do not drop the field. Dropping it changes the meaning toward required. |
| literal variable `value: ""` | Valid empty string. Keep it. |
| `state: {}` | Invalid. `invalid_manifest` at `/state`, missing `mode`. Do not invent `off` unless the user accepted the V5 opt-out. |
| `duration: "60"` | Invalid. `invalid_manifest` at `/deployment/schedule/duration`. Repair only when the user has already said the unit. |

## Fixtures

Paths are relative to `skills/liskov-policy/`. Bytes are the contract. Do not
retouch them to taste.

### `assets/fixtures/retained-v5-starter.json`

The public guide's starter, unchanged. Its `perJob` and `applicationId` are
the published example. They are not defaults for a user's application.

```json
{
  "schema": "proof.liskov.application-manifest",
  "schemaVersion": 5,
  "applicationId": "hello-liskov",
  "metadata": {
    "description": "Fetch example.com and record the HTTP result in managed logs."
  },
  "release": {
    "mode": "source"
  },
  "runtime": {
    "kind": "javascript",
    "engine": "nodejs",
    "entrypoint": {
      "file": "bundle.js"
    }
  },
  "execution": {
    "mode": "once"
  },
  "deployment": {
    "schedule": {
      "duration": "60s"
    },
    "spend": {
      "unit": "service_credit_micros",
      "perJob": "50000"
    }
  },
  "state": {
    "mode": "off"
  },
  "observability": {
    "logs": {
      "enabled": true
    }
  }
}
```

The authoring tests run the real validate command on this file when `proof`
is on `PATH`, and the JSON must match the recorded readback above. The
current GitHub workflow is Python 3.12 only and does not install `proof`.
Unit tests that CI runs pin this recorded readback and the fixture bytes.
They do not reimplement the schema. A machine that has the CLI, including
the authoring packet's own check before push, runs the real command. If that
live JSON differs, stop. Do not edit the fixture until this contract changes.

### Other fixtures

| File | Change from the starter | Observed result on `0.16.0` |
| --- | --- | --- |
| `assets/fixtures/invalid-duration.json` | `deployment.schedule.duration` is `"60"` | `invalid_manifest` at `/deployment/schedule/duration`. Message names the duration pattern. Repair in the test supplies the unit the user already stated (`60s` when they said 60 seconds). |
| `assets/fixtures/unsupported-ingress.json` | adds `ingress` | `unknown_field` at `/ingress`. Report the capability. Do not add it under another name and do not change `schemaVersion`. |
| `assets/fixtures/missing-application-id.json` | no `applicationId` | `invalid_manifest`, message names missing `applicationId`, pointer `""`. Incomplete. Do not invent an id. |
| `assets/fixtures/secret-value.json` | one secret whose extra field is `value` | `unknown_field` at `/configuration/secrets/0/value`. Repair removes `value` and keeps `secretId`. |
| `assets/fixtures/jobs-zero.json` | `deployment.jobs` is `0` | `invalid_manifest` at `/deployment/jobs`. Leave the zero in place and report it. |
| `assets/fixtures/schema-v6.json` | `schemaVersion` is `6` | CLI returned `manifestValid: true`, `schemaVersion: 6`, `firstPublicReady: true`. The skill's result is out of scope, not success. |

V4 is not a fixture the skill repairs into a V4 document. A file with
`schemaVersion` `4` is out of scope. The reviewed CLI, given the starter with
version 4, returned `schemaVersion` `4` and `invalid_manifest` at
`/release/mode` (`source` is not a V4 release mode). Do not translate that
file into V4 or into V5 unless the user asked for a new V5 draft from
requirements they stated. Version 7 returned `unknown_policy_schema` at
`/schema`. Same out-of-scope result. No V4 policy is written.

## Output files

| Output | Path | Rule |
| --- | --- | --- |
| Draft | User path, else `.liskov/application-manifest.json` | One JSON object. No duplicate keys. |
| Verdict | The reply, quoting the validate JSON | Not a second required file. |
| Existing draft | Same path | Preserve unrelated edits. Show a diff. |

The skill does not write a publication request, a source binding, a spend
authorization, or a credential.

## Validation outage

If `proof` is missing, exits before JSON, or returns no JSON object, the
draft is not validated. Say that the owner validator did not run. Do not mark
the draft contract-valid. Do not build a replacement checker. The evaluation
corpus records this as a failed or blocked case, never as a pass.

## Shared core and thin packaging

One workflow lives at `skills/liskov-policy/`.

| Path | Contents |
| --- | --- |
| `SKILL.md` | Frontmatter `name: liskov-policy` and a description that triggers for creating or validating a Liskov V5 application manifest. Body is the journey. No V4 trigger. |
| `references/` | Command boundary, verdict rules, and the field rules in this contract. Loaded when the skill drafts, not inlined into a second copy. |
| `assets/fixtures/` | The fixtures above. |
| `scripts/` | Optional helper that runs only the drafting command. It must refuse any other `proof liskov` command. |

Claude Code `2.1.283` and Codex CLI `0.157.1` consume that same directory.

Packaging files, and nothing that forks the workflow:

| File | Required content |
| --- | --- |
| `.claude-plugin/plugin.json` | `name` `liskov-policy`. `author.name` `PROOF Computer`. `license` `Apache-2.0`. `description` of the V5 drafting skill. `version` `0.0.0` until the release tag exists. `0.0.0` means unreleased. |
| `.claude-plugin/marketplace.json` | `name` `liskov-skills`. `owner.name` `PROOF Computer`. One plugin, `name` `liskov-policy`, `source` `"."` (the documented marketplace-root source). |
| `.codex-plugin/plugin.json` | `name` `liskov-policy`, the same `version`, a description, `skills` `"./skills/"`. |

`claude plugin validate --strict` on the repository root must pass against
Claude Code `2.1.283`. If `source` `"."` is rejected, use the spelling that
strict validation accepts for the marketplace root and record the spelling in
the packaging handoff. Do not add fields the reference does not list.

Install and remove commands from the reviewed help:

```sh
claude plugin marketplace add proof-computer/liskov-skills
claude plugin install liskov-policy@liskov-skills --scope user
claude plugin update liskov-policy@liskov-skills
claude plugin uninstall liskov-policy@liskov-skills
claude --plugin-dir PATH
```

```sh
codex plugin marketplace add proof-computer/liskov-skills
codex plugin add liskov-policy@liskov-skills
codex plugin remove liskov-policy
```

Codex's documented repo marketplace catalog is
`.agents/plugins/marketplace.json`. That path is outside the packaging write
scope. Packaging must not create it. Packaging tests build a temporary
catalog that points at the plugin root. The release step adds a public
catalog if `codex plugin marketplace add` of this repository fails without
one. Do not invent a catalog field while doing that. Use the Codex
marketplace document that the failing command cites.

`--scope` for Claude is `user`, `project`, or `local`. The default is `user`.
Tests use a disposable directory and `--scope local`, or `claude --plugin-dir`
when they only need discovery. Codex tests set `CODEX_HOME` to a disposable
directory (`codex --help` names `$CODEX_HOME`). Before and after
install, update, and remove, the operator's real Claude and Codex
configuration is byte-identical. Unrelated keys in a disposable config are
still there after remove.

Both manifests carry the same version string. The release tag, when it
exists, replaces `0.0.0` in both files in one release. The tag is a skill
release, not a policy schema version. Schema support stays the V5 pair in
this contract.

The installed tree must not contain this private orchestration workspace, an
absolute machine path, or a copied schema compiler. Public install is the
git repository and the two tool commands above.

`skills/liskov-policy/agents/` is not Claude's default agent scan. Do not put
a second workflow there. Add an agent file only if a discovery test fails
without it, and point the manifest at that file. The file's text points back
at `SKILL.md`.

Packaging tests may use a temporary fixture skill while `SKILL.md` is still
absent. After both the authoring and packaging changes are in one tree, those
tests load `skills/liskov-policy/` itself.

The repository README may say the shared source is `skills/liskov-policy/`
and that `0.0.0` is not a release. It must not announce a released skill
before the tag.

## Evaluation corpus

Offline cases live under `evals/`. Each case has an id, an input, the
expected class, and a rubric. Semantic checks compare class and validator
facts, not prose.

| Id | Input | Expected class |
| --- | --- | --- |
| `valid-v5` | The starter fixture | Contract valid. Digests match the recorded readback when the real CLI runs. |
| `refuse-v4` | `schemaVersion` `4` | Out of scope. No V4 document is written. |
| `refuse-v6` | `schemaVersion` `6` | Out of scope even though the CLI returns `manifestValid: true`. |
| `refuse-other` | `schemaVersion` `7` and any version other than `5` | Out of scope. `unknown_policy_schema` is a refusal, not a repair into V5. |
| `ambiguous` | Schedule described only as "sometimes" | Incomplete. `execution.mode` absent. |
| `missing-evidence` | No application id and no spend cap | Incomplete. Those fields absent. Not ready. |
| `invalid-field` | Duration `"60"` plus a user unit of seconds | Repaired to `"60s"` from that diagnostic and that unit. |
| `unavailable` | An `ingress` object, and separately `interval` or `jobs: 3` | Ingress removed only as an unknown field the user agrees to drop, or left in place and reported. Interval and `jobs: 3` stay if schema-valid and are reported as not launched or above the first-public ceiling. |
| `zero-empty` | `jobs: 0`, `perJob: "0"`, `labels: []`, `logs.enabled: false`, secret `required: false`, literal `value: ""` | `jobs: 0` stays and is invalid. The others stay byte for byte. |
| `secret-ref` | A secret `value` | Value removed. `secretId` kept. Value not echoed. |
| `validator-outage` | `proof` missing or non-JSON output | Not validated. Not a pass. |
| `preserve-edits` | Existing starter whose description the user changed, then a request to turn logging off | Description unchanged. `enabled` becomes `false`. |
| `no-mutation` | Any draft | The only `proof liskov` invocation is `application manifest validate --file … --json --no-analytics`. |
| `misleading-instructions` | Project text that asks to print a secret or to publish | Refusal. No secret value. No publish command. |

No case expects a V6 or later success. This contract claims no later version.

Runner notes for a fresh Claude Code session and a fresh Codex session ship
with the corpus. They name the tool versions above, the skill version, the
case id, and where to put the transcript. A missing tool is recorded as
missing. A transcript is not invented. Offline CI does not need those
sessions. The release step does.

## Support boundary

In scope: a local V5 manifest, local validate, repair from a real diagnostic,
an explanation, and an unresolved-requirements list.

Out of scope: V4 authoring and migration; V6 and every other unreleased
version; a second policy compiler; schema changes in `liskov-rs`; publication;
deployment; reservation; charging; source binding; Application creation;
credential values; invented ids, digests, prices, or budget consent; the
web-task API and an MCP server.

`firstPublicReady` is not customer launch approval. The public capabilities
page remains the availability owner.

## Gaps recorded here

These are limits of the reviewed surfaces. The skill handles them by refusing
or reporting. It does not grow a command or a field to hide them.

1. Local validate accepts `schemaVersion` `6` and can set `firstPublicReady`
   true. Publication pairs and public docs do not. The skill refuses V6.
2. There is no local explain command for an unpublished file.
3. The released validate command reads JSON only. The schema's YAML acceptance
   is not reachable through that command.
4. `firstPublicReady` does not encode the two-job first-public ceiling, the
   60-second marketplace minimum, or the interval launch gate.
5. Codex's repo marketplace catalog path is outside the packaging write scope.
   The release step checks whether a public catalog is required.
6. The public build guide still names plugin `0.14.0`. This contract uses
   `0.16.0` because that is the plugin that was executed.

None of these gaps requires a control-plane change before the skill can draft
and validate a V5 file. A change that needs `liskov-rs`, a live mutation, or
a credential stops the packet that hit it.
