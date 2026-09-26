# Limits

Read this while deciding. It is not a second workflow. See
[Command boundary](command-boundary.md).

## Fleet

Judge every program against this fleet:

| Fact | Rule |
| --- | --- |
| ARM | The fleet this skill judges. Not a sentence found on the pages cited below. |
| Residential phones | One job is one phone. Acurast processors are phones. |
| Memory-constrained | Do not invent a memory size. Do not copy the resources page's sample numbers. |
| Intermittently reachable | Assignment can change at renewal. A missed interval boundary is not caught up. |
| Outbound-only | Allowlisted public endpoints. No stable public IP, hostname, or Liskov ingress. |

Public parallelism above 1 is not a recipe. Capabilities says retained V5 is
v1 at one or two jobs. The manifest reference's first-public admission maximum
is 2. Neither sentence is permission to design two cooperating phones. Do not
propose a job count above 1. If the user already stated a count, keep that
number, including zero, and do not extend it into a peer or shard design.
Zero jobs does not place a phone. Do not rewrite zero to 1.

## Stated values

Keep an explicit zero or an explicit empty value as the user wrote it. The
resources page says explicit zero is preserved and is not treated as unset.
That sentence does not make this skill write a manifest.

Do not pick `once`. Do not pick a duration. Do not invent a spend cap, a
price, or budget consent. A cap the user stated is recorded as stated. It is
not a reserve and not a final charge.

The resources page sample uses `memoryMiB` 256, `storageMiB` 256, and
`networkRequestQuota` 1000. Those numbers are not defaults. Do not copy them
unless the user stated them. This skill does not write them either way.

## What fits

| Work | Leaves the phone by | Fit |
| --- | --- | --- |
| Scheduled check | Outbound HTTP or one log line | Fits, if the schedule is not invented here |
| Outbound probe | Outbound HTTP or one log line | Fits |
| Fan-out of fetches with one returned result | Outbound HTTP or one log line | Fits on one phone |
| One batch item | Outbound HTTP or one log line | Fits |

Fan-out means many outbound calls from that one phone, then one result. It
does not mean many jobs.

## What does not fit

| Work | Why |
| --- | --- |
| Inbound HTTP server | No public inbound. Liskov-hosted HTTP/SSH ingress is not v1. |
| Websocket server | No public inbound. |
| Shared disk or durable volume | `state.mode` is only `off`. Storage on the phone is ephemeral. |
| GPU training | No such product on the capabilities page. Does not fit. |
| Tensor-parallel serving | Does not fit. Peers and a GPU are both absent. |
| Peers on the fleet | Cohort discovery is absent. Topology selection is internal. |

A curated Tunnel or WebView facility is an offering boundary, not general
ingress. Do not move a refused inbound server onto that path.

## Schedule

| User said | This skill does |
| --- | --- |
| Nothing about schedule | Leave it unresolved. Do not pick `once` or a duration. |
| `once`, a duration, or a cap | Keep the value, including zero or empty. Do not "fix" it. |
| An interval such as `every` | Record it. Say it can be schema-valid and still not launch. |
| Cron, a calendar, or local time | Record the words. Do not convert them. Those schedules are not v1. |

Job schedule on the capabilities page is v1 only inside its own bounds
(`durationMs` at least 60000, `maxStartDelayMs` at most 3600000, and a
supplied start not more than 24 hours ahead). This skill does not choose a
duration to satisfy that bound.

## Placement

Open-market processor selection is v1. The manifest reference says omitting
exact processor selection uses open-market selection, and that allow, exclude,
spread, distribution, topology, and manager or static selectors are absent.

There is no processor catalog to shop. Do not pick a processor, a city, a
device, or a runtime instance. Do not invent a processor id.

## Pages

| Page | Use |
| --- | --- |
| [Capabilities and limits](https://docs.proof.computer/liskov/reference/capabilities) | Availability. Ingress, jobs, interval, open market. |
| [Liskov and Acurast](https://docs.proof.computer/liskov/concepts/product-boundaries) | Phones, no general HTTP or SSH ingress. |
| [Runtime resources and outbound networking](https://docs.proof.computer/liskov/configure/resources-networking) | Outbound allowlist, ephemeral storage, no public address. |
| [Retained Application Manifest V5](https://docs.proof.computer/liskov/reference/manifest-v5) | `state.mode` off, no cohort, no durable volume. |

If a page cannot be read, do not invent its rule. Say the skill cannot confirm
that page and leave the related instruction absent.
