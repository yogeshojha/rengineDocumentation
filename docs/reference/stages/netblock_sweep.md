---
title: Netblock Sweep
description: Find hosts by resolving reverse DNS across the network ranges the organisation announces. It sends no traffic to your target.
sources:
  - "stages/netblock_sweep/stage.py:61"
  - stages/netblock_sweep/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 205
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `netblock_sweep` |
| Group | Hosts |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 3 of 8 |
| Depends on | [Host Discovery](host_discovery.md), [Seed Resolution](seed_resolution.md), [Subdomain Discovery](subdomain_discovery.md) |
| Input | `addresses` |
| Output | `hosts` |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `dnsx` |
| API keys | None |
| Target types | Domain |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: Subdomain rows with source netblock for PTR names under the target.

## Request rate

The stage runs `dnsx` with a timeout of 5 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | Not limited | 50 |
| Normal | Not limited | 50 |
| Aggressive | Not limited | 83 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Netblock sweep | boolean | `true` |  | Resolve reverse DNS across the network ranges the organisation announces. |
| `max_sweep` (advanced) | Address budget | integer | `8192` | 256 to 65536 | Addresses resolved at most. A larger range is reported as partial. |

