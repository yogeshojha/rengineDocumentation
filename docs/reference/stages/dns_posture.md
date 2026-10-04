---
title: Domain posture
description: "SPF, DMARC, DKIM, MTA-STS, DNSSEC and CAA read from each zone. It sends traffic to your target."
sources:
  - "stages/dns_posture/stage.py:58"
  - stages/dns_posture/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 618
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `dns_posture` |
| Group | Hosts |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 7 of 8 |
| Depends on | [Subdomain Discovery](subdomain_discovery.md) |
| Input | `hosts` |
| Output | None |
| Adds results to | None |
| Tools | `dnsx` |
| API keys | None |
| Target types | Domain, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Runs, but skips what sends traffic to the target |

What it stores in the database: domain_posture rows, one per zone, folded onto host rows. Not a surface dimension.

What changes at passive intensity: The MTA-STS policy file is not fetched (fetch_policy is False). DNS lookups run.

## Request rate

The stage runs `dnsx` with a timeout of 5 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | Not limited | 30 |
| Normal | Not limited | 30 |
| Aggressive | Not limited | 50 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Domain posture | boolean | `true` |  | SPF, DMARC, DKIM, MTA-STS, DNSSEC and CAA read from each zone. |
| `dkim_selectors` (advanced) | DKIM selectors probed | array | `default`, `google`, `selector1`, `selector2`, `k1`, `k2`, `s1`, `s2`, `dkim`, `mail`, `smtp`, `mandrill`, and 8 more | At most 60 items | Selector names queried under _domainkey. |

