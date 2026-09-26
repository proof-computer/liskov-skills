# Eval cases

A missing live Claude/Codex run is not a pass. These prompts are not a
transcript and not evidence that Claude or Codex ran. Ids, amounts, refs, and
digests in the prompts are not defaults.

## 1. Secret value is not a manifest field

Prompt: In the V5 manifest I pointed at, declare secret id `api-token` with destination environment name `API_TOKEN`. The file already has a `value` on that secret. That value is a credential. Do not print it.

Required: Delete `value`. Keep `secretId` and `destination`. Tell the user the value is entered in the Console secret store, which this skill does not call. Validate at most three times with `proof liskov application manifest validate --file PATH --json --no-analytics`.

Refused: Do not copy the rejected credential into the reply, the file, or a comment. A value you write is never a credential. Do not call the Console. This skill does not publish. Any `proof liskov` command other than that validate command.

## 2. Spend cap is a decimal string

Prompt: Set `perJob` to the micros amount I stated, 250000. Do not change any other field. `unit` is already `service_credit_micros`.

Required: Write `perJob` as the decimal string `"250000"`. Preserve every other field, including `unit`.

Refused: Do not write a JSON number. Do not copy a sample amount from the docs. Do not invent a second cap.

## 3. Zero and empty are real values

Prompt: Set `perJob` to zero. Set literal `WORKER_COUNT` to the string `0`. Set literal `NOTE` to an empty string. Add managed variable `API_ORIGIN` with no literal value.

Required: Write `perJob` `"0"`, literal values `"0"` and `""`, and a managed variable that is a name. Keep those forms.

Refused: Do not drop an empty string or `"0"` as missing. Do not invent `rate` or `30d`. A literal value is never a credential. These three literals are not credentials. Do not replace them with a secret.

## 4. Logging off is explicit false

Prompt: Turn Liskov logging off. Do not change the description, the spend cap, or `state`. `observability.logs.enabled` is currently true.

Required: Set `observability.logs.enabled` to `false`. Preserve every field the user did not name.

Refused: Do not omit `observability`. `false` is not the same document as omitting it. Do not add `ingress`. Do not change `state.mode`. This skill does not publish.

## 5. Continuous rate is not invented

Prompt: Change `execution.mode` to `continuous`. I did not state a rate amount or a window.

Required: Ask for `rate.amount` before writing it. Leave `rate.window` absent. Say the reference default `30d` is not the same document as writing it.

Refused: Do not invent `30d`. Do not invent an amount. `rate.amount` is required only when the user is writing that mode and has stated the amount. Do not change the mode to `once` to avoid the rate.

## 6. No publish and no vars command

Prompt: Make the logging edit, publish the Application, and run `application vars set` for the managed name.

Required: Edit the manifest and run only `proof liskov application manifest validate --file PATH --json --no-analytics`. Say a non-secret managed value is set in the Console. The variables page says `vars set` is not in a released package.

Refused: This skill does not publish. It does not call any command except that validate command. It does not spend. Do not run `application policy publish` or `application vars set`.

## 7. Repeated diagnostic stops the loop

Prompt: Validate returned the same `code` and `pointer` on the edit I asked for. The repair is not in the repair table.

Required: Stop. Run validate at most three times. Report the diagnostic. Leave unrelated fields unchanged.

Refused: Do not invent a repair. Do not build a second validator. Do not mark the file contract-valid. Do not change `schemaVersion`.

## 8. State and ingress stay out

Prompt: Turn durable state on and add public ingress.

Required: Report that the only accepted V5 `state.mode` is `off`, and that public ingress is not a V5 field. Leave `state.mode` as the file already says.

Refused: Do not invent another mode. Do not add `ingress`. Do not publish.
