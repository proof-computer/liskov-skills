# Command boundary

Read this while checking a running Application. It is not a second workflow.
This skill is read only.

Reviewed help is the flag authority. Every fenced command passes `--json` and
`--no-analytics`. Do not add `--config`, `--slipway-url`, or `--liskov-url`
unless the user supplied that value. Do not invent a URL.

`APPLICATION_ID` and `APP_REF` are the Application id the user gave. Help
prints `APPLICATION_ID` on policy explain, plans, and status. It prints
`APP_REF` on source-binding show, artifact-pin list, and deployment status.
Do not substitute a file path, a deployment id, a job id, or a digest.

`ORG_ID` is an organization id or slug the user gave. If you do not have a
value, do not invent it.

## Organization

```sh
proof liskov whoami --json --no-analytics
```

whoami is a read. Quote the organization fields it prints. That read separates
the effective organization from the persistent session organization. Do not
rename those fields.

`--organization ORG_ID` or `LISKOV_ORGANIZATION` scopes one command:

```sh
proof liskov application status APPLICATION_ID --organization ORG_ID --json --no-analytics
```

Run `organization use` only when the user asked to change the session default.
Help has no `--yes` flag. Do not invent one.

```sh
proof liskov organization use ORG_ID --json --no-analytics
```

## Reads

Run these only for the Application id the user gave. Each one is read only.
None of them publish, reserve, or charge.

```sh
proof liskov application source-binding show APP_REF --json --no-analytics
```

Help: this reads the current server-owned source binding. A 404
`source_binding_not_found` means the Application is not bound yet. Do not
invent a repository, ref, workflow, or manifest path to fill that gap.

```sh
proof liskov application artifact-pin list APP_REF --json --no-analytics
```

Help's command is `application artifact-pin list`. It takes `APP_REF`. It has
no restore flag. Do not add one.

```sh
proof liskov application policy explain APPLICATION_ID --json --no-analytics
```

Help: this reads the canonical retained V5 policy explanation envelope without
recomputing policy, spend, or eligibility. It takes `APPLICATION_ID`. It has
no `--file` flag. It does not explain a local unpublished file.

```sh
proof liskov application deployment status APP_REF --json --no-analytics
```

Help prints one argument, `APP_REF`. Do not pass a deployment id as the
positional.

```sh
proof liskov application plans APPLICATION_ID --json --no-analytics
```

```sh
proof liskov application status APPLICATION_ID --json --no-analytics
```

There is no processor list or search command. Do not invent one. Do not fence
a processor command. The Console record for the organization's own history is
[Inspect a processor your organization used](https://docs.proof.computer/liskov/operate/processors).

## Commands this skill does not run

Do not run these. Do not add flags, examples, or a procedure for them.

| Command | Rule |
| --- | --- |
| `admin` | Do not run. |
| `custody` | Do not run. |
| `delete` | Do not run. |
| `import` | Do not run. |
| V4 `application publish` | Do not run. |
| `application policy publish` | Do not run. This skill does not publish. |
| `backfill-identities` | Do not run. |
| `deployment import` | Do not run. |
| `artifact-pin restore` | Do not run. |
| `lockbox` | Do not run. |
| `devtools` | Do not run. |
| `blackbox` | Do not run. |
| `runtime-image` | Do not run. |
| `application execution` | Do not run. |
| `application hold` | Do not run. |
| `application run` | Do not run. |
| `retirement-census` | Do not run. |
| `source-binding set` | Do not run. Show is the read. Set is not. |
| `source-binding revoke` | Do not run. |
| SSH and `runtime-ssh` | Do not run. |
| pause, resume, retire, retry | Do not run. Those belong to liskov-operate. |

Do not implement a second validator.
