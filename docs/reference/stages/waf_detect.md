---
title: WAF Detection
description: Fingerprint web application firewalls in front of live web assets. It sends traffic to your target.
sources:
  - "stages/waf_detect/stage.py:18"
  - stages/waf_detect/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 516
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">support</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `waf_detect` |
| Group | Web |
| Role | Support: reNgine runs it when a stage you selected needs what it produces, or when its own input is available |
| Step | 6 of 8 |
| Depends on | [HTTP Probe](http_probe.md) |
| Input | `http_assets` |
| Output | None |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `wafw00f` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: HttpAsset.waf.

## Request rate

The stage runs `httpx` with a timeout of 10 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 6 |
| Normal | 150 | 6 |
| Aggressive | 400 | 12 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Detect WAFs | boolean | `true` |  | Fingerprint web application firewalls in front of live web assets. |

