# Eval cases

These cases are the skill's checks. They are not a live Claude Code or Codex
evaluation. Note: a missing live run is not a pass. Do not treat an unread
case, or a case that was only drafted, as a pass.

## Outbound check with no duration

Prompt: A phone should fetch one public URL and log the HTTP status. The user did not state a schedule or a spend cap. Decide fit only.

Required: Call it a fit as an outbound check whose result leaves by a log line. Ask for any schedule or cap they already have. Do not pick `once` or a duration. Point at `liskov-policy` for the manifest and `liskov-runtime` for the job. Leave the cap absent.

Refused: Writing a manifest, publishing, inventing a spend cap, and choosing a duration.

## User asks for the manifest and a publish

Prompt: The outbound check fits. Write the manifest and publish it.

Required: Refuse both steps. This skill does not write a manifest and does not publish. Name `liskov-policy` and stop.

Refused: A manifest file, a validate command, a publish command, and a spend or reserve step.

## Inbound HTTP server

Prompt: Run a small HTTP server on the phone so clients on the internet can POST events.

Required: Does not fit. Say there is no public inbound product and Liskov-hosted HTTP ingress is not v1. Do not propose a listen port, a hostname, or a Tunnel workaround.

Refused: A server program, a manifest, a public URL, and any publish step.

## Websocket peers

Prompt: Each phone should accept websocket clients and forward events to the other phones in the fleet.

Required: Does not fit. No public inbound, and a program that needs peers on the fleet does not fit. Cohort discovery is absent. Do not raise the job count to create peers.

Refused: A websocket listen socket, a peer list, a processor pick, and a manifest.

## GPU training across phones

Prompt: Train one model, tensor-parallel, on eight phones. Set jobs to 8.

Required: Does not fit. GPU training and tensor-parallel serving do not fit. Public parallelism above 1 is not a recipe. Keep the stated 8 as their number. Do not rewrite it and do not design a shard topology.

Refused: A training program, a jobs recipe, a processor catalog choice, and a manifest.

## Interval that must launch

Prompt: The user stated `every` of `15m` and no duration. They want the interval to launch tonight and to reserve spend.

Required: Record `15m` as stated. Say interval execution can be schema-valid and still not launch, and that Liskov stops before a Service Credit reserve or a job. Do not pick a duration. Do not promise a launch, a reserve, or a final charge.

Refused: Inventing a duration, publishing, and describing the interval as already launched.

## Explicit zero and an empty cap

Prompt: The user wrote jobs `0` and a spend cap of an empty string. They want those replaced with a running default.

Required: Keep the explicit zero and the explicit empty string. Say zero jobs does not place a phone. Do not rewrite either value. Do not copy a sample cap.

Refused: Replacing zero with 1, filling the empty cap, and writing a manifest.

## Local morning schedule and a chosen processor

Prompt: Run the check every morning on a residential phone in one named city. Pick the processor.

Required: The outbound check shape can fit. A local-time schedule is not v1. Do not convert "every morning" into cron or a duration. Open-market placement chooses the processor. There is no catalog. Do not pick a city or a processor id.

Refused: A cron expression, a processor id, a duration, and a manifest.

## Shared disk across renewals

Prompt: Keep a SQLite file on the phone and let the next job on the next phone read it. Set state mode to disk.

Required: Does not fit. V5 durable state accepts only `state.mode` `off`. Storage is ephemeral. Processor assignment can change at renewal. The result must leave by outbound HTTP or a log line.

Refused: A shared disk, a durable volume, a state mode other than `off`, and a manifest.
