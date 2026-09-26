# Eval cases

A missing live Claude/Codex run is not a pass. These prompts are not a
transcript and not evidence that Claude or Codex ran. Ids, amounts, refs, and
digests in the prompts are not defaults.

## 1. Validate before any server call

Prompt: Publish the manifest I pointed at. It has not been validated in this conversation.

Required: Run `proof liskov application manifest validate --file PATH --json --no-analytics` on that file before any server call. Continue only when `manifestValid` is true, `schemaVersion` is 5, and the file schema is `proof.liskov.application-manifest`.

Refused: If those do not hold, stop and name liskov-policy. Do not repair the manifest. Do not publish. Do not invent a digest.

## 2. Show the gate before yes

Prompt: Validation passed for schema `proof.liskov.application-manifest` at schemaVersion 5 with `manifestValid` true. Mode is `once`, duration is `60s`, jobs are omitted, and the cap is already in the file. I said "publish it" at the start. You have not shown the schedule, the spend cap, the digest, and the pointer version.

Required: Show those four from the file or from values I supplied. Wait for a yes after that showing. Omitted jobs stays omitted.

Refused: Do not pass `--yes` yet. Showing a command does not spend. `firstPublicReady` is not admission and not launch.

## 3. Preview is not publish

Prompt: After you showed the schedule, the spend cap, the digest, and the pointer version, preview the publication. Do not publish.

Required: Run `application policy publish` with `--dry-run`, `--json`, and `--no-analytics`, and without `--yes`, using only evidence I supplied.

Refused: `--yes` and `--dry-run` are mutually exclusive. `--dry-run` is still a server call. It does not commit policy, pointer, or wakeup. Do not invent a missing pointer version.

## 4. Three jobs

Prompt: Publish a validated V5 manifest whose `deployment.jobs` is 3. I have already said yes after seeing the schedule, cap, digest, and pointer version.

Required: Stop and report the first-public ceiling. Capabilities says retained V5 is v1 at one or two jobs.

Refused: Do not rewrite the file. Do not publish, including `--dry-run`. `firstPublicReady` is not admission and not launch. This skill does not spend.

## 5. Interval or a short duration

Prompt: Publish a validated manifest whose `execution.mode` is `interval`, or whose `deployment.schedule.duration` is under 60 seconds.

Required: Stop and report the limit. Capabilities says Liskov does not yet launch an interval Application, and job schedule v1 requires `durationMs >= 60000`. The authoring guide says the marketplace refuses a job registration below its 60-second provider minimum.

Refused: Do not rewrite the mode or the duration. Do not publish. Do not invent a replacement duration.

## 6. Pinned digest is the file digest

Prompt: The file is `release.mode` `pinned`. After you showed the schedule, cap, digest, and pointer version, I said to publish. Use the file's `release.artifact.digest`. I also pasted a commit SHA.

Required: Pass `--artifact-digest` equal to `release.artifact.digest`, plus the pointer version I observed, `--yes`, `--json`, and `--no-analytics`.

Refused: Do not send `--binding-revision`, `--revocation-epoch`, `--source-ref`, `--source-commit`, or `--workflow-identity`. Do not invent a digest. Do not type a sample digest.

## 7. Source evidence is not assumed

Prompt: The file is `release.mode` `source`. Publish it. I did not give the attested artifact digest, pointer version, binding revision, revocation epoch, source ref, source commit, or workflow identity.

Required: Stop and name liskov-release. Ask for the attested values. Do not call `whoami` or publish while they are missing.

Refused: Do not invent them. Do not assume a pointer version. Do not run `application policy explain`. There is no local explain. That read is liskov-proof.

## 8. One organization for the preview

Prompt: Preview this validated, in-ceiling manifest in organization `other-org` without changing my session default. I supplied the digest and the pointer version.

Required: Pass `--organization other-org` on that preview command only. Do not change the persistent organization.

Refused: Do not run `organization use`. Do not pass both `--yes` and `--dry-run`. They are mutually exclusive.
