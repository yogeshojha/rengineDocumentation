---
title: Origin Probe
description: Request each address by IP and record what it serves without a hostname. It sends traffic to your target.
sources:
  - "stages/origin_probe/stage.py:38"
  - stages/origin_probe/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 514
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `origin_probe` |
| Group | Services |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 6 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `ports` |
| Output | `vulnerabilities` |
| Adds results to | [Web assets](../query/web-assets.md), [Vulnerabilities](../query/vulnerabilities.md) |
| Tools | `httpx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |
| Findings | Reported as findings of [Vulnerability Scan](vulnerability_scan.md), severities <span class="rn-sev medium">medium</span>, <span class="rn-sev low">low</span> |

What it stores in the database: HttpAsset rows for addresses requested without a hostname. Origin exposure findings (scanner rengine).

## Request rate

The stage runs `httpx` with a timeout of 10 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 30 |
| Normal | 150 | 30 |
| Aggressive | 400 | 60 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Probe addresses directly | boolean | `true` |  | Request each address by IP and record what it serves without a hostname. |
| `max_addresses` (advanced) | Address budget | integer | `2048` | 1 to 65536 | Stop after this many addresses. |

