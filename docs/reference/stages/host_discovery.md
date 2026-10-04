---
title: Host Discovery
description: Sweep a netblock for responsive hosts before port scanning. It sends traffic to your target.
sources:
  - "stages/host_discovery/stage.py:19"
  - stages/host_discovery/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 108
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `host_discovery` |
| Group | Addresses |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 2 of 8 |
| Depends on | [Seed Resolution](seed_resolution.md) |
| Input | None |
| Output | `addresses` |
| Adds results to | [IP addresses](../query/ips.md) |
| Tools | `naabu` |
| API keys | None |
| Target types | ASN, CIDR range |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: IpAddress.is_alive.

## Request rate

The stage runs `naabu` with a timeout of 5 s and 1 retry. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 30 |
| Normal | 150 | 30 |
| Aggressive | 450 | 60 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Find live hosts | boolean | `true` |  | Sweep a netblock for responsive hosts before port scanning. |

