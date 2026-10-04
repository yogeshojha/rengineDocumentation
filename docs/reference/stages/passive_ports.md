---
title: Passive Port Discovery
description: Read ports indexed for each address by internet-wide scanners. It sends no traffic to your target.
sources:
  - "stages/passive_ports/stage.py:22"
  - stages/passive_ports/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 210
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `passive_ports` |
| Group | Services |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 3 of 8 |
| Depends on | [Host Discovery](host_discovery.md), [Seed Resolution](seed_resolution.md), [Subdomain Discovery](subdomain_discovery.md) |
| Input | `addresses` |
| Output | `ports` |
| Adds results to | [Services](../query/services.md) |
| Tools | `naabu` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: Port rows with source internetdb.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Look up indexed ports | boolean | `true` |  | Read ports indexed for each address by internet-wide scanners. |

