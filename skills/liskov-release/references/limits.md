# Limits

Read this while writing the workflow. It is not a second workflow. See
[Command boundary](command-boundary.md).

## Uses revision

The actions page prints one caller line:

`proof-computer/liskov-github-actions/.github/workflows/acurast-app.yml@v1`

It says callers should use `@v1`. It says security-sensitive callers may
instead pin the reviewed commit
`cbca2cde077df0cfd6be894519c6f8e4915e386a`.

| Printed fact | Where | Write it on `uses`? |
| --- | --- | --- |
| `@v1` | Actions page. Callers should use it. | Yes, unless the user asked for the security-sensitive pin. |
| Commit `cbca2cde077df0cfd6be894519c6f8e4915e386a` | Actions page. Security-sensitive pin. | Yes, only when the user asked for that pin. Same workflow path. |
| `v1.2.2` | Actions page. Production acceptance recorded for this contract. | No. Not the uses revision. |
| `v1.3.2` | Capabilities. Moving `v1` tag verified there. Also named for release-gated encrypted payload execution. | No. |
| `v1.2.4` and `aa1b83f` | Capabilities. Exact-bound import inside `liskov-github-actions`. | No. `aa1b83f` is not an artifact digest. |

Do not invent a tag, a commit, or an artifact digest.

## Page sample, not a default

[Build and attest with GitHub Actions](https://docs.proof.computer/liskov/build/github-actions)
shows this caller. `status-worker`, `app.cjs`,
`.liskov/application-manifest.json`, `.`, and `main` are that page's sample.
Use one of them only when the user stated it.

```yaml
name: Build Liskov Application

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  artifact:
    uses: proof-computer/liskov-github-actions/.github/workflows/acurast-app.yml@v1
    with:
      app-id: status-worker
      working-directory: .
      entrypoint: app.cjs
      authored-manifest-path: .liskov/application-manifest.json
```

When the user gave a path, write a file at that path. Copy `permissions` and
the `uses` path from this sample. Do not copy a sample `with` value or the
branch `main` unless the user stated it. Omit unknown keys. An omitted key
stays unresolved. Explicit empty values stay empty. Do not replace them with
the sample.

The only `with` keys this sample shows are `app-id`, `working-directory`,
`entrypoint`, and `authored-manifest-path`. The page says a monorepo sets
`working-directory` to the directory that contains `package.json` and
`pnpm-lock.yaml`. Do not invent a directory. The caller sample does not
show `node-version` or `pnpm-version`. The reusable workflow accepts both.
Write one only when the user stated that version. Do not write `"24"` as a
default.

## No spend credential

The actions page says: "You do not store a Liskov bearer token or
spend-capable credential in GitHub."

| Allowed | Not allowed |
| --- | --- |
| `permissions.contents: read` | A Liskov API token |
| `permissions.id-token: write` (GitHub OIDC, not a spend credential) | A service-credit key |
| No repository secret for the default IPFS proxy | A pasted proxy key or URL value |
| `ACURAST_IPFS_URL` and `ACURAST_IPFS_API_KEY` only if the user asked for a custom proxy, as names, never as values | A publish step, a create step, or a source-binding step |

The page says those two custom-proxy names authorize upload to that proxy,
not Acurast spend and not Liskov policy publication. They are still secrets.
Do not echo a value the user pasted.

The called workflow uploads without spending. It does not reserve a USD
Service Credit, select a deployment schedule, or register a job. Do not add
those steps.

## What a digest proves

[Artifacts, encryption, and provenance](https://docs.proof.computer/liskov/build/artifacts-provenance)
separates the evidence. Do not collapse a row into a claim that page rejects.

| Evidence | Proves | Does not prove |
| --- | --- | --- |
| GitHub OIDC | The repository, ref, commit, and workflow identity seen by GitHub. | That the source is safe or correctly reviewed. |
| CID and artifact digest | The exact uploaded bundle bytes. | Who authored those bytes. |
| Artifact version | Liskov's record joining those bytes and accepted provenance. | That a policy selected it. |
| Policy digest | The execution contract for one Application. | That the network accepted or started a job. |
| Job and processor evidence | Registration, schedule, assignment, and network identities. | That application code became ready. |
| Signed runtime contact | A bound runtime instance contacted Liskov and reported capability state. | That every application-level request is correct. |

Say this in the reply: the artifact digest proves those bytes. The OIDC
attestation with that pin proves that workflow and that ref. The pin does
not prove source privacy, a running job, or a charge. It does not prove a
deployment started, a processor assignment, a runtime instance, a reserve,
or a final charge.

The same page says current IPFS Application bytes are not a private-code
mechanism, even when their source repository is private. The reusable pin
action requires `none` and rejects an `aes256_gcm` build requirement. The
complete encrypted path is not supported today. Do not add an encryption
input. Capabilities lists encrypted JavaScript payload delivery as
release-gated. Do not write that recipe.

Quote a CID, an artifact digest, or an `artifact-version-id` only from a run
the user shows. Otherwise do not invent a digest. Do not write one into the
workflow or the manifest.

## Source binding

Repository, ref, workflow identity, and manifest path are the server source
binding. They stay out of the manifest. Do not invent them. `liskov-bind` is
the later admin step. Do not run it.

The actions page says to use the same Application id, repository, ref,
workflow path, and manifest path as the manifest's builder block. This skill
does not write that block. A build from another repo, ref, workflow, or
manifest path must fail even if the bundle filename matches. That is the
artifacts page's rule. It is not permission to publish.

## Triggers and package manager

| User stated | Write |
| --- | --- |
| A branch ref | `push` to that ref only. |
| No ref | No `branches` list. Do not use `main` from the sample. |
| A manual run | `workflow_dispatch`. |
| No manual run | Omit `workflow_dispatch`. |
| No `pnpm-lock.yaml` | Say the called workflow runs `pnpm install --frozen-lockfile`. Do not invent another installer. |

Incomplete is the result when a required input is absent. Do not call the
file ready.
