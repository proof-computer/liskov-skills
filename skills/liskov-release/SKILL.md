---
name: liskov-release
description: Put a customer's build in GitHub by pinning to IPFS and attesting with GitHub OIDC, with no spend credential in the workflow. Use when asked for that caller workflow. Does not publish and does not bind source.
---

# Pin and attest on GitHub

This skill writes the caller's GitHub workflow for an IPFS pin and a GitHub
OIDC attestation. The workflow has no spend credential. This skill does not
publish, import, deploy, reserve, or charge.

It does not write the manifest. That file is `liskov-policy`. It does not set
the server source binding. That later admin step is `liskov-bind`. Do not run
that step.

Schema work, when a later skill does it, is
`proof.liskov.application-manifest` at `schemaVersion` 5. Do not author version
4. Do not write schema `proof.liskov.application-policy`.

Before writing, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a validator.

## 1. Requirements

Collect the workflow path, Application id, entrypoint, manifest path, working
directory, git ref, and whether the user asked for the security-sensitive pin
or a custom IPFS proxy.

Do not invent an application id, a digest, a price, a spend cap, a schedule,
a commit, a ref, or budget consent. Keep an explicit zero or empty value as
the user wrote it. Leave every unknown absent and list it as unresolved.

The actions page sample uses Application id `status-worker`, entrypoint
`app.cjs`, manifest path `.liskov/application-manifest.json`, working
directory `.`, and branch `main`. Those are samples. Use one of them only
when the user stated that value.

## 2. Choose the uses revision

Copy the revision from
[Build and attest with GitHub Actions](https://docs.proof.computer/liskov/build/github-actions).
Do not invent a tag or a commit.

The page says the moving `v1` release is live, that production acceptance
recorded for this contract used `v1.2.2`, and that callers should use `@v1`
to receive compatible v1 fixes. Security-sensitive callers may instead pin
the reviewed commit `cbca2cde077df0cfd6be894519c6f8e4915e386a` and update it
deliberately.

| Caller asked | `uses` revision to write |
| --- | --- |
| Nothing about a pin, or the moving release | `proof-computer/liskov-github-actions/.github/workflows/acurast-app.yml@v1` |
| A security-sensitive pin | The same workflow path, with the page's reviewed commit in place of `@v1` |

The workflow file name `acurast-app.yml` is the path that page prints.

Do not rewrite `@v1` to `@v1.2.2`. Capabilities says the moving `v1` tag was
verified at `v1.3.2`, and that `liskov-github-actions` `v1.2.4` contains the
exact-bound import (`aa1b83f`). Those are records on the capabilities page.
They are not the uses revision the actions page says to write. `aa1b83f` is
not an artifact digest. When a digest is not in hand, do not invent a digest.

## 3. Write the workflow

Write a workflow file only when the user gave a path. If they gave no path,
do not write a file.

When they gave a path, write that file and no other:

- `permissions` are `contents: read` and `id-token: write`. That is GitHub
  OIDC for the attestation the page shows. It is not a Liskov API token and
  not a spend credential. Do not remove it.
- `uses` is the revision chosen above.
- Add a `with` key only for a value the user stated. The page's caller
  sample shows `app-id`, `working-directory`, `entrypoint`, and
  `authored-manifest-path`. The reusable workflow also accepts
  `node-version` and `pnpm-version`. Write either only when the user stated
  that version. Do not write the workflow's own default `"24"`. Do not
  invent any other input key.
- Add a `push` branch only when the user stated that ref. Do not default the
  branch to `main`.
- Add `workflow_dispatch` only when the user asked for a manual run.

The page says the called workflow installs the requested pnpm and Node.js
versions. When the user stated a Node version, the input key is
`node-version`. When they stated a pnpm version, the input key is
`pnpm-version`. Leave the key absent when they did not state a version.

The called workflow runs `pnpm install --frozen-lockfile`, typecheck, test,
and build, then uploads the bundle to the Acurast IPFS proxy without
spending, then attests the CID, the SHA-256 digest, the manifest digests,
and the GitHub OIDC identity. Do not replace pnpm with another installer.
If the repository has no `pnpm-lock.yaml`, say so and leave that mismatch
unresolved.

A file that omits an unknown key is incomplete. Say that. Do not call it
ready.

The workflow must not contain a Liskov API token, a service-credit key, a
publish step, or a `proof liskov` publish, create, or source-binding command.
It must not contain any `proof liskov` command. The default IPFS proxy
requires no repository secret. Do not add `ACURAST_IPFS_URL` or
`ACURAST_IPFS_API_KEY` unless the user asked for a custom proxy. Those names
authorize upload to that proxy, not Acurast spend and not Liskov policy
publication. Never write the key's value into the workflow or the reply.

## 4. What the pin proves

The artifact digest proves those bytes. The GitHub OIDC attestation recorded
with that pin proves that workflow and that ref: the repository, ref, commit,
and workflow identity GitHub saw. It does not prove source privacy, a running
job, or a charge. It does not prove a deployment, a processor assignment, or
a runtime instance. It does not prove a reserve or a final charge.

Do not type a CID, an artifact digest, or an `artifact-version-id` into the
workflow or the manifest. The actions page says the Attest artifact pin step
reports that id. Quote an id or a digest only from a run the user shows.
Otherwise do not invent a digest.

[Artifacts, encryption, and provenance](https://docs.proof.computer/liskov/build/artifacts-provenance)
says current IPFS Application bytes are not a private-code mechanism, even
when the source repository is private. The reusable pin action requires
`none` and rejects an `aes256_gcm` build requirement. Do not add an
encryption input. Do not claim the build makes the source private. Encrypted
JavaScript payload delivery is release-gated on the capabilities page. Do
not write that recipe.

## 5. Source binding stays out of the manifest

Repository, ref, workflow identity, and manifest path are the server source
binding. They stay out of the manifest. Capabilities says an organization
admin binds repository, allowed refs, workflow identity, and manifest path
before publication, and every build attests them. The actions page says the
caller should use the same Application id, repository, ref, workflow path,
and manifest path as the manifest's builder block. This skill does not write
a builder block and does not write the manifest. It cannot confirm that
block as a field of `proof.liskov.application-manifest` from the release
pages. Leave those facts out of the manifest.

Name `liskov-bind` as the later admin step. Do not run it. Do not invent the
binding. Publication is `liskov-publish`. This skill does not publish. The
actions page points at a validate, import, and publish guide. Do not import.
Do not follow that guide into a publish step.

## 6. Unresolved

List every missing path, Application id, entrypoint, manifest path, ref, and
any digest the user expected you to already know. Incomplete is the result.
Do not fill the gap from the page sample.

These files do not record a live agent run. Note: a missing live run is not a pass.
