# Limits

Read this while writing the program. It is not a second workflow. See
[Command boundary](command-boundary.md).

## Versions

Do not invent a version. The pages below disagree on purpose. Say which row
you used.

| Source | Printed pin | Use it when |
| --- | --- | --- |
| Build guide, supported v1 | `github:proof-computer/liskov-runtime-js#v0.3.26` | The user asked for the v1 baseline, or the program does not read managed secrets or signed runtime-env and they named no version. |
| Reference page, current secret installation | `github:proof-computer/liskov-runtime-js#v0.3.33` | V5 JavaScript that reads managed secrets or signed runtime-env, and the user named no version. |
| Capabilities, Node.js bundle | SDK `0.3.26` is v1 | Do not pretend a later pin erases this row. Say it. |
| Capabilities, V5 customer secrets | runtime-contact `0.10.40` or SDK `0.3.32` | Say this row when pinning `v0.3.33`. If the user stated `0.3.32`, record `0.3.32`. Do not invent `#v0.3.32`. |
| Capabilities, encrypted payload | Actions `v1.3.2` and SDK `0.3.30`, release-gated | Do not write that path. Do not pin `0.3.30` for an ordinary job. |

The reference page says: version `v0.3.26` remains the public bootstrap
baseline. Use `v0.3.33` for the V5 JavaScript signed runtime-env fallback and
current secret installation.

Import only:

```ts
import { bootstrapSlipwayRuntime } from "@proof-computer/liskov-runtime";
```

That export is the compatibility name. Do not import `bootstrapLiskovRuntime`.

## Handle

The reference page's customer handle, limited to methods that page teaches:

| Member | Contract on that page |
| --- | --- |
| `env.get(name)` | Return a final runtime value or `undefined`. |
| `env.require(name)` | Return a final runtime value or throw when absent. |
| `status()` | Return current identity, blockers, and capability states. |
| `whenReady()` | Resolve immediately when required capabilities are ready; otherwise throw `SlipwayRuntimeNotReadyError`. |
| `log(event, details?, options?)` | Emit a structured Liskov log record. |
| `flush()` | Bounded log flush returning counts and state. |
| `refreshNow()` | Refresh runtime env, make one eligible background-secret attempt, then refresh logging. |
| `diagnostics.report(...)` | Send an ordinary bounded signed diagnostic. |
| `diagnostics.fatal(...)` | First-call-wins terminal boundary. |
| `stop()` | Synchronously and idempotently stop SDK timers and retries. |

The package README's normal application calls are `env`, `status`,
`whenReady`, `log`, `flush`, `refreshNow`, and `stop`. Do not add methods
that are absent from the reference page.

`whenReady()` fails fast. It is not a poll loop. Do not loop on `status`.

`home` on that page is the resolved state directory. Do not use it as a
shared disk. Do not invent a filesystem layout under it.

Capability states on that page are `off`, `pending`, `ready`, `degraded`,
`failed`, and `blocked`. `status.ready` is true only when every required
capability is ready.

## Page sample, not a default

The build guide shows this shape. `worker`, `APP_REVISION`, `API_ENDPOINT`,
`API_TOKEN`, `worker.ready`, and `application_failed` are that page's sample.
Use one of them only when the user stated that string. `runWorker` is the
page's stand-in for the user's program. Do not log `apiToken`.

```ts
import { bootstrapSlipwayRuntime } from "@proof-computer/liskov-runtime";

const runtime = await bootstrapSlipwayRuntime({
  component: "worker",
  revision: process.env.APP_REVISION,
  secrets: { mode: "required" },
  logging: { mode: "background" },
});

try {
  await runtime.whenReady();
  const endpoint = runtime.env.require("API_ENDPOINT");
  const apiToken = runtime.env.require("API_TOKEN");
  await runtime.log("worker.ready", { endpoint });
  await runWorker({ endpoint, apiToken });
} catch (error) {
  await runtime.diagnostics.fatal({
    kind: "explicit",
    code: "application_failed",
    component: "worker",
    error,
  });
  throw error;
} finally {
  await runtime.flush();
  runtime.stop();
}
```

The reference page's minimal call uses `component` `worker` and `revision`
`release-2026-07-28`. Those are samples too. Do not copy them unless the
user stated them.

`secrets.mode` `required` fails closed. Use it only when the process cannot
run without managed secrets. Logging on the reference page defaults to
`background`. Test hooks stay unset. Do not set a state directory path.

## Secrets

Managed secrets are installed after bootstrap. Read them through `env`.

| Rule | What to do |
| --- | --- |
| Hard-code | Never hard-code a secret. |
| Log or diagnostic | never log a secret. Do not return it in an error. |
| Repository | Never put a secret in the repository. |
| Empty string | An empty string is a present value. Do not replace it. |
| Absent | `env.get` returns `undefined`. `env.require` throws. Do not treat `""` as absent. |

`require` of a name the user did not state is an invented configuration. Leave
it unwritten.

## Logging

`runtime.log(event, details)`. Do not construct a log writer.

`observability.logs.enabled` is a manifest field owned by `liskov-policy` and
`liskov-configure`. Do not set it here.

Call `flush()` before `stop()` when a one-shot job must emit its last log.
`stop()` does not stop the Acurast job.

Severity on the reference page is `debug`, `info`, `warn`, or `error`. Do not
invent another severity. Omit options the user did not ask for.

## Network

Do not add an HTTP listen socket. Outbound calls only.

[Runtime resources and outbound networking](https://docs.proof.computer/liskov/configure/resources-networking)
says the public v1 repository path can call allowlisted public endpoints over
outbound networking. It does not receive a stable public IP, custom hostname,
Liskov HTTP endpoint, or Liskov SSH endpoint. Acurast allowlisting exists.
Do not add an allowlist procedure that page does not print. Retry with
bounded backoff and idempotency, as that page says. Do not invent a retry
count.

The capabilities page lists Liskov-hosted HTTP/SSH ingress as not v1.

## Cooperative cease

Do not register `onCease`.

The capabilities page lists cooperative cease as release-gated v1: accepted
behavior whose final release artifact or rollout is not yet available. Do not
assume it is live. The package README exposes the callback as of `0.3.27`.
That does not make it v1. Refuse the registration. Do not show a sample that
registers it.

## Native image and encryption

| Request | Write |
| --- | --- |
| JavaScript on Node | The program, under the rules above. |
| Native image, missing name, version, or entrypoint | Nothing. List the missing facts. |
| Native image, all three supplied | Those three facts only. No image bytes, digest, or base image. |
| Encrypted JavaScript payload | Nothing. Release-gated. Do not invent the recipe. |
| Ingress adapter or websocket server | Nothing. No public inbound. |

General customer-authored Cargo or runtime images are internal on the
capabilities page. Private customer code inside Cargo images is not v1.

## Values this skill does not invent

An application id, an env name, a URL, an event name, a digest, a price, a
spend cap, a schedule, a commit, a ref, a catalogue image, or budget consent.
Explicit zero and empty values stay as the user wrote them.
