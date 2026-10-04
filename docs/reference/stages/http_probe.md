---
title: HTTP Probe
description: "Fingerprint every host and port for live HTTP, technologies and titles. It sends traffic to your target."
sources:
  - "stages/http_probe/stage.py:111"
  - stages/http_probe/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 413
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span> <span class="rn-tag neutral">always on</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `http_probe` |
| Group | Web |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 5 of 8 |
| Depends on | [Port Scan](port_scan.md), [Virtual Host Discovery](vhost.md) |
| Input | `addresses`, `hosts` |
| Output | `http_assets` |
| Adds results to | [Web assets](../query/web-assets.md), [Services](../query/services.md) |
| Tools | `httpx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: HttpAsset rows. Port rows with source http_probe. HTTP fields copied onto Subdomain rows for a domain target. Subdomain rows for referenced hostnames.

## Request rate

The stage runs `httpx` with a timeout of 10 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 150 |
| Normal | 150 | 150 |
| Aggressive | 400 | 300 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Probe HTTP services | boolean | `true` |  | Fingerprint every host and port for live HTTP, technologies and titles. |

