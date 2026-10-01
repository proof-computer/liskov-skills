# Limits

Do not widen these rows. The owner is
[Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities).
The procedure owner is
[Use retained V5 Managed Runtime SSH](https://docs.proof.computer/liskov/operate/runtime-ssh-v5).

| Surface | Availability the page gives |
| --- | --- |
| Managed Runtime SSH, Liskov-operated relay | Preview on Developer and above |
| Retained V5 managed path | Preview on Developer and above. Native image only. `access.ssh.provider.kind` `liskov_managed` |
| Customer-owned Tailscale SSH | Separate Preview on Pro and above. Roadmap in Integrations until a live policy version can name it |

Customer-owned SSH stays on that capabilities row. This skill does not set
it up.

## What the V5 page requires

| Requirement | Bound |
| --- | --- |
| Plan | Developer or above. `runtime_ssh_plan_required` means do not retry the same request |
| Runtime | `native_image` only. No port, mode, Tailscale, or tunnel field on this arm |
| Keys | `ssh-ed25519` only. Register at least one before the first launch |
| Attachment size | The V5 page says an attachment accepts 1–8 keys. More than eight registered keys makes attachment preparation fail closed |
| Registry cap | The CLI reference says the registry holds at most 50 keys. Fifty is not the attachment limit |
| Empty registry | Attachment preparation fails closed. A job that started against an empty registry is served `runtime_ssh_operator_key_registry_empty` for the whole of that run |
| Snapshot | Existing attachments are not narrowed in place. A new key reaches the next attachment only |
| Session | One session at a time. An open session drains. It is not cut |
| Drain | Ends when the operator disconnects, when the job ends, or at the relay's two-hour maximum. A missed heartbeat closes after 60 seconds |
| Ticket | Minted only after host trust, on the real open. `--print-command` does not mint one. A ticket is single use |
| Relay loss | Open sessions drop until the relay returns. Jobs are unaffected |
| Sandbox relaunch | Managed SSH reconnects on its own, usually within a minute, under a new host key. CLI `0.16.0` and later ask for confirmation |
| Helper or sidecar failure | Ends managed SSH for that job until the next run. The job itself is unaffected |

Relay traffic counts against the plan's included log volume and is charged
at the log overage rate above it.

The relay cannot read the session. Liskov brokers metadata and one-time
tickets and verifies the runtime-contact and SSH server binaries. The
customer runtime image is not attested by that verification.

## Host keys

A relaunch reports the previous fingerprint and the new one. Name both
fingerprints from that output before `--accept-host-key`. Do not invent a
fingerprint. Any other mismatch is `RUNTIME_SSH_HOST_KEY_MISMATCH`. Stop.
Do not delete the pin and do not relax checking.

## Not this skill

Do not generate a key. Do not teach `runtime-ssh integration`. Do not claim
Free, or a non-native runtime, can use this path. Do not claim revoke or
withdraw ends the job. Force stop is not a public customer action. Ending
the job sooner is outside this skill.

Report a fingerprint list only when the JSON you just read contains that
field. Do not say the print-command JSON includes a list it did not print.

Share identifiers and timestamps with support. Never share private keys,
bearer tickets, session files, or secret values.
