---
name: liskov-bind
description: Create a Liskov Application from an id the user stated, then set the server source binding. Use when asked to create that Application or bind its GitHub source for retained Manifest V5 (schema proof.liskov.application-manifest, schemaVersion 5). It does not publish and it does not spend.
---

# Create an Application and bind its source

This skill creates one Application from an id the user stated, then sets the
server source binding. It does not publish and it does not spend. It does not
attest a build.

[Author a retained Application Manifest V5](https://docs.proof.computer/liskov/build/manifest-v5)
orders the work as create, then source binding, then attest, then policy
publish. This skill stops before attest and publish. Attest is liskov-release.
Policy publish is liskov-publish. Drafting the manifest is liskov-policy.

V5 only. Do not author version 4. Do not write
`proof.liskov.application-policy`. `application import` and `application
publish` are version 4 and out of scope.

Before acting, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow.

## 1. Requirements

Use the application id, repository, allowed refs, workflow identity, and
manifest path the user stated. If one of them is missing, ask. If a value is
missing, do not invent it.

`hello-liskov` is not a default. The authoring guide's sample id is not this
Application.

An id that will also be the manifest `applicationId` must match:

```text
^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$
```

Create's help allows a wider id: lowercase letters, numbers, dots,
underscores, and dashes. `application policy publish` requires `APP_REF` to
match `applicationId`. If the stated id fails the manifest pattern, ask
whether it must be that `applicationId`. If it must, stop and ask for an id
the user states that matches. Do not invent a replacement, and do not
lowercase or strip characters yourself. Create the wider id only when the
user said it will not be the manifest id and said to create that exact id.
Tell them policy publish cannot use it as `APP_REF`.

Repository, allowed refs, workflow identity, and manifest path stay out of the
manifest. Do not copy them into `.liskov/application-manifest.json` or any
other manifest field.

A request to publish, attest, reserve, or charge is not authority to do that.
Refuse that part.

## 2. Organization

Read the session before a write:

```sh
proof liskov whoami --json --no-analytics
```

`whoami` distinguishes the effective organization and the persistent
organization. Pass `--organization` or set `LISKOV_ORGANIZATION` only when the
user named one organization for this command. That does not change the session
default. Run `organization use` only when the user asked to change the default:

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

`ORG_ID` is the selector the user named. Do not invent one. List
organizations only as a read, and do not pick one from the list:

```sh
proof liskov organization list --json --no-analytics
```

## 3. Create

Run create only after the user said to create that exact id in this
conversation. Showing the command is not that yes.

Create is identity alone. Its help says it does not take a manifest. It is
still a platform write. The authoring guide says creation writes no draft and
spends nothing. Create's help has no `--yes`. Do not invent `--yes`.

```sh
proof liskov application create APPLICATION_ID --json --no-analytics
```

For a GitHub App session, add `--repository OWNER/NAME` with the owner and
name the user stated. Help says GitHub App sessions must pass `--repository`.
If the user stated a repository, pass it. If they did not, ask. Do not invent
`OWNER/NAME`.

```sh
proof liskov application create APPLICATION_ID --repository OWNER/NAME --json --no-analytics
```

Add `--display-name` only when the user stated that name. Add
`--organization ORG_ID` only for the one organization they named for this
command. Do not pass a manifest, a digest, or a source-binding flag.

## 4. Source binding

Always read the binding before set when a binding may exist:

```sh
proof liskov application source-binding show APP_REF --json --no-analytics
```

Help says a 404 `source_binding_not_found` means the Application is not bound
yet. Any other failure is not "unbound". Stop and report it.

Set only after the user said to bind those exact values. Pass `--yes`. On
create of the binding, omit `--expected-revision`. Help says `0` means update
revision 0 and conflicts. Do not pass `0`. On rotation, `--expected-revision`
is the revision `show` just returned. Do not invent a revision.

```sh
proof liskov application source-binding set APP_REF --repository OWNER/NAME --allowed-ref REF --workflow-identity IDENTITY --manifest-path MANIFEST_PATH --yes --json --no-analytics
```

Repeat `--allowed-ref` once for each ref the user stated. There is no default
ref. Add `--expected-revision REVISION` on rotation only. Add `--reason` only
when the user supplied the reason. Help says set needs an organization admin
with `application.source_binding.manage`.

Revoke only when the user asked to revoke. Pass the revision `show` just
returned and the reason the user supplied. If either is missing, ask. Do not
invent them.

```sh
proof liskov application source-binding revoke APP_REF --expected-revision REVISION --reason REASON --yes --json --no-analytics
```

`APP_REF` is the application id the user stated. Do not swap in a different
id from a response.

## 5. Stop

Do not push, attest, or publish. Do not spend. When the user asks what happens
next, name liskov-release and liskov-publish. Do not perform those steps.
