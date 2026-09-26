# Limits

Use these while choosing the id and the binding. They are not a validator.
This skill does not copy a schema and does not implement one.

## Manifest id

The manifest `applicationId` pattern is:

```text
^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$
```

The [manifest reference](https://docs.proof.computer/liskov/reference/manifest-v5)
calls that field an organization-local slug of 1–63 lowercase letters, digits,
and hyphens. Create's help allows a wider id: lowercase letters, numbers,
dots, underscores, and dashes.

| Stated id | Action |
| --- | --- |
| Matches the manifest pattern, and the user said to create it | Create that id. |
| Fails the pattern, and they have not said whether it is the manifest `applicationId` | Ask. Do not create yet. |
| Fails the pattern, and it must be `applicationId` | Stop. Policy publish requires `APP_REF` to match `applicationId`. Do not invent a replacement. |
| Uses only the wider create alphabet, is not a manifest id, and they said to create that exact id | Create allows lowercase letters, numbers, dots, underscores, and dashes. Say policy publish cannot use it as `APP_REF`. |
| Uppercase, empty, or longer than either rule | Stop. Ask. Do not rewrite it. |
| Not stated | Ask. Do not invent one. `hello-liskov` is not a default. |

Do not create an id the user did not state, even when they said "create
something" or pointed at the authoring guide's sample.

## Binding facts stay out of the manifest

The [authoring guide](https://docs.proof.computer/liskov/build/manifest-v5)
says the repository, ref, workflow identity, manifest path, and artifact
digest do not belong in the manifest. They are bound to the Application, and
every build attests them.

| User fact | Command | Manifest |
| --- | --- | --- |
| Repository `owner/name` | `--repository` on create when required, and on set | Stays out of the manifest. |
| Allowed ref | Repeatable `--allowed-ref` | Stays out of the manifest. |
| Workflow identity | `--workflow-identity` | Stays out of the manifest. |
| Manifest path | `--manifest-path`, a safe relative path | Stays out of the manifest. Do not rewrite it into `.liskov/application-manifest.json` unless the user stated that path. |
| Artifact digest, commit, pointer | Not this skill | Do not invent one, and do not write one into a file. |

An absolute manifest path is not the safe relative path help asks for. Ask
for a relative path. Do not invent one.

The guide's workflow-identity shape is `OWNER/REPO/.github/workflows/FILE.yml@REF`.
Use only the identity string the user stated. Do not invent the file name,
the ref, or the `@` suffix.

Allowed refs have no default. Do not assume `refs/heads/main`.

## What this skill does not decide

Launch ceilings, interval availability, and the marketplace duration minimum
belong to publication. Do not "fix" a manifest so a later publish will pass.
Do not publish. Do not spend.

Attest is liskov-release. Policy publish is liskov-publish. See
[Command boundary](command-boundary.md).
