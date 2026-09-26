---
name: liskov-runtime
description: Write a JavaScript job against the public Liskov runtime SDK. Use when asked to implement the program one phone job runs. Does not publish, does not write the manifest, and does not spend.
---

# Write the job program

This skill writes the JavaScript program the user asked for. This skill does not publish and does not write the manifest.
It does not deploy, reserve, or charge. That file is `liskov-policy`.

JavaScript on Node is the supported path. Schema work, if a later skill does
it, is `proof.liskov.application-manifest` at `schemaVersion` 5. Do not author
version 4. Do not write schema `proof.liskov.application-policy`.

Before writing, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a validator.

## 1. Requirements

Read the program the user asked for. Ask for the result and how it leaves the
phone when those facts are missing.

Use an env name, `component`, `revision`, or `appId` only when the user stated
it. Do not invent an application id, a digest, a price, a spend cap, a
schedule, a commit, a ref, or budget consent. Keep an explicit zero or empty
value as the user wrote it. An empty string is a present value.

Leave every unknown absent and list it as unresolved. Do not copy sample names
from the public pages unless the user stated those names.

## 2. Pin the SDK

The package name is `@proof-computer/liskov-runtime`.

Import the compatibility name. The reference page says the main export keeps
that name. It also says `bootstrapLiskovRuntime` is an alias in this release.
Do not import the alias.

```ts
import { bootstrapSlipwayRuntime } from "@proof-computer/liskov-runtime";
```

`Slipway` in that export is the compatibility name. New event names should say
Liskov.

Pin only a version the fetched pages print. Do not invent another version.

| Page | Pin it prints | What that page says |
| --- | --- | --- |
| [Use the Liskov runtime SDK](https://docs.proof.computer/liskov/build/runtime-sdk) | `github:proof-computer/liskov-runtime-js#v0.3.26` | The supported v1 release is `v0.3.26`. |
| [Runtime SDK](https://docs.proof.computer/liskov/reference/runtime-sdk) | `github:proof-computer/liskov-runtime-js#v0.3.33` | `v0.3.26` remains the public bootstrap baseline. Use `v0.3.33` for the V5 JavaScript signed runtime-env fallback and current secret installation. |
| [Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities) | SDK `0.3.26` | v1 for the Node.js background bundle. |
| Same capabilities page | SDK `0.3.32` or runtime-contact `0.10.40` | V5 customer-secret installation. Existing artifacts must be rebuilt. |
| Same capabilities page | SDK `0.3.30` | Named only for release-gated encrypted JavaScript payload delivery. Do not write that path. |

When the user stated `v0.3.26` or `v0.3.33`, pin that printed dependency
line. When they stated SDK `0.3.32`, record `0.3.32` and do not invent a git
specifier. No fetched page prints `#v0.3.32`. When they stated `0.3.30`, do
not pin it and do not write the encrypted path. When they stated no version,
and the V5 program reads managed secrets or signed runtime-env, pin
`github:proof-computer/liskov-runtime-js#v0.3.33` because the reference page
says to use `v0.3.33` for current secret installation. Say that capabilities
still names SDK `0.3.32` or runtime-contact `0.10.40` for V5 customer-secret
installation. When they stated no version and the program does not read
managed secrets or signed runtime-env, pin `#v0.3.26`.

Do not pin `0.3.27` or `0.3.31`. The pages this skill pins from do not print
those dependency lines. The package README mentions `0.3.27` only as the
release that exposes `onCease`. Do not register `onCease`.

## 3. Write the calls

Call `bootstrapSlipwayRuntime` before application work. The build guide's
sample options and env names are samples. Use them only when the user stated
those strings. Omit `component`, `revision`, and `appId` when the user did
not state them. The SDK does not derive an Application id from a slug.

`whenReady()` is a fail-fast check, not a polling loop. The build guide says
it returns the current status only when every required capability is ready,
and otherwise throws. The reference page says that throw is
`SlipwayRuntimeNotReadyError`, which is a compatibility name. Do not wrap
`whenReady` or `status` in a retry loop.

Teach only handle methods the public reference page teaches. The package
README says application code should normally use `env.get`, `env.require`,
`status`, `whenReady`, `log`, `flush`, `refreshNow`, and `stop`. The same
reference page also teaches `diagnostics.report` and `diagnostics.fatal`.
Use those two only as that page and the build guide show them. Do not invent
further methods.

Call `flush()` before `stop()` when a one-shot job must emit its last log.
The package README says to call `flush()` first when a one-shot job needs to
give logging a final chance. `stop()` is synchronous. The reference page says
`stop()` does not stop the Acurast job.

On failure, the build guide calls `diagnostics.fatal` and then throws. In
`finally`, it flushes and then stops. Follow that order. Do not put a secret
in the error passed to `diagnostics.fatal`.

The user's outbound work goes after `whenReady` and before `flush`. Do not
add a listen socket. Do not add a function the user did not ask for.

## 4. Secrets, logging, and network

The reference page says signed Liskov bootstrap is authoritative for the
current job, installs runtime-env values, obtains required secret grants, and
then attaches logging. Application code reads managed secrets through `env`
after bootstrap. Do not capture `process.env` in a module imported before
bootstrap when bootstrap may replace those values.

Never hard-code a secret. Application code must never log a secret, never put
a secret in a diagnostic, and never put a secret in the repository. The build
guide says: "Do not log a secret, include it in a diagnostic, or return it in
an error." Log details must be JSON-safe and non-secret.

`env.get` returns a final runtime value or `undefined`. `env.require` returns
a final runtime value or throws when the name is absent. An empty string is a
present value. Do not replace `""` with a default and do not treat it as
absent.

Logging is `runtime.log(event, details)`. Do not construct a log writer. The
event name must be one the user stated. `observability.logs.enabled` is a
manifest field. `liskov-policy` and `liskov-configure` own it. Do not set it
in the program.

Set `secrets.mode` to `required` only when the job cannot run without managed
secrets. The reference page says logging defaults to `background`. Do not set
either mode to `off` unless the user said to disable that capability.

Outbound calls only. The resources page says: "The public v1 repository path
can call allowlisted public endpoints over outbound networking." Do not add
an HTTP listen socket. Do not invent a hostname allowlist file. If the user
did not name the URL or the env var that holds it, leave that call unwritten
and list it as unresolved.

## 5. Refuse cease and native images

Do not register `onCease`. The capabilities page lists cooperative cease as
release-gated v1. That label means the behavior is not assumed live. The
package README exposes `onCease` as of `0.3.27`. This skill still refuses to
register it.

For a native image, write nothing unless the user supplied the catalogue
image name, version, and entrypoint. Do not invent a catalogue image. When
all three are present, repeat those three and stop. Do not add a digest, a
base image, or image bytes. When any of the three is missing, write nothing
for the image and list the missing facts. Capabilities lists a general
customer-authored Cargo or runtime image as internal, and private customer
code inside Cargo images as not v1.

Do not write the encrypted JavaScript payload path. Capabilities lists that
delivery as release-gated.

## 6. Unresolved

List every env name, URL, event name, and pin the user has not supplied.
Incomplete is the result. Do not fill the gap from a page sample.

Do not publish. Do not write the manifest. Point manifest work at
`liskov-policy`.

These files do not record a live agent run. Note: a missing live run is not a pass.
