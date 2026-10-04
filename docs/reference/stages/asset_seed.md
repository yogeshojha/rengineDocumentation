---
title: Seed Assets
description: Start a run from stored assets and assets chosen in an earlier run. It sends no traffic to your target.
sources:
  - "stages/asset_seed/stage.py:36"
  - stages/asset_seed/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 0
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag passive">Passive</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `asset_seed` |
| Group | Hosts |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 1 of 8 |
| Depends on | None |
| Input | None |
| Output | `addresses`, `hosts` |
| Adds results to | [Web assets](../query/web-assets.md), [IP addresses](../query/ips.md), [Endpoints](../query/endpoints.md), [Services](../query/services.md) |
| Tools | `dnsx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | No |
| In the Default engine | No |
| Sends traffic to the target | No |
| At passive intensity | Runs unchanged |

What it stores in the database: Subdomain rows for seeded hosts, IpAddress rows (source seed), Endpoint rows for URL seeds (source import or proxy), Port rows (source seed) for URL seeds on a non-default port.

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Seed chosen assets | boolean | `false` |  | Start this run from assets picked in an earlier scan. |

