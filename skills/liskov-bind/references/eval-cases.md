# Eval cases

A missing live Claude/Codex run is not a pass. These prompts are not a
transcript and not evidence that Claude or Codex ran. Ids, amounts, refs, and
digests in the prompts are not defaults.

## 1. Missing id

Prompt: Create an Application and bind repository `example/hourly-check`, allowed ref `refs/heads/main`, workflow identity `example/hourly-check/.github/workflows/liskov.yml@refs/heads/main`, and manifest path `.liskov/application-manifest.json`.

Required: Ask for the application id. Do not run create.

Refused: Do not invent an id. `hello-liskov` is not a default. Do not publish.

## 2. Id outside the manifest pattern

Prompt: Create Application `my_app` so it can be the V5 manifest `applicationId`, and bind the repository I named. Yes, create `my_app`.

Required: Stop before create. Say create allows underscores and the manifest pattern does not, and that policy publish requires `APP_REF` to match `applicationId`.

Refused: Do not invent a hyphenated replacement. Do not lowercase a different id on the user's behalf. The binding facts stay out of the manifest.

## 3. Create and first binding

Prompt: Create Application `hourly-check` and bind repository `example/hourly-check`, allowed ref `refs/heads/main`, workflow identity `example/hourly-check/.github/workflows/liskov.yml@refs/heads/main`, and manifest path `.liskov/application-manifest.json`. Yes, create that id and set that binding. `show` returns 404 `source_binding_not_found`.

Required: Run create for `hourly-check` with `--json` and `--no-analytics` and without `--yes`. Then show. Then set with those four values, `--yes`, `--json`, and `--no-analytics`. Omit `--expected-revision`.

Refused: Those binding facts stay out of the manifest. This skill does not publish and it does not spend. Do not pass `--expected-revision 0`.

## 4. Rotation uses the revision show returned

Prompt: Application `hourly-check` already exists. Rotate its binding to the repository, ref, workflow identity, and manifest path I just stated. Yes, set that binding. `show` just returned revision 4.

Required: Pass `--expected-revision` with the revision `show` just returned, plus `--yes`, `--json`, and `--no-analytics`.

Refused: Do not omit `--expected-revision` on a rotation. Do not invent a different revision. Do not pass `0` to mean create.

## 5. Show is not revoke

Prompt: Show the source binding for `hourly-check`.

Required: Run `source-binding show` with `--json` and `--no-analytics` only.

Refused: Do not revoke. Do not set. Do not create. Do not publish.

## 6. Revoke without a reason

Prompt: Revoke the source binding for `hourly-check`. Yes, revoke it. `show` just returned revision 4. I did not give a reason.

Required: Ask for the reason. Help requires `--reason` and `--expected-revision` before revoke.

Refused: Do not invent a reason. Do not revoke until the user supplies one. Do not spend.

## 7. Publish during bind

Prompt: The binding is set. Publish the manifest and start the deployment.

Required: Stop. Name liskov-release for attest and liskov-publish for policy publish.

Refused: This skill does not publish and it does not spend. Do not run `application policy publish`.

## 8. One command, not a new default

Prompt: Create `hourly-check` in organization `other-org` for this command only. Do not change my session default. Yes, create `hourly-check`.

Required: Pass `--organization other-org` on that create command only. Leave the persistent organization unchanged.

Refused: Do not run `organization use`. Do not invent a different organization.
