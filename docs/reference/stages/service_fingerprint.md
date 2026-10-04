---
title: Service Fingerprint
description: Identify the software behind every non-web port from its service banner. It sends traffic to your target.
sources:
  - "stages/service_fingerprint/stage.py:26"
  - stages/service_fingerprint/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 515
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `service_fingerprint` |
| Group | Services |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 6 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `ports` |
| Output | None |
| Adds results to | [Services](../query/services.md) |
| Tools | None |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Port service_name, product, version, banner and tls (source banner).

## Request rate

The stage runs `banner` with a timeout of 4 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | Not limited | 32 |
| Normal | Not limited | 32 |
| Aggressive | Not limited | 64 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Fingerprint services | boolean | `true` |  | Identify the software behind every non-web port from its service banner. |
| `max_services` (advanced) | Service budget | integer | `2000` | 1 to 50000 | Stop after this many ports. |

