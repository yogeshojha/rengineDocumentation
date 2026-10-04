---
title: Seed Resolution
description: "Expand an IP, netblock, ASN or URL seed into individual addresses. It sends no traffic to your target."
sources:
  - "stages/seed_resolution/stage.py:23"
  - stages/seed_resolution/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 2
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `seed_resolution` |
| Group | Addresses |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 1 of 8 |
| Depends on | None |
| Input | None |
| Output | `addresses` |
| Adds results to | [IP addresses](../query/ips.md) |
| Tools | `dnsx` |
| API keys | None |
| Target types | ASN, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: IpAddress rows with source seed, cidr_expansion or asn_expansion.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Seed resolution | boolean | `true` |  | Expand an IP, netblock, ASN or URL seed into individual addresses. |
| `asn_scan_mode` | ASN / CIDR expansion | string | `smart` | `smart`, `full` | Smart samples large netblocks. Full enumerates every host. |

