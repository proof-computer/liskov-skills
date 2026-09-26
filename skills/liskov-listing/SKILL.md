---
name: liskov-listing
description: State the Marketplace release gate and, after a human says a launch already finished, compare running bytes to the public listing. Use when asked about Uptime Prober or OpenClaw. There is no launch command. Does not browse, launch, spend, or store a secret.
---

# State the Marketplace gate

This skill states the Marketplace release gate. After the human says a launch
already finished, it checks the running bytes. It does not launch, browse,
spend, or publish. It does not hand the user a form to fill. Marketplace
launch is release-gated. Naming the gate is not approval to launch.

Before preparing, read and apply:

- [Command boundary](references/command-boundary.md)
- [Limits](references/limits.md)
- [Eval cases](references/eval-cases.md)

Do not copy those rules into a second workflow. Do not implement a second
validator.

## 1. State the gate

Say that curated Marketplace launch and Uptime Prober are release-gated v1,
limited to internal first-party engineering acceptance. They are not a
supported customer offering. Do not enter a Telegram bot token, approve
Marketplace spend, or treat a listing as creating an Application while that
gate stands. Internal acceptance is not permission for a customer to repeat
the journey.

## 2. There is no launch command

There is no Marketplace browse or launch command. There is no launch command.
Where the CLI has no such verb, do not invent one. Do not invent a catalog,
an Application id, a listing version, a price, or a digest the public page
did not print. Do not send the user through a Console form while the gate
stands.

`--organization` or `LISKOV_ORGANIZATION` scopes one later read. Do not run
`organization use` unless the user asked to change the session default.

## 3. Uptime Prober, only when asked

Use Uptime Prober only when the user asked for it. While the gate stands,
state the gate and link the public prober page. Do not restate its option
table, defaults, or prerequisites as fields to enter. Do not add endpoints.

Point at the public source only as a citation. Do not clone it and do not
turn it into a launch. The page prints no price. Do not invent one.

## 4. Secrets stay out of the reply

A Telegram bot token or any other secret is not entered from this skill. Do
not put it in source, a chat field, logs, a support message, the repo, or
the reply. If the user pastes a token, refuse to store it, do not repeat it,
and tell them to rotate it. Do not send them to type it into a Console form
while the gate stands.

## 5. OpenClaw is not preparable

The OpenClaw page is missing. The capabilities page says no versioned
descriptor was present. OpenClaw is not a listing you can prepare. Do not
write a launch procedure. Do not invent options, endpoints, or a digest.

Any other name has no contract in this skill. Do not invent one.

## 6. After the human says the Console launch finished

Run these reads only after the user says that launch finished, and only for
the Application id they give. If they give no id, ask. Do not invent an
application id. `APP` below is that id.

```sh
proof liskov application status APP --json --no-analytics
```

```sh
proof liskov application policy explain APP --json --no-analytics
```

```sh
proof liskov application artifact-pin list APP --json --no-analytics
```

When the user gave an organization selector for this command only, add
`--organization ORGANIZATION` with that selector. Do not change the session
default.

Compare the artifact digest printed by artifact-pin list to the digest the
public listing page printed on the day you read it. Read that page again for
the comparison. Do not type a digest from memory into the command. If the
page prints no digest, or the command prints no digest, say the check is
incomplete. Do not invent the expected digest. Do not call the result
verified or safe. There is no single verified mark.

These reads do not launch, publish, restore a pin, or spend. `policy explain`
does not recompute policy, spend, or eligibility.

## 7. Reply

Name the gate, the listing, and every digest comparison you actually made.
Do not list form fields to fill. Leave unknown ids and prices absent. A
missing live agent run is not a pass.
