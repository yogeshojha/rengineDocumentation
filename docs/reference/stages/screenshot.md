---
title: Screenshots
description: Render live web assets to images. It sends traffic to your target.
sources:
  - "stages/screenshot/stage.py:62"
  - stages/screenshot/
  - stages/registry.py
revised: 2026-10-03
generated: scripts/gen_stages.py
layout: reference
nav_order: 617
---

This page is generated from the reNgine 3.0 source. `scripts/gen_stages.py` writes it from `data/stages.json`. To change it, edit the script or refresh the data, not this page.
{ .rn-gen }

<span class="rn-tag active">Active</span> <span class="rn-tag neutral">capability</span>

Use this page to check when the stage runs, what it needs from earlier stages, what it adds to your results and which options you can set. To see how it fits with the other stages, go to [Stages](index.md).

| Property | Value |
|---|---|
| Key in the engine YAML | `screenshot` |
| Group | Web |
| Role | Capability: you select it in a scan engine or a custom scan |
| Step | 7 of 8 |
| Depends on | [Origin Probe](origin_probe.md) |
| Input | `http_assets` |
| Output | None |
| Adds results to | [Web assets](../query/web-assets.md) |
| Tools | `httpx` |
| API keys | None |
| Target types | ASN, Domain, IP address, CIDR range, URL |
| On by default | Yes |
| In the Default engine | Yes |
| Sends traffic to the target | Yes |
| At passive intensity | Skipped |

What it stores in the database: Image files under /app/scan_media/<scan id> and HttpAsset.screenshot_path, copied to Subdomain for a domain target.

## Request rate

The stage runs `httpx` with a timeout of 10 s. Its rate and threads depend on the intensity you choose.

| Intensity | Rate per second | Threads |
|---|---|---|
| Passive | 150 | 40 |
| Normal | 150 | 40 |
| Aggressive | 400 | 80 |

## Options

You set these options per stage: in the engine editor, in the engine YAML, or in the stage settings of a custom scan.

| Option | Label | Type | Default | Values | Description |
|---|---|---|---|---|---|
| `enabled` | Capture screenshots | boolean | `true` |  | Render live web assets to images. |
| `max_screenshots` (advanced) | Screenshot budget | integer | `0` | 0 to 100000 | Most web assets to render, best first. 0 renders every one. |

